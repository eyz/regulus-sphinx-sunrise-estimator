#!/usr/bin/env python3
"""
Regulus-Sphinx Almanac-Based Optuna Optimizer
==============================================
Finds the best upcoming date and exact moment for the prophecy:

  "When the red star of Regulus aligns just before dawn
   in the gaze of the Sphinx."

Interpretation (repo author):
  - "Red star" = literal atmospheric reddening near the horizon.
    Red = warning (cf. "red sky at morning, sailor take warning").
  - "On the horizon" = imminent (the event is about to happen).
  - "Just before dawn" = sun almost rising. Maximum imminence.

Scoring — four physical factors, product (no weights):
  - redness:    precession → altitude → airmass → B-V color shift
  - imminence:  sun angle below horizon (closer to rising → higher)
  - visibility: star contrast vs sky (atmosphere dims + sky brightens)
  - az_prox:    Gaussian on |Regulus az - 90°| (Sphinx's gaze)
  - composite = redness × imminence × visibility × az_proximity

Architecture:
  Study A (near-term): almanac-based 2D search, 2026-2031
  Study B (deep-time): mirror-log 3D search, 2026-6500 CE

References:
  - SQM twilight model (hnsky.org): empirical zenith sky brightness
  - Kasten & Young (1989), airmass formula
  - Hardie (1962), extinction coefficients
  - Optuna: Akiba et al. (2019), KDD
"""

import warnings
import numpy as np
from pathlib import Path

import optuna
from optuna.samplers import TPESampler
from skyfield import almanac
from skyfield.api import wgs84, N, E

from regulus_upcoming_alignment import (
    setup, observed_bv, observed_vmag,
    airmass_kasten_young, bv_to_color_name, twilight_phase,
    imminence_score, redness_score, visibility_score,
    az_proximity_score, prophecy_score,
    GIZA_LAT, GIZA_LON, SPHINX_AZIMUTH,
    DEFAULT_AZ_SIGMA,
)

warnings.filterwarnings("ignore", category=FutureWarning)
optuna.logging.set_verbosity(optuna.logging.WARNING)

NEAR_TERM_START = 2026
NEAR_TERM_END = 2031
PEAK_REDNESS_YEAR = 4244  # Dec≈0° → Regulus crosses az=90° at the horizon
END_YEAR = 6500           # well past peak, redness declining
DAWN_WINDOW_SEC = 5400    # ~90 min, conservative Giza dawn estimate
N_TRIALS_NEAR = 2000
N_TRIALS_DEEP = 10000
N_STARTUP_NEAR = 100
N_STARTUP_DEEP = 500
TOP_N_REPORT = 20

# Mirror-log year mapping: two log-space segments joined at peak redness.
# t in [0,2] → year.  t<1: log-dense near 2026, reaches 4244.
#                       t≥1: log-dense near 4244, reaches 6500.
_SEG1_SPAN = PEAK_REDNESS_YEAR - NEAR_TERM_START   # 2218
_SEG2_SPAN = END_YEAR - PEAK_REDNESS_YEAR           # 2256
_LOG_SEG1 = np.log10(_SEG1_SPAN)                    # ~3.35
_LOG_SEG2 = np.log10(_SEG2_SPAN)                    # ~3.35


def redness_strength_from_bv(bv):
    """Human-readable redness strength from B-V bins."""
    if bv < 0.3:
        return "very mild"
    if bv < 0.6:
        return "mild"
    if bv < 0.9:
        return "moderate"
    if bv < 1.2:
        return "strong"
    if bv < 1.5:
        return "very strong"
    return "extreme"


def format_bv_label(bv):
    """Compact B-V label with color class and strength."""
    return f"{bv:+.2f} ({bv_to_color_name(bv)}, {redness_strength_from_bv(bv)})"


def mirror_log_year(t):
    """
    Map t in [0, 2] to a year in [2026, 6500] with mirror-log density.

    Segment 1 (t=0→1): log-space from 2026 toward 4244.
      Dense near 2026 (near-term), sparser in the middle.
    Segment 2 (t=1→2): log-space from 4244 toward 6500.
      Dense near 4244 (peak redness), sparser toward 6500.

    The join at t=1 (year=4244) creates a natural concentration of
    trials around peak redness from both sides.
    """
    if t < 1.0:
        offset = 10 ** (t * _LOG_SEG1)
        return NEAR_TERM_START + int(round(offset))
    else:
        offset = 10 ** ((t - 1.0) * _LOG_SEG2)
        return PEAK_REDNESS_YEAR + int(round(offset))


def compute_almanac(observer, sun_body, ts, start_year, end_year):
    """
    Use Skyfield's almanac to find sunrise and astronomical twilight start
    for every day in the given year range.

    Returns dict with numpy arrays:
      sunrise_jd, dawn_start_jd, dawn_duration_sec,
      window_before_sec (2× dawn duration), window_after_sec (+15 min)
    """
    t0 = ts.utc(start_year, 1, 1)
    t1 = ts.utc(end_year, 1, 1)

    print("  Computing sunrises ...")
    t_rise, y_rise = almanac.find_risings(observer, sun_body, t0, t1)
    sunrise_jds = t_rise.tt[y_rise]
    print(f"    {len(sunrise_jds):,} sunrises found")

    print("  Computing astronomical twilight starts (Sun crossing -18 deg) ...")
    t_dawn, y_dawn = almanac.find_risings(
        observer, sun_body, t0, t1, horizon_degrees=-18
    )
    dawn_start_jds = t_dawn.tt[y_dawn]
    print(f"    {len(dawn_start_jds):,} dawn starts found")

    n_days = min(len(sunrise_jds), len(dawn_start_jds))
    sunrise_jds = sunrise_jds[:n_days]
    dawn_start_jds = dawn_start_jds[:n_days]

    dawn_duration_sec = (sunrise_jds - dawn_start_jds) * 86400.0

    mask = dawn_duration_sec > 0
    sunrise_jds = sunrise_jds[mask]
    dawn_start_jds = dawn_start_jds[mask]
    dawn_duration_sec = dawn_duration_sec[mask]

    avg_dur = np.mean(dawn_duration_sec) / 60
    window_before = dawn_duration_sec * 2.0
    window_after = np.full_like(dawn_duration_sec, 15.0 * 60.0)
    avg_before = np.mean(window_before) / 60
    print(f"    {len(sunrise_jds):,} valid days after pairing")
    print(f"    Avg dawn duration: {avg_dur:.1f} min")
    print(f"    Search window: -{avg_before:.0f} min to +15 min from sunrise"
          f" ({avg_before + 15:.0f} min total)")

    return {
        "sunrise_jd": sunrise_jds,
        "dawn_start_jd": dawn_start_jds,
        "dawn_duration_sec": dawn_duration_sec,
        "window_before_sec": window_before,
        "window_after_sec": window_after,
    }


def evaluate_moment(jd, observer, sun_body, regulus, ts):
    """
    Evaluate the prophecy score at a single moment in time.
    Two Skyfield calls (Regulus + Sun), then score.

    Returns dict with all observables and scores, or None if invalid.
    """
    t = ts.tt_jd(jd)

    reg_app = observer.at(t).observe(regulus).apparent()
    reg_alt_obj, reg_az_obj, _ = reg_app.altaz()
    reg_alt = reg_alt_obj.degrees
    reg_az = reg_az_obj.degrees

    if reg_alt < -2:
        return None

    sun_app = observer.at(t).observe(sun_body).apparent()
    sun_alt_obj, _, _ = sun_app.altaz()
    sun_alt = sun_alt_obj.degrees

    r_sc = redness_score(reg_alt)
    imm_sc = imminence_score(sun_alt)
    v_mag = observed_vmag(reg_alt)
    vis_sc = visibility_score(v_mag, sun_alt)
    az_sc = az_proximity_score(reg_az)
    comp = prophecy_score(r_sc, imm_sc, vis_sc, az_sc)

    bv_obs = observed_bv(reg_alt)
    cal = t.tt_calendar()

    return {
        "year": cal[0], "month": cal[1], "day": cal[2],
        "hour": cal[3], "minute": cal[4], "second": cal[5],
        "jd": jd,
        "reg_alt": reg_alt, "reg_az": reg_az,
        "sun_alt": sun_alt,
        "bv_obs": bv_obs, "v_mag": v_mag,
        "airmass": airmass_kasten_young(reg_alt),
        "color_name": bv_to_color_name(bv_obs),
        "twilight": twilight_phase(sun_alt),
        "redness": r_sc, "imminence": imm_sc,
        "visibility": vis_sc, "az_score": az_sc,
        "composite": comp,
    }


def print_result_detail(r, rank=None):
    prefix = f"  #{rank}" if rank else "  "
    sec = r.get("second", 0)
    print(f"{'─'*70}")
    print(f"{prefix}  {r['year']}-{r['month']:02d}-{r['day']:02d}"
          f"  {r['hour']:02d}:{r['minute']:02d}:{sec:04.1f} UTC")
    print(f"{'─'*70}")
    print(f"  PROPHECY SCORE:        {r['composite']:.6f}"
          f"  (redness × imminence × visibility × az_prox)")
    print(
        f"    Moment (single-stage): red={r['redness']:.4f}"
        f" imm={r['imminence']:.4f}"
        f" vis={r['visibility']:.4f}"
        f" az={r['az_score']:.4f}"
    )
    print(f"    Redness:             {r['redness']:.6f}"
          f"  (B-V: {format_bv_label(r['bv_obs'])})")
    print(f"    Imminence:           {r['imminence']:.6f}"
          f"  (Sun alt: {r['sun_alt']:.2f}°, {r['twilight']})")
    print(f"    Visibility:          {r['visibility']:.6f}"
          f"  (V mag: {r['v_mag']:.1f} after extinction)")
    print(f"    Az proximity:        {r['az_score']:.6f}"
          f"  (Regulus az: {r['reg_az']:.2f}°, Sphinx: {SPHINX_AZIMUTH}°)")
    print(f"  Regulus altitude:      {r['reg_alt']:.2f}°")
    print(f"  Airmass:               {r['airmass']:.1f}")
    if "offset_sec" in r:
        print(f"  Offset from sunrise:   {r['offset_sec']:+.0f}s"
              f"  ({r['offset_sec']/60:+.1f} min)")
    print()


def _log_trial_result(result, offset_sec, comp, best_composite, n_trials, trial_num):
    """Shared logging for trial results."""
    is_new_best = comp > best_composite[0]
    if is_new_best:
        best_composite[0] = comp

    if is_new_best or trial_num < 5 or (trial_num < 100 and trial_num % 20 == 0) or trial_num % 200 == 0:
        marker = " ★ NEW BEST" if is_new_best else ""
        print(f"  Trial {trial_num:>5d}/{n_trials}{marker}")
        if is_new_best:
            r = result
            print(f"    {r['year']}-{r['month']:02d}-{r['day']:02d}"
                  f" {r['hour']:02d}:{r['minute']:02d}:{r.get('second',0):04.1f} UTC"
                  f"  offset={offset_sec:+.0f}s")
            print(f"    Sun={r['sun_alt']:.1f}° ({r['twilight']})"
                  f"  Reg alt={r['reg_alt']:.1f}° az={r['reg_az']:.2f}°"
                  f"  B-V={format_bv_label(r['bv_obs'])}")
            print(f"    red={r['redness']:.4f}"
                  f"  imm={r['imminence']:.4f}"
                  f"  vis={r['visibility']:.4f}"
                  f"  az={r['az_score']:.4f}"
                  f"  → {comp:.6f}")
        else:
            print(f"    best so far: {best_composite[0]:.6f}")
        print()

    return is_new_best


def run_near_term(alm, observer, sun_body, regulus, ts):
    """Study A: almanac-based search over the near-term window."""
    n_days = len(alm["sunrise_jd"])
    avg_b = np.mean(alm["window_before_sec"]) / 60

    print(f"STUDY A — NEAR-TERM ({NEAR_TERM_START}–{NEAR_TERM_END})")
    print(f"  {n_days:,} days × pre-dawn window (~-{avg_b:.0f} to +15 min)")
    print(f"  {N_TRIALS_NEAR:,} trials (TPE, {N_STARTUP_NEAR} startup)")
    print()

    best_composite = [0.0]
    all_results = []

    def objective(trial):
        day_idx = trial.suggest_int("day", 0, n_days - 1)
        before = alm["window_before_sec"][day_idx]
        after = alm["window_after_sec"][day_idx]
        offset_sec = trial.suggest_float("offset_sec", -before, after)

        jd = alm["sunrise_jd"][day_idx] + offset_sec / 86400.0
        result = evaluate_moment(jd, observer, sun_body, regulus, ts)
        if result is None:
            return 0.0

        result["offset_sec"] = offset_sec
        comp = result["composite"]
        all_results.append(result)
        _log_trial_result(result, offset_sec, comp, best_composite,
                          N_TRIALS_NEAR, trial.number)
        return comp

    study = optuna.create_study(
        direction="maximize",
        sampler=TPESampler(seed=42, n_startup_trials=N_STARTUP_NEAR),
        study_name="near_term",
    )
    study.optimize(objective, n_trials=N_TRIALS_NEAR)
    return all_results


def _find_sunrise_for_date(observer, sun_body, ts, year, month, day):
    """Find sunrise JD and dawn duration for one specific date."""
    t0 = ts.utc(year, month, day, 0)
    t1 = ts.utc(year, month, day, 12)
    try:
        t_rise, y_rise = almanac.find_risings(observer, sun_body, t0, t1)
        if not y_rise.any():
            return None, None
        sunrise_jd = t_rise.tt[y_rise][0]

        t_dawn, y_dawn = almanac.find_risings(
            observer, sun_body, t0, t1, horizon_degrees=-18
        )
        if y_dawn.any():
            dawn_jd = t_dawn.tt[y_dawn][0]
            dawn_dur = (sunrise_jd - dawn_jd) * 86400.0
        else:
            dawn_dur = DAWN_WINDOW_SEC
        return sunrise_jd, max(dawn_dur, 600.0)
    except Exception:
        return None, None


def run_deep_time(observer, sun_body, regulus, ts):
    """
    Study B: mirror-log year search across the full precession window.

    3D search: (t_year, day_of_year, offset_from_sunrise).
    t_year in [0, 2] maps via mirror_log_year():
      - Segment 1 (0→1): log-dense near 2026, reaching peak redness ~4244 CE
      - Segment 2 (1→2): log-dense near 4244, reaching 6500 CE
    Concentrates trials around "now" and around peak redness.
    Per-trial sunrise lookup — no bulk almanac needed.
    """
    print(f"STUDY B — DEEP TIME (mirror-log {NEAR_TERM_START}–{END_YEAR} CE)")
    print(f"  Peak redness target: ~{PEAK_REDNESS_YEAR} CE")
    print(f"  Segment 1: {NEAR_TERM_START}→{PEAK_REDNESS_YEAR} (log-dense near {NEAR_TERM_START})")
    print(f"  Segment 2: {PEAK_REDNESS_YEAR}→{END_YEAR} (log-dense near {PEAK_REDNESS_YEAR})")
    print(f"  3D search: (t_year, day_of_year, offset_from_sunrise)")
    print(f"  {N_TRIALS_DEEP:,} trials (TPE, {N_STARTUP_DEEP} startup)")
    print()

    best_composite = [0.0]
    all_results = []

    def objective(trial):
        t_year = trial.suggest_float("t_year", 0.0, 2.0)
        year = mirror_log_year(t_year)
        year = max(NEAR_TERM_START, min(year, END_YEAR))

        doy = trial.suggest_int("day_of_year", 1, 365)

        sunrise_jd, dawn_dur = _find_sunrise_for_date(
            observer, sun_body, ts, year, 1, doy
        )
        if sunrise_jd is None:
            return 0.0

        before = dawn_dur * 2.0
        after = 15.0 * 60.0
        offset_sec = trial.suggest_float("offset_sec", -before, after)

        jd = sunrise_jd + offset_sec / 86400.0
        result = evaluate_moment(jd, observer, sun_body, regulus, ts)
        if result is None:
            return 0.0

        result["offset_sec"] = offset_sec
        result["target_year"] = year
        comp = result["composite"]
        all_results.append(result)
        _log_trial_result(result, offset_sec, comp, best_composite,
                          N_TRIALS_DEEP, trial.number)
        return comp

    study = optuna.create_study(
        direction="maximize",
        sampler=TPESampler(seed=42, n_startup_trials=N_STARTUP_DEEP),
        study_name="deep_time",
    )
    study.optimize(objective, n_trials=N_TRIALS_DEEP)
    return all_results


PROXIMITY_HALFLIFE_YRS = 100.0  # year-distance weighting half-life


def _proximity_weight(year):
    """Exponential decay weight based on years from now. Halflife = 100 yr."""
    dt = abs(year - NEAR_TERM_START)
    return 0.5 ** (dt / PROXIMITY_HALFLIFE_YRS)


def _deduplicate_by_day(results, top_n):
    """Return up to top_n results, one per unique calendar day."""
    seen = set()
    unique = []
    for r in results:
        key = (r["year"], r["month"], r["day"])
        if key not in seen:
            seen.add(key)
            unique.append(r)
        if len(unique) >= top_n:
            break
    return unique


def report_results(all_results, label, top_n=TOP_N_REPORT):
    """Print results for one study: raw top scores + proximity-weighted."""
    if not all_results:
        print(f"\n  No valid results for {label}.\n")
        return []

    print()
    print("=" * 70)
    print(f"TOP {top_n} RESULTS — {label} (raw prophecy score)")
    print("=" * 70)
    print()
    print("Scoring: prophecy = redness × imminence × visibility × az_prox")
    print()

    all_results.sort(key=lambda r: r["composite"], reverse=True)
    unique_raw = _deduplicate_by_day(all_results, top_n)

    for rank, r in enumerate(unique_raw, 1):
        print_result_detail(r, rank)

    print("=" * 70)
    print(f"RAW TOP {len(unique_raw)} — TABLE-FRIENDLY ROWS")
    print("=" * 70)
    print("  rank | date | time_utc | prophecy | red | imm | vis | az | reg_alt | reg_az | sun_alt | bv | vmag | twilight | airmass | offset_min")
    for rank, r in enumerate(unique_raw, 1):
        sec = r.get("second", 0.0)
        offset_min = r.get("offset_sec", 0.0) / 60.0
        print(
            f"  {rank} | {r['year']}-{r['month']:02d}-{r['day']:02d} | "
            f"{r['hour']:02d}:{r['minute']:02d}:{sec:04.1f} | "
            f"{r['composite']:.6f} | {r['redness']:.4f} | {r['imminence']:.4f} | "
            f"{r['visibility']:.4f} | {r['az_score']:.4f} | {r['reg_alt']:.2f} | "
            f"{r['reg_az']:.2f} | {r['sun_alt']:.2f} | {format_bv_label(r['bv_obs'])} | "
            f"{r['v_mag']:.2f} | {r['twilight']} | {r['airmass']:.2f} | {offset_min:+.1f}"
        )
    print()

    # --- Proximity-weighted ranking ---
    print()
    print("=" * 70)
    print(f"TOP {top_n} RESULTS — {label} (weighted by proximity to {NEAR_TERM_START})")
    print("=" * 70)
    print()
    print(f"  proximity_weighted = prophecy_score × 0.5^(years_from_now / {PROXIMITY_HALFLIFE_YRS:.0f})")
    print()

    for r in all_results:
        r["prox_weighted"] = r["composite"] * _proximity_weight(r["year"])

    by_prox = sorted(all_results, key=lambda r: r["prox_weighted"], reverse=True)
    unique_prox = _deduplicate_by_day(by_prox, top_n)

    for rank, r in enumerate(unique_prox, 1):
        pw = r["prox_weighted"]
        yrs = r["year"] - NEAR_TERM_START
        sec = r.get("second", 0)
        print(f"  #{rank:>2d}  {r['year']}-{r['month']:02d}-{r['day']:02d}"
              f"  {r['hour']:02d}:{r['minute']:02d}:{sec:04.1f} UTC"
              f"  prophecy={r['composite']:.6f}"
              f"  ×{_proximity_weight(r['year']):.4f}"
              f"  → weighted={pw:.6f}"
              f"  (+{yrs:,} yr)"
              f"  B-V={format_bv_label(r['bv_obs'])}"
              f"  RegAlt={r['reg_alt']:.2f}°"
              f"  SunAlt={r['sun_alt']:.2f}°"
              f"  Az={r['reg_az']:.2f}°")

    print("=" * 70)
    print(f"WEIGHTED TOP {len(unique_prox)} — TABLE-FRIENDLY ROWS")
    print("=" * 70)
    print("  rank | date | time_utc | weighted | prophecy | weight | years_from_now | red | imm | vis | az | reg_alt | reg_az | sun_alt | bv | twilight")
    for rank, r in enumerate(unique_prox, 1):
        sec = r.get("second", 0.0)
        weight = _proximity_weight(r["year"])
        years_from_now = r["year"] - NEAR_TERM_START
        print(
            f"  {rank} | {r['year']}-{r['month']:02d}-{r['day']:02d} | "
            f"{r['hour']:02d}:{r['minute']:02d}:{sec:04.1f} | "
            f"{r['prox_weighted']:.6f} | {r['composite']:.6f} | {weight:.4f} | "
            f"{years_from_now:+d} | {r['redness']:.4f} | {r['imminence']:.4f} | "
            f"{r['visibility']:.4f} | {r['az_score']:.4f} | {r['reg_alt']:.2f} | "
            f"{r['reg_az']:.2f} | {r['sun_alt']:.2f} | {format_bv_label(r['bv_obs'])} | {r['twilight']}"
        )
    print()

    # --- Summary ---
    scores = np.array([r["composite"] for r in all_results])
    print()
    print("=" * 70)
    print(f"SUMMARY — {label}")
    print("=" * 70)
    print()
    print(f"  Trials evaluated:    {len(all_results):,}")
    print(f"  Peak prophecy score: {scores.max():.6f}")
    print(f"  Median score:        {np.median(scores):.6f}")
    print()

    if unique_raw:
        best = unique_raw[0]
        print(f"  Best (raw):  {best['year']}-{best['month']:02d}-{best['day']:02d}"
              f"  prophecy={best['composite']:.6f}")
    if unique_prox:
        best_p = unique_prox[0]
        print(f"  Best (prox): {best_p['year']}-{best_p['month']:02d}-{best_p['day']:02d}"
              f"  weighted={best_p['prox_weighted']:.6f}"
              f"  (+{best_p['year'] - NEAR_TERM_START:,} yr)")
    print()

    print("  Seasonal distribution of top raw scores:")
    month_counts = {}
    for r in unique_raw:
        m = r["month"]
        month_counts[m] = month_counts.get(m, 0) + 1
    month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for m in sorted(month_counts):
        bar = "█" * month_counts[m]
        print(f"    {month_names[m]:>3s}: {bar} ({month_counts[m]})")
    print()

    return unique_raw


def main():
    print("=" * 70)
    print("REGULUS-SPHINX ALMANAC-BASED OPTUNA OPTIMIZER")
    print("=" * 70)
    print()
    print('Prophecy: "When the red star of Regulus aligns just before dawn')
    print('           in the gaze of the Sphinx."')
    print()
    print("Two searches:")
    print(f"  A) Near-term:  {NEAR_TERM_START}–{NEAR_TERM_END} CE"
          f"  ({N_TRIALS_NEAR:,} trials, almanac-based)")
    print(f"  B) Deep time:  {NEAR_TERM_START}–{END_YEAR} CE"
          f"  ({N_TRIALS_DEEP:,} trials, mirror-log year sampling,"
          f" dense near {NEAR_TERM_START} & {PEAK_REDNESS_YEAR})")
    print()
    print("Scoring: prophecy = redness × imminence × visibility × az_prox")
    print(f"  redness:    precession → altitude → airmass → B-V color shift")
    print(f"  imminence:  sun angle below horizon (closer to rising → higher)")
    print(f"  visibility: star contrast vs sky (atmosphere dims star + sky brightens)")
    print(f"  az_prox:    Gaussian, center={SPHINX_AZIMUTH}°, sigma={DEFAULT_AZ_SIGMA}°")
    print(f"  Year-proximity weighting: halflife = {PROXIMITY_HALFLIFE_YRS:.0f} yr")
    print()

    # --- Load ephemeris ---
    print("Loading ephemeris ...")
    eph, ts, earth, sun_body, regulus, giza = setup()
    observer = earth + giza
    print("Ephemeris loaded.")
    print()

    # --- Study A: Near-term (almanac-based) ---
    print("=" * 70)
    print(f"ALMANAC: Computing sunrise + dawn ({NEAR_TERM_START}–{NEAR_TERM_END})")
    print("=" * 70)
    print()

    alm = compute_almanac(observer, sun_body, ts, NEAR_TERM_START, NEAR_TERM_END)
    print()

    print("=" * 70)
    near_results = run_near_term(alm, observer, sun_body, regulus, ts)
    near_unique = report_results(
        near_results,
        label=f"NEAR-TERM ({NEAR_TERM_START}–{NEAR_TERM_END})",
        top_n=10,
    )

    # --- Study B: Deep time (log-space year) ---
    print("=" * 70)
    deep_results = run_deep_time(observer, sun_body, regulus, ts)
    deep_unique = report_results(
        deep_results,
        label=f"DEEP TIME ({NEAR_TERM_START}–{END_YEAR}, mirror-log)",
        top_n=TOP_N_REPORT,
    )

    # --- Side-by-side comparison ---
    print("=" * 70)
    print("COMPARISON: NEAR-TERM vs DEEP TIME")
    print("=" * 70)
    print()
    if near_unique:
        nb = near_unique[0]
        print(f"  Near-term best: {nb['year']}-{nb['month']:02d}-{nb['day']:02d}"
              f"  prophecy={nb['composite']:.6f}"
              f"  red={nb['redness']:.3f} imm={nb['imminence']:.3f}"
              f"  vis={nb['visibility']:.3f} az={nb['az_score']:.3f}")
    if deep_unique:
        fb = deep_unique[0]
        print(f"  Deep-time best: {fb['year']}-{fb['month']:02d}-{fb['day']:02d}"
              f"  prophecy={fb['composite']:.6f}"
              f"  red={fb['redness']:.3f} imm={fb['imminence']:.3f}"
              f"  vis={fb['visibility']:.3f} az={fb['az_score']:.3f}")
    if near_unique and deep_unique:
        delta = deep_unique[0]["composite"] - near_unique[0]["composite"]
        print(f"  Improvement:    {delta:+.6f}")
    print()

    # --- Plot (deep time results) ---
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        all_for_plot = deep_results

        dates_dec = [r["year"] + (r["month"] - 1) / 12 + r["day"] / 365
                     for r in all_for_plot]
        comps = [r["composite"] for r in all_for_plot]

        ax = axes[0][0]
        ax.scatter(dates_dec, comps, c="steelblue", s=3, alpha=0.4)
        if deep_unique:
            best = deep_unique[0]
            bx = best["year"] + (best["month"] - 1) / 12 + best["day"] / 365
            ax.scatter([bx], [best["composite"]], c="gold", s=80,
                       edgecolors="black", zorder=5, label="Best")
        ax.set_xlabel("Year CE")
        ax.set_ylabel("Prophecy Score")
        ax.set_title(f"Deep-Time Trials ({NEAR_TERM_START}–{END_YEAR}, mirror-log)")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        ax = axes[0][1]
        offsets_min = [r.get("offset_sec", 0) / 60 for r in all_for_plot]
        ax.scatter(offsets_min, comps, c="orange", s=3, alpha=0.4)
        ax.set_xlabel("Offset from Sunrise (min)")
        ax.set_ylabel("Prophecy Score")
        ax.set_title("Score vs Time Offset")
        ax.grid(True, alpha=0.3)

        ax = axes[1][0]
        reg_azs = [r["reg_az"] for r in all_for_plot]
        sc = ax.scatter(reg_azs, [r["reg_alt"] for r in all_for_plot],
                        c=comps, cmap="viridis", s=3, alpha=0.5)
        ax.axvline(x=90, color="red", ls="--", lw=0.8, label="Sphinx gaze (90°)")
        ax.set_xlabel("Regulus Azimuth (°)")
        ax.set_ylabel("Regulus Altitude (°)")
        ax.set_title("Regulus Position (color = prophecy score)")
        ax.legend(fontsize=8)
        plt.colorbar(sc, ax=ax, label="Prophecy Score")
        ax.grid(True, alpha=0.3)

        ax = axes[1][1]
        sun_alts = [r["sun_alt"] for r in all_for_plot]
        ax.scatter(sun_alts, comps, c="coral", s=3, alpha=0.4)
        ax.axvline(x=-18, color="blue", ls="--", lw=0.8,
                   label="Astro dawn (−18°)")
        ax.set_xlabel("Sun Altitude (°)")
        ax.set_ylabel("Prophecy Score")
        ax.set_title("Score vs Sun Altitude (imminence)")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        plt.suptitle("Regulus-Sphinx Prophecy: Near-term + Deep-time Search",
                      fontsize=13, fontweight="bold")
        plt.tight_layout()
        plot_path = str(Path(__file__).parent / "regulus_optuna_results.png")
        plt.savefig(plot_path, dpi=150)
        print(f"Plot saved to: {plot_path}")
        plt.close()

    except ImportError:
        print("matplotlib not available, skipping plot.")

    print("\nDone.")


if __name__ == "__main__":
    main()
