#!/usr/bin/env python3
"""
Regulus-Sphinx Sequential Morning-Arc Optimizer
===============================================
Alternative interpretation of the prophecy as a pre-dawn sequence:

  Stage A (early): Regulus is low/reddened and still visible.
  Stage B (later): Regulus reaches azimuth ~90° (Sphinx gaze) before sunrise.

This differs from the single-moment model by allowing the "red sign" and
the "alignment" to occur at different times within one morning episode.
"""

import warnings
import numpy as np
from pathlib import Path
import time

import optuna
from optuna.samplers import TPESampler
from skyfield import almanac
from skyfield.api import wgs84, N, E

from regulus_upcoming_alignment import (
    setup,
    observed_bv,
    observed_vmag,
    airmass_kasten_young,
    bv_to_color_name,
    twilight_phase,
    imminence_score,
    redness_score,
    visibility_score,
    az_proximity_score,
    GIZA_LAT,
    GIZA_LON,
    SPHINX_AZIMUTH,
)

warnings.filterwarnings("ignore", category=FutureWarning)
optuna.logging.set_verbosity(optuna.logging.WARNING)

NEAR_TERM_START = 2026
NEAR_TERM_END = 2031
END_YEAR = 6500
PEAK_REDNESS_YEAR = 4244

N_TRIALS_DEEP = 10000
N_STARTUP_DEEP = 500
TOP_N_REPORT = 20

SAMPLES_PER_MORNING = 240

_SEG1_SPAN = PEAK_REDNESS_YEAR - NEAR_TERM_START
_SEG2_SPAN = END_YEAR - PEAK_REDNESS_YEAR
_LOG_SEG1 = np.log10(_SEG1_SPAN)
_LOG_SEG2 = np.log10(_SEG2_SPAN)


def mirror_log_year(t):
    """Map t in [0,2] to [2026,6500] with density near 2026 and 4244."""
    if t < 1.0:
        offset = 10 ** (t * _LOG_SEG1)
        return NEAR_TERM_START + int(round(offset))
    offset = 10 ** ((t - 1.0) * _LOG_SEG2)
    return PEAK_REDNESS_YEAR + int(round(offset))


def _redness_strength_from_bv(bv):
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


def _format_bv_label(bv):
    return f"{bv:+.2f} ({bv_to_color_name(bv)}, {_redness_strength_from_bv(bv)})"


def _find_sunrise_and_dawn(observer, sun_body, ts, year, month, day):
    """Return (sunrise_jd, dawn_start_jd) for one date; None if unavailable."""
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
        else:
            dawn_jd = sunrise_jd - (90.0 * 60.0 / 86400.0)
        return sunrise_jd, dawn_jd
    except Exception:
        return None, None


def evaluate_morning_episode(year, month, day, observer, sun_body, regulus, ts):
    """
    Score one pre-dawn morning as a sequence:
      stageA_score = max(redness * visibility) before Stage B
      stageB_score = max(az_proximity * imminence * visibility) before sunrise
      sequence_score = stageA_score * stageB_score
    """
    result = {
        "year": int(year),
        "month": int(month),
        "day": int(day),
        "valid": False,
        "status": "unknown",
        "stage_a_any_score": 0.0,
        "stage_b_any_score": 0.0,
        "partial_score": 0.0,
    }

    sunrise_jd, dawn_jd = _find_sunrise_and_dawn(
        observer, sun_body, ts, year, month, day
    )
    if sunrise_jd is None:
        result["status"] = "no_sunrise_or_dawn"
        return result
    if dawn_jd >= sunrise_jd:
        result["status"] = "bad_dawn_window"
        return result

    jds = np.linspace(dawn_jd, sunrise_jd, SAMPLES_PER_MORNING)
    times = ts.tt_jd(jds)

    reg_app = observer.at(times).observe(regulus).apparent()
    reg_alt_obj, reg_az_obj, _ = reg_app.altaz()
    reg_alts = reg_alt_obj.degrees
    reg_azs = reg_az_obj.degrees

    sun_app = observer.at(times).observe(sun_body).apparent()
    sun_alt_obj, _, _ = sun_app.altaz()
    sun_alts = sun_alt_obj.degrees

    valid = (reg_alts >= -2.0) & (sun_alts < 0.0)
    if not np.any(valid):
        result["status"] = "no_predawn_samples"
        return result

    reds = np.array([redness_score(float(a)) for a in reg_alts])
    v_mags = np.array([observed_vmag(float(a)) for a in reg_alts])
    vis = np.array(
        [visibility_score(float(v), float(s)) for v, s in zip(v_mags, sun_alts)]
    )
    imm = np.array([imminence_score(float(s)) for s in sun_alts])
    az = np.array([az_proximity_score(float(a)) for a in reg_azs])
    stage_a_any_metric = reds * vis
    stage_a_any_metric = np.where(valid, stage_a_any_metric, -1.0)
    stage_b_any_metric = az * imm * vis
    stage_b_any_metric = np.where(valid, stage_b_any_metric, -1.0)

    idx_a_any = int(np.argmax(stage_a_any_metric))
    idx_b_any = int(np.argmax(stage_b_any_metric))
    result["stage_a_any_score"] = float(max(stage_a_any_metric[idx_a_any], 0.0))
    result["stage_b_any_score"] = float(max(stage_b_any_metric[idx_b_any], 0.0))
    result["partial_score"] = (
        result["stage_a_any_score"] * result["stage_b_any_score"]
    )

    if stage_a_any_metric[idx_a_any] > 0:
        t_a_any = ts.tt_jd(jds[idx_a_any])
        cal_a_any = t_a_any.tt_calendar()
        result["stage_a_any_hour"] = int(cal_a_any[3])
        result["stage_a_any_minute"] = int(cal_a_any[4])
        result["stage_a_any_second"] = float(cal_a_any[5])
        result["stage_a_any_reg_alt"] = float(reg_alts[idx_a_any])
        result["stage_a_any_reg_az"] = float(reg_azs[idx_a_any])
        result["stage_a_any_sun_alt"] = float(sun_alts[idx_a_any])
        result["stage_a_any_bv"] = float(observed_bv(float(reg_alts[idx_a_any])))

    if stage_b_any_metric[idx_b_any] > 0:
        t_b_any = ts.tt_jd(jds[idx_b_any])
        cal_b_any = t_b_any.tt_calendar()
        result["stage_b_any_hour"] = int(cal_b_any[3])
        result["stage_b_any_minute"] = int(cal_b_any[4])
        result["stage_b_any_second"] = float(cal_b_any[5])
        result["stage_b_any_reg_alt"] = float(reg_alts[idx_b_any])
        result["stage_b_any_reg_az"] = float(reg_azs[idx_b_any])
        result["stage_b_any_sun_alt"] = float(sun_alts[idx_b_any])
        result["stage_b_any_az"] = float(az[idx_b_any])
        result["stage_b_any_imminence"] = float(imm[idx_b_any])
        result["stage_b_any_visibility"] = float(vis[idx_b_any])
        result["stage_b_any_bv"] = float(observed_bv(float(reg_alts[idx_b_any])))

    # Stage B: later event in the Sphinx gaze before sunrise.
    stage_b_metric = az * imm * vis
    stage_b_metric = np.where(valid, stage_b_metric, -1.0)
    idx_b = int(np.argmax(stage_b_metric))
    if stage_b_metric[idx_b] <= 0:
        result["status"] = "no_stage_b"
        return result

    # Stage A: earlier red+visible moment identifying Regulus.
    earlier = np.arange(len(jds)) < idx_b
    stage_a_valid = valid & earlier
    if not np.any(stage_a_valid):
        result["status"] = "no_earlier_samples_before_stage_b"
        return result

    stage_a_metric = reds * vis
    stage_a_metric = np.where(stage_a_valid, stage_a_metric, -1.0)
    idx_a = int(np.argmax(stage_a_metric))
    if stage_a_metric[idx_a] <= 0:
        result["status"] = "no_stage_a_before_stage_b"
        return result

    t_a = ts.tt_jd(jds[idx_a])
    t_b = ts.tt_jd(jds[idx_b])
    cal_a = t_a.tt_calendar()
    cal_b = t_b.tt_calendar()

    stage_a_score = float(stage_a_metric[idx_a])
    stage_b_score = float(stage_b_metric[idx_b])
    sequence_score = stage_a_score * stage_b_score

    return {
        "year": int(cal_b[0]),
        "month": int(cal_b[1]),
        "day": int(cal_b[2]),
        "valid": True,
        "status": "valid_sequence",
        "stage_a_hour": int(cal_a[3]),
        "stage_a_minute": int(cal_a[4]),
        "stage_a_second": float(cal_a[5]),
        "stage_b_hour": int(cal_b[3]),
        "stage_b_minute": int(cal_b[4]),
        "stage_b_second": float(cal_b[5]),
        "stage_a_jd": float(jds[idx_a]),
        "stage_b_jd": float(jds[idx_b]),
        "stage_a_score": stage_a_score,
        "stage_b_score": stage_b_score,
        "sequence_score": sequence_score,
        "stage_a_redness": float(reds[idx_a]),
        "stage_a_visibility": float(vis[idx_a]),
        "stage_a_reg_alt": float(reg_alts[idx_a]),
        "stage_a_reg_az": float(reg_azs[idx_a]),
        "stage_a_sun_alt": float(sun_alts[idx_a]),
        "stage_a_bv": float(observed_bv(float(reg_alts[idx_a]))),
        "stage_a_vmag": float(v_mags[idx_a]),
        "stage_b_az": float(az[idx_b]),
        "stage_b_imminence": float(imm[idx_b]),
        "stage_b_visibility": float(vis[idx_b]),
        "stage_b_reg_alt": float(reg_alts[idx_b]),
        "stage_b_reg_az": float(reg_azs[idx_b]),
        "stage_b_sun_alt": float(sun_alts[idx_b]),
        "stage_b_bv": float(observed_bv(float(reg_alts[idx_b]))),
        "stage_b_vmag": float(v_mags[idx_b]),
        "stage_b_airmass": float(airmass_kasten_young(float(reg_alts[idx_b]))),
        "stage_b_twilight": twilight_phase(float(sun_alts[idx_b])),
        "stage_b_color_name": bv_to_color_name(float(observed_bv(float(reg_alts[idx_b])))),
        "delta_minutes": float((jds[idx_b] - jds[idx_a]) * 1440.0),
    }


def _deduplicate_by_day(results, top_n):
    seen = set()
    out = []
    for r in results:
        key = (r["year"], r["month"], r["day"])
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
        if len(out) >= top_n:
            break
    return out


def print_episode_result(r, rank=None):
    pfx = f"  #{rank}" if rank else "  "
    print(f"{'-'*72}")
    print(
        f"{pfx}  {r['year']}-{r['month']:02d}-{r['day']:02d}"
        f"  A:{r['stage_a_hour']:02d}:{r['stage_a_minute']:02d}:{r['stage_a_second']:04.1f}"
        f"  → B:{r['stage_b_hour']:02d}:{r['stage_b_minute']:02d}:{r['stage_b_second']:04.1f} UTC"
    )
    print(f"{'-'*72}")
    print(
        f"  Sequence score: {r['sequence_score']:.6f}"
        f"  (stageA {r['stage_a_score']:.6f} × stageB {r['stage_b_score']:.6f})"
    )
    print(
        f"    Stage A (red/visible): red={r['stage_a_redness']:.4f}"
        f" vis={r['stage_a_visibility']:.4f}"
        f" alt={r['stage_a_reg_alt']:.2f}° az={r['stage_a_reg_az']:.2f}°"
        f" sun={r['stage_a_sun_alt']:.2f}°"
        f" B-V={_format_bv_label(r['stage_a_bv'])}"
    )
    print(
        f"    Stage B (az~90 later): az={r['stage_b_az']:.4f}"
        f" imm={r['stage_b_imminence']:.4f}"
        f" vis={r['stage_b_visibility']:.4f}"
        f" alt={r['stage_b_reg_alt']:.2f}° az={r['stage_b_reg_az']:.2f}°"
        f" sun={r['stage_b_sun_alt']:.2f}° ({r['stage_b_twilight']})"
        f" B-V={_format_bv_label(r['stage_b_bv'])}"
    )
    print(
        f"  Stage separation: {r['delta_minutes']:.1f} min"
        f"  | Sphinx az={SPHINX_AZIMUTH:.1f}°"
    )
    print()


def run_near_term_scan(observer, sun_body, regulus, ts):
    """Exhaustive daily scan for the near-term interval."""
    print(f"NEAR-TERM DAILY SCAN ({NEAR_TERM_START}-{NEAR_TERM_END})")
    print("  Deterministic date-by-date episode scoring")
    print()

    results = []
    total_days = 0
    total_target_days = sum(
        366 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 365
        for y in range(NEAR_TERM_START, NEAR_TERM_END + 1)
    )
    start = time.time()
    next_log = 50
    reason_counts = {}
    best_partial = None
    for year in range(NEAR_TERM_START, NEAR_TERM_END + 1):
        for doy in range(1, 366):
            total_days += 1
            t = ts.utc(year, 1, doy)
            cal = t.tt_calendar()
            m = int(cal[1])
            d = int(cal[2])
            r = evaluate_morning_episode(year, m, d, observer, sun_body, regulus, ts)
            if r["valid"]:
                results.append(r)
            else:
                reason = r.get("status", "unknown")
                reason_counts[reason] = reason_counts.get(reason, 0) + 1
                if best_partial is None or r["partial_score"] > best_partial["partial_score"]:
                    best_partial = r

            if total_days >= next_log or total_days == total_target_days:
                elapsed = time.time() - start
                rate = total_days / max(elapsed, 1e-9)
                remaining = max(total_target_days - total_days, 0)
                eta = remaining / max(rate, 1e-9)
                print(
                    f"  Progress: {total_days:,}/{total_target_days:,} days"
                    f"  ({100.0 * total_days / total_target_days:5.1f}%)"
                    f"  valid={len(results):,}"
                    f"  elapsed={elapsed:5.1f}s  eta={eta:5.1f}s"
                )
                if best_partial is not None:
                    stage_a_any_bv = best_partial.get("stage_a_any_bv")
                    stage_b_any_bv = best_partial.get("stage_b_any_bv")
                    a_any_label = (
                        _format_bv_label(stage_a_any_bv)
                        if stage_a_any_bv is not None else "n/a"
                    )
                    b_any_label = (
                        _format_bv_label(stage_b_any_bv)
                        if stage_b_any_bv is not None else "n/a"
                    )
                    print(
                        f"    best partial (invalid): {best_partial['year']}-{best_partial['month']:02d}-{best_partial['day']:02d}"
                        f"  partial={best_partial['partial_score']:.6f}"
                        f"  stageA_any={best_partial['stage_a_any_score']:.6f}"
                        f"  stageB_any={best_partial['stage_b_any_score']:.6f}"
                        f"  status={best_partial['status']}"
                        f"  A_B-V={a_any_label}"
                        f"  B_B-V={b_any_label}"
                    )
                if reason_counts:
                    top_reason, top_count = max(reason_counts.items(), key=lambda x: x[1])
                    print(f"    top invalid reason so far: {top_reason} ({top_count})")
                next_log += 50

    print(f"  Days scanned: {total_days:,}")
    print(f"  Valid morning episodes: {len(results):,}")
    if best_partial is not None:
        stage_a_any_bv = best_partial.get("stage_a_any_bv")
        stage_b_any_bv = best_partial.get("stage_b_any_bv")
        a_any_label = (
            _format_bv_label(stage_a_any_bv)
            if stage_a_any_bv is not None else "n/a"
        )
        b_any_label = (
            _format_bv_label(stage_b_any_bv)
            if stage_b_any_bv is not None else "n/a"
        )
        print(
            f"  Best partial invalid day: {best_partial['year']}-{best_partial['month']:02d}-{best_partial['day']:02d}"
            f"  partial={best_partial['partial_score']:.6f}"
            f"  stageA_any={best_partial['stage_a_any_score']:.6f}"
            f"  stageB_any={best_partial['stage_b_any_score']:.6f}"
            f"  status={best_partial['status']}"
            f"  A_B-V={a_any_label}"
            f"  B_B-V={b_any_label}"
        )
    if reason_counts:
        print("  Invalid-day reasons:")
        for reason, count in sorted(reason_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"    {reason:<34} {count:>6d}")
    print()
    return results


def run_deep_time_optuna(observer, sun_body, regulus, ts):
    """
    Deep-time date search with mirror-log year sampling.
    Objective: maximize sequence_score(year, day_of_year).
    """
    print(f"DEEP-TIME OPTUNA ({NEAR_TERM_START}-{END_YEAR}, mirror-log year)")
    print(f"  Trials: {N_TRIALS_DEEP:,} (startup {N_STARTUP_DEEP})")
    print("  Search dims: t_year, day_of_year")
    print()

    all_results = []
    best = [0.0]

    def objective(trial):
        t_year = trial.suggest_float("t_year", 0.0, 2.0)
        year = max(NEAR_TERM_START, min(mirror_log_year(t_year), END_YEAR))
        doy = trial.suggest_int("day_of_year", 1, 365)

        t = ts.utc(year, 1, doy)
        cal = t.tt_calendar()
        month = int(cal[1])
        day = int(cal[2])

        r = evaluate_morning_episode(year, month, day, observer, sun_body, regulus, ts)
        if not r["valid"]:
            return 0.0

        all_results.append(r)
        score = r["sequence_score"]
        if score > best[0]:
            best[0] = score
            a_label = _format_bv_label(r["stage_a_bv"])
            b_label = _format_bv_label(r["stage_b_bv"])
            print(
                f"  Trial {trial.number:>5d} ★ NEW BEST"
                f"  {r['year']}-{r['month']:02d}-{r['day']:02d}"
                f"  score={score:.6f}"
                f"  A(alt {r['stage_a_reg_alt']:.1f}°, B-V {a_label})"
                f" -> B(az {r['stage_b_reg_az']:.2f}°, sun {r['stage_b_sun_alt']:.1f}°, B-V {b_label})"
            )
        elif trial.number < 5 or (trial.number < 100 and trial.number % 20 == 0) or trial.number % 200 == 0:
            print(f"  Trial {trial.number:>5d}  best={best[0]:.6f}")
        return score

    study = optuna.create_study(
        direction="maximize",
        sampler=TPESampler(seed=42, n_startup_trials=N_STARTUP_DEEP),
        study_name="deep_time_sequential",
    )
    study.optimize(objective, n_trials=N_TRIALS_DEEP)
    return all_results


def report_results(results, label, top_n=TOP_N_REPORT):
    if not results:
        print(f"\nNo valid results for {label}.\n")
        return []

    results.sort(key=lambda r: r["sequence_score"], reverse=True)
    unique = _deduplicate_by_day(results, top_n)

    print()
    print("=" * 72)
    print(f"TOP {len(unique)} — {label}")
    print("=" * 72)
    print()
    print("Scoring: sequence = [max early(redness*visibility)] × [max later(az*imminence*visibility)]")
    print()
    for i, r in enumerate(unique, 1):
        print_episode_result(r, i)

    scores = np.array([r["sequence_score"] for r in results], dtype=float)
    print("=" * 72)
    print(f"SUMMARY — {label}")
    print("=" * 72)
    print(f"  Valid episodes: {len(results):,}")
    print(f"  Peak score:     {scores.max():.6f}")
    print(f"  Median score:   {np.median(scores):.6f}")
    print()
    return unique


def main():
    print("=" * 72)
    print("REGULUS-SPHINX SEQUENTIAL MORNING-ARC OPTIMIZER")
    print("=" * 72)
    print()
    print('Alternative reading: "red Regulus appears first, then reaches the Sphinx gaze"')
    print("within one pre-dawn morning episode.")
    print()

    print("Loading ephemeris ...")
    eph, ts, earth, sun_body, regulus, giza = setup()
    observer = earth + giza
    print("Ephemeris loaded.")
    print(f"Observer: {GIZA_LAT:.4f}N, {GIZA_LON:.4f}E")
    print(f"Sphinx gaze azimuth: {SPHINX_AZIMUTH:.1f}°")
    print()

    near = run_near_term_scan(observer, sun_body, regulus, ts)
    near_top = report_results(near, f"NEAR-TERM ({NEAR_TERM_START}-{NEAR_TERM_END})", top_n=10)

    deep = run_deep_time_optuna(observer, sun_body, regulus, ts)
    deep_top = report_results(deep, f"DEEP-TIME ({NEAR_TERM_START}-{END_YEAR}, mirror-log)")

    print("=" * 72)
    print("COMPARISON")
    print("=" * 72)
    if near_top:
        n = near_top[0]
        print(
            f"  Near-term best: {n['year']}-{n['month']:02d}-{n['day']:02d}"
            f"  score={n['sequence_score']:.6f}"
            f"  Δt={n['delta_minutes']:.1f} min"
        )
    if deep_top:
        d = deep_top[0]
        print(
            f"  Deep-time best: {d['year']}-{d['month']:02d}-{d['day']:02d}"
            f"  score={d['sequence_score']:.6f}"
            f"  Δt={d['delta_minutes']:.1f} min"
        )
    print()

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        plot_data = deep if deep else near
        if plot_data:
            years = [r["year"] + (r["month"] - 1) / 12.0 + r["day"] / 365.0 for r in plot_data]
            seq = [r["sequence_score"] for r in plot_data]
            sep = [r["delta_minutes"] for r in plot_data]
            a_bv = [r["stage_a_bv"] for r in plot_data]
            b_az = [r["stage_b_reg_az"] for r in plot_data]

            ax = axes[0][0]
            ax.scatter(years, seq, s=3, alpha=0.4, c="steelblue")
            ax.set_title("Sequence Score vs Year")
            ax.set_xlabel("Year CE")
            ax.set_ylabel("Sequence Score")
            ax.grid(True, alpha=0.3)

            ax = axes[0][1]
            ax.scatter(a_bv, seq, s=3, alpha=0.4, c="firebrick")
            ax.set_title("Score vs Stage A Redness (B-V)")
            ax.set_xlabel("Stage A B-V")
            ax.set_ylabel("Sequence Score")
            ax.grid(True, alpha=0.3)

            ax = axes[1][0]
            ax.scatter(b_az, seq, s=3, alpha=0.4, c="darkgreen")
            ax.axvline(x=SPHINX_AZIMUTH, color="black", linestyle="--", linewidth=1)
            ax.set_title("Score vs Stage B Azimuth")
            ax.set_xlabel("Stage B Regulus Azimuth (deg)")
            ax.set_ylabel("Sequence Score")
            ax.grid(True, alpha=0.3)

            ax = axes[1][1]
            ax.scatter(sep, seq, s=3, alpha=0.4, c="purple")
            ax.set_title("Score vs Stage Separation")
            ax.set_xlabel("A->B Separation (minutes)")
            ax.set_ylabel("Sequence Score")
            ax.grid(True, alpha=0.3)

            plt.tight_layout()
            out = str(Path(__file__).parent / "regulus_optuna_sequential_results.png")
            plt.savefig(out, dpi=150)
            plt.close()
            print(f"Plot saved to: {out}")
    except ImportError:
        print("matplotlib not available, skipping plot.")

    print("\nDone.")


if __name__ == "__main__":
    main()
