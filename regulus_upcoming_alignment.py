#!/usr/bin/env python3
"""
Regulus-Sphinx Prophecy — Astronomical Scoring Library
======================================================
Scoring functions for the prophecy:

  "When the red star of Regulus aligns just before dawn
   in the gaze of the Sphinx."

Interpretation (repo author):
  - "Red star" = Regulus literally reddened by atmosphere near the horizon.
    Red = warning, same cultural root as "red sky at morning, sailor take
    warning."
  - "In the gaze of the Sphinx" = az=90° sightline. "On the horizon" =
    both literal (low altitude → redness) and symbolic (imminent).
  - "Just before dawn" = sun almost rising but not yet up. Maximum
    imminence of the warning.

Scoring model — four physical factors, product (no weights):
  - Redness    (precession):  atmospheric B-V color shift. Lower altitude
    → more airmass → redder. The warning sign.
  - Imminence  (angle):       how close the sun is to rising. Closer =
    more imminent. Based on SQM sky brightness model. The urgency.
  - Visibility (atmosphere):  how prominently the star stands out against
    the sky. Same airmass that reddens also dims; brighter sky reduces
    contrast. Creates natural tension with imminence.
  - Az prox    (alignment):   Gaussian on |Regulus az - 90°|.
  - Composite = redness × imminence × visibility × az_proximity.
    Product, not average — ALL conditions must be met simultaneously.
    The imminence-visibility tension creates a natural inflection point.

Atmospheric reddening model:
  Regulus is a B7V star (intrinsic B-V = -0.11, blue-white). Atmospheric
  extinction preferentially scatters blue light (Rayleigh, ~lambda^-4).
  At low altitudes the increased airmass shifts the observed B-V toward
  yellow, orange, and red.
  - k_B = 0.34 mag/airmass, k_V = 0.20 mag/airmass (Hardie 1962, AAVSO)
  - Observed B-V = intrinsic + 0.143 * airmass
  - At 10 deg altitude (X~5.6): B-V ~ +0.69 (yellow-orange)
  - At 5 deg altitude (X~10.4): B-V ~ +1.38 (orange-red)
  - At 2 deg altitude (X~20+):  B-V ~ +2.7  (deep red, very dim)

References:
  - Hipparcos Catalogue (ESA, 1997): Regulus astrometric data
  - Meeus, "Astronomical Algorithms" (1991): spherical astronomy
  - Hardie (1962), "Photoelectric Reductions": extinction coefficients
  - Kasten & Young (1989): airmass formula accurate at low altitudes
  - Lehner, "The Complete Pyramids" (1997): Sphinx dimensions
  - GPMP survey: Giza terrain elevations
  - hnsky.org/sqm_twilight: empirical SQM twilight model
"""

import numpy as np
from pathlib import Path

from skyfield.api import load, Star, wgs84, N, E


# --- Observer ---
GIZA_LAT = 29.9753
GIZA_LON = 31.1376
SPHINX_AZIMUTH = 90.0

SPHINX_TOTAL_HEIGHT = 20.22
SPHINX_EYE_FRACTION = 0.89
SPHINX_EYE_HEIGHT = SPHINX_TOTAL_HEIGHT * SPHINX_EYE_FRACTION
SPHINX_BASE_ELEVATION_ASL = 60.0
EASTERN_TERRAIN_ASL = 15.0
SPHINX_EYE_ASL = SPHINX_BASE_ELEVATION_ASL + SPHINX_EYE_HEIGHT
SPHINX_EYE_ABOVE_HORIZON = SPHINX_EYE_ASL - EASTERN_TERRAIN_ASL

# --- Regulus (HIP 49669) ---
REGULUS_RA_HOURS = (10, 8, 22.311)
REGULUS_DEC_DEG = (11, 58, 1.95)
REGULUS_PM_RA_MASYR = -248.73
REGULUS_PM_DEC_MASYR = 5.59
REGULUS_PARALLAX_MAS = 41.13
REGULUS_RV_KMSEC = 5.9
REGULUS_INTRINSIC_BV = -0.11   # B7V spectral type (Hipparcos)
REGULUS_APPARENT_MAG = 1.35

# --- Atmospheric extinction (sea-level, Hardie 1962 / AAVSO standard) ---
K_B = 0.34   # B-band extinction coefficient (mag/airmass)
K_V = 0.20   # V-band extinction coefficient (mag/airmass)

SCAN_YEARS = 50


def compute_horizon_dip(height_m):
    """Nautical Almanac dip formula including standard refraction (k~0.167)."""
    return 1.75 * np.sqrt(height_m) / 60.0


def airmass_kasten_young(altitude_deg):
    """
    Airmass using the Kasten & Young (1989) formula, accurate down to the
    horizon. Returns airmass X for a given true altitude in degrees.

    Reference: Kasten, F. & Young, A.T. (1989), Applied Optics 28, 4735
    """
    if altitude_deg <= 0:
        return 40.0  # practical cap near/below horizon
    alt_rad = np.radians(altitude_deg)
    z_deg = 90.0 - altitude_deg
    z_rad = np.radians(z_deg)
    denom = np.cos(z_rad) + 0.50572 * (96.07995 - z_deg) ** (-1.6364)
    return min(1.0 / denom, 40.0)


def observed_bv(altitude_deg):
    """
    Compute the observed B-V color index of Regulus at a given altitude,
    accounting for atmospheric reddening.

    (B-V)_obs = (B-V)_0 + (k_B - k_V - 0.03*(B-V)_0) * X
              = -0.11 + 0.143 * X   (for Regulus)

    Reference: Hardie (1962); AAVSO extinction standards
    """
    X = airmass_kasten_young(altitude_deg)
    delta_k = K_B - K_V - 0.03 * REGULUS_INTRINSIC_BV
    return REGULUS_INTRINSIC_BV + delta_k * X


def observed_vmag(altitude_deg):
    """Apparent V magnitude after atmospheric extinction."""
    X = airmass_kasten_young(altitude_deg)
    return REGULUS_APPARENT_MAG + K_V * X


def bv_to_color_name(bv):
    """Human-readable color name from B-V index."""
    if bv < 0.0:
        return "blue-white"
    elif bv < 0.3:
        return "white"
    elif bv < 0.6:
        return "yellow-white"
    elif bv < 0.9:
        return "yellow-orange"
    elif bv < 1.2:
        return "orange"
    elif bv < 1.5:
        return "orange-red"
    else:
        return "red"


def twilight_phase(sun_alt_deg):
    """Classify the twilight phase from Sun altitude."""
    if sun_alt_deg > 0:
        return "daytime"
    elif sun_alt_deg > -6:
        return "civil twilight"
    elif sun_alt_deg > -12:
        return "nautical twilight"
    elif sun_alt_deg > -18:
        return "astronomical twilight"
    else:
        return "night"


DEFAULT_AZ_SIGMA = 2.0

SQM_DARK = 21.7    # mag/arcsec² at astronomical darkness (Sun ≤ -18°)
SQM_SUNRISE = 6.75  # mag/arcsec² at Sun = 0°


def _zenith_sqm(sun_alt_deg):
    """
    Empirical zenith sky brightness (mag/arcsec²) vs Sun altitude.

    Two-piece fit from Sky Quality Meter observations:
      0° to -12°:  SQM = -1.057 × sun_alt + 6.7489  (linear)
      -12° to -18°: SQM = -0.0744 × sun_alt² - 2.5768 × sun_alt - 0.5845  (quadratic)

    Reference: hnsky.org/sqm_twilight (empirical SQM twilight model)
    """
    h = sun_alt_deg
    if h >= -12.0:
        return -1.057 * h + 6.7489
    else:
        return -0.0744 * h * h - 2.5768 * h - 0.5845


def _sky_brightness_fraction(sun_alt_deg):
    """
    Fraction of sky brightness from 0.0 (full dark) to 1.0 (sunrise).

    Based on empirical SQM (Sky Quality Meter) zenith brightness model.
    """
    if sun_alt_deg > 0:
        return 1.0
    if sun_alt_deg <= -18.0:
        return 0.0
    sqm = _zenith_sqm(sun_alt_deg)
    darkness = (sqm - SQM_SUNRISE) / (SQM_DARK - SQM_SUNRISE)
    return float(1.0 - np.clip(darkness, 0.0, 1.0))


def imminence_score(sun_alt_deg):
    """
    How close the sun is to rising: 1.0 = sunrise (maximum imminence),
    0.0 = full dark / night (no imminence).

    "Just before dawn" in the prophecy means the warning is imminent --
    the sun is ALMOST up. Closer to sunrise = higher score.

    Uses the SQM sky brightness model (inverted): brighter sky =
    closer to sunrise = more imminent.

      Sun  0°:  score = 1.00  (sunrise — maximum imminence)
      Sun -6°:  score = 0.58  (civil twilight)
      Sun -12°: score = 0.15  (nautical twilight)
      Sun -18°: score = 0.00  (astronomical dawn — not imminent)
      Sun <-18°: score = 0.00 (night)
    """
    return _sky_brightness_fraction(sun_alt_deg)


def redness_score(altitude_deg):
    """
    Score how red Regulus appears at a given altitude, on a continuous 0-1
    scale normalized to the physical range of atmospheric reddening.

    Linear mapping from zenith B-V (~+0.03, white) to horizon B-V (~+2.7,
    deep red). Every altitude gets proportional credit.

    In this interpretation, redness IS the signal -- Regulus reddened on
    the horizon is the warning sign (cf. "red sky at morning").
    """
    bv = observed_bv(altitude_deg)
    bv_zenith = observed_bv(90.0)
    bv_max = observed_bv(1.0)
    if bv_max <= bv_zenith:
        return 0.0
    raw = (bv - bv_zenith) / (bv_max - bv_zenith)
    return float(np.clip(raw, 0.0, 1.0))


def visibility_score(v_mag, sun_alt_deg):
    """
    How prominently Regulus stands out against the sky: 0-1 soft score.

    The same atmosphere that reddens Regulus also dims it (atmospheric
    density does double duty). Meanwhile, a brighter sky (closer to
    sunrise) reduces contrast. This score captures both effects.

    Uses arcus visionis: limiting magnitude as a function of sky
    brightness (Sun altitude). The score is the star's "headroom"
    above the detection threshold, normalized to a 0-1 range:

      margin = limiting_mag - v_mag_extincted
      score  = clamp(margin / 2.0, 0, 1)

    At 1.0 the star is vivid against the sky; at 0.0 it is invisible.
    This creates a natural tension with imminence: brighter dawn sky
    = higher imminence but lower visibility. The product of the two
    peaks at the inflection point — the last moment the star is
    prominently visible before sunrise washes it out.
    """
    if sun_alt_deg > 0:
        return 0.0
    limiting_mag = 2.0 + abs(sun_alt_deg) * 0.3
    if v_mag > limiting_mag:
        return 0.0
    margin = limiting_mag - v_mag
    return float(np.clip(margin / 2.0, 0.0, 1.0))


def az_proximity_score(az_deg, sigma=DEFAULT_AZ_SIGMA):
    """
    Score how close Regulus's azimuth is to the Sphinx's gaze (90°).

    Gaussian centered on 90° with configurable width (sigma=2°).
    """
    return np.exp(-0.5 * ((az_deg - SPHINX_AZIMUTH) / sigma) ** 2)


def prophecy_score(r_score, imm_score, vis_score, az_score):
    """
    Composite prophecy fulfillment score.

    Product of four physical factors:

      prophecy = redness × imminence × visibility × az_proximity

    Each factor is 0-1. The product requires ALL conditions
    simultaneously — any single weak factor correctly suppresses the
    score. No weights needed; the physics self-balances.

    The four factors map to four physical drivers:

      1. Precession     → redness    (dec → alt at az=90° → airmass → B-V)
      2. Atmospheric     → visibility (same airmass that reddens also dims;
         density                       sky brightness reduces contrast)
      3. Alignment       → az_prox   (Sphinx's gaze, az=90°)
      4. Angle           → imminence (sun's angle — how close to rising)

    The tension between imminence (pushes toward sunrise / brighter sky)
    and visibility (pushes toward darker sky / more contrast) creates a
    natural inflection point: the prophecy peaks at the last moment the
    reddened star is prominently visible before dawn washes it out.
    """
    return r_score * imm_score * vis_score * az_score


def setup():
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    loader = load
    loader.directory = str(data_dir)
    eph = loader("de441.bsp")
    ts = load.timescale()

    earth = eph["earth"]
    sun = eph["sun"]
    regulus = Star(
        ra_hours=REGULUS_RA_HOURS,
        dec_degrees=REGULUS_DEC_DEG,
        ra_mas_per_year=REGULUS_PM_RA_MASYR,
        dec_mas_per_year=REGULUS_PM_DEC_MASYR,
        parallax_mas=REGULUS_PARALLAX_MAS,
        radial_km_per_s=REGULUS_RV_KMSEC,
    )
    giza = wgs84.latlon(GIZA_LAT * N, GIZA_LON * E)

    return eph, ts, earth, sun, regulus, giza


def find_az90_crossing(observer, regulus, ts, year, month, day):
    """
    Find the moment Regulus crosses azimuth 90 degrees during the pre-dawn
    hours of a given date at Giza.

    Scans from midnight to sunrise (~00:00 to 06:00 local, which is
    ~22:00 to 04:00 UTC for Giza at UTC+2) in 2-minute steps using
    vectorized Skyfield calls, then refines with bisection.

    Returns dict with crossing info or None if no crossing found.
    """
    t_start = ts.tt(year, month, day - 1, 22, 0, 0)
    t_end = ts.tt(year, month, day, 6, 0, 0)

    n_steps = 240
    jds = np.linspace(t_start.tt, t_end.tt, n_steps)
    times = ts.tt_jd(jds)

    app = observer.at(times).observe(regulus).apparent()
    alt, az, _ = app.altaz()
    alts = alt.degrees
    azs = az.degrees

    for i in range(len(azs) - 1):
        if alts[i] < -2 and alts[i + 1] < -2:
            continue
        if (azs[i] - 90.0) * (azs[i + 1] - 90.0) < 0:
            if abs(azs[i] - azs[i + 1]) > 180:
                continue

            t_lo = jds[i]
            t_hi = jds[i + 1]
            for _ in range(30):
                t_mid_jd = (t_lo + t_hi) / 2.0
                t_mid = ts.tt_jd(t_mid_jd)
                app_mid = observer.at(t_mid).observe(regulus).apparent()
                _, az_mid, _ = app_mid.altaz()
                if (azs[i] - 90.0) * (az_mid.degrees - 90.0) < 0:
                    t_hi = t_mid_jd
                else:
                    t_lo = t_mid_jd
                if abs(t_hi - t_lo) < 1e-8:
                    break

            t_cross_jd = (t_lo + t_hi) / 2.0
            t_cross = ts.tt_jd(t_cross_jd)
            app_cross = observer.at(t_cross).observe(regulus).apparent()
            alt_cross, az_cross, _ = app_cross.altaz()

            if alt_cross.degrees < -2:
                continue

            return {
                "t": t_cross,
                "alt_deg": alt_cross.degrees,
                "az_deg": az_cross.degrees,
            }

    return None


def analyze_date(observer, earth, sun, regulus, ts, year, month, day):
    """
    Full analysis for one date: find az=90 crossing, compute Sun position,
    atmospheric reddening, and all scores.
    """
    crossing = find_az90_crossing(observer, regulus, ts, year, month, day)
    if crossing is None:
        return None

    t_cross = crossing["t"]
    reg_alt = crossing["alt_deg"]
    reg_az = crossing["az_deg"]

    sun_app = (earth + wgs84.latlon(GIZA_LAT * N, GIZA_LON * E)).at(
        t_cross
    ).observe(sun).apparent()
    sun_alt, sun_az, _ = sun_app.altaz()
    sun_alt_deg = sun_alt.degrees

    bv_obs = observed_bv(reg_alt)
    v_mag = observed_vmag(reg_alt)
    X = airmass_kasten_young(reg_alt)

    r_sc = redness_score(reg_alt)
    imm_sc = imminence_score(sun_alt_deg)
    vis_sc = visibility_score(v_mag, sun_alt_deg)
    az_sc = az_proximity_score(reg_az)
    comp = prophecy_score(r_sc, imm_sc, vis_sc, az_sc)

    cal = t_cross.tt_calendar()

    return {
        "year": cal[0], "month": cal[1], "day": cal[2],
        "hour": cal[3], "minute": cal[4],
        "reg_alt": reg_alt,
        "reg_az": reg_az,
        "sun_alt": sun_alt_deg,
        "sun_az": sun_az.degrees,
        "bv_obs": bv_obs,
        "v_mag": v_mag,
        "airmass": X,
        "color_name": bv_to_color_name(bv_obs),
        "twilight": twilight_phase(sun_alt_deg),
        "redness": r_sc,
        "imminence": imm_sc,
        "visibility": vis_sc,
        "az_score": az_sc,
        "composite": comp,
        "t": t_cross,
    }


def main():
    print("=" * 70)
    print("REGULUS-SPHINX PROPHECY ALIGNMENT SCANNER")
    print("=" * 70)
    print()
    print('Prophecy: "When the red star of Regulus aligns just before dawn')
    print('           in the gaze of the Sphinx."')
    print()
    print("Scoring: prophecy = redness × imminence × visibility × az_prox")
    print()

    horizon_dip = compute_horizon_dip(SPHINX_EYE_ABOVE_HORIZON)
    print(f"Observer: Sphinx eyes at Giza ({GIZA_LAT}°N, {GIZA_LON}°E)")
    print(f"Eye height above E horizon: {SPHINX_EYE_ABOVE_HORIZON:.0f} m")
    print(f"Horizon dip: {horizon_dip:.4f}° ({horizon_dip*60:.2f} arcmin)")
    print()

    eph, ts, earth, sun, regulus, giza = setup()
    observer = earth + giza

    t_now = ts.tt(2026, 4, 11, 3, 0, 0)
    app = observer.at(t_now).observe(regulus).apparent()
    alt_now, az_now, _ = app.altaz()
    ra_now, dec_now, _ = app.radec(epoch="date")
    print(f"Regulus today (2026-04-11):")
    print(f"  Dec (of-date): {dec_now.degrees:.4f}°")
    print(f"  Crosses az=90° while climbing -- this is the event we seek")
    print()

    print(f"Scanning {SCAN_YEARS} years forward from 2026-04-11 ...")
    print()

    start_year = 2026
    start_month = 4
    start_day = 11
    total_days = SCAN_YEARS * 365

    all_results = []
    prev_pct = -1

    for d in range(total_days):
        t_probe = ts.tt(start_year, start_month, start_day + d)
        cal = t_probe.tt_calendar()
        yr, mo, dy = cal[0], cal[1], cal[2]

        pct = int(d / total_days * 100)
        if pct % 10 == 0 and pct != prev_pct:
            prev_pct = pct
            print(f"  {pct}% ... scanning {yr}-{mo:02d}-{dy:02d}")

        result = analyze_date(observer, earth, sun, regulus, ts, yr, mo, dy)
        if result is not None:
            all_results.append(result)

    print(f"  100% ... done. Found {len(all_results)} dates with az=90 crossings")
    print()

    all_results.sort(key=lambda r: r["composite"], reverse=True)

    print("=" * 70)
    print("TOP 10 ALIGNMENT DATES")
    print("=" * 70)
    print()
    print("Scoring: prophecy = redness × imminence × visibility × az_prox")
    print()

    for rank, r in enumerate(all_results[:10], 1):
        print(f"{'─'*70}")
        print(f"  #{rank}  {r['year']}-{r['month']:02d}-{r['day']:02d}"
              f"  ~{r['hour']:02d}:{r['minute']:02d} UTC")
        print(f"{'─'*70}")
        print(f"  PROPHECY SCORE:        {r['composite']:.6f}")
        print(f"    Redness:             {r['redness']:.6f}"
              f"  (B-V: {r['bv_obs']:+.2f}, {r['color_name']})")
        print(f"    Imminence:           {r['imminence']:.6f}"
              f"  (Sun alt: {r['sun_alt']:.2f}°, {r['twilight']})")
        print(f"    Az proximity:        {r['az_score']:.6f}"
              f"  (Regulus az: {r['reg_az']:.2f}°, Sphinx: {SPHINX_AZIMUTH}°)")
        print(f"    Visibility:          {r['visibility']:.6f}"
              f"  (V mag: {r['v_mag']:.1f})")
        print()
        print(f"  Regulus altitude:      {r['reg_alt']:.2f}°")
        print(f"  Airmass:               {r['airmass']:.1f}")
        print()

    if all_results:
        best_year = all_results[0]["year"]
        print(f"{'─'*70}")
        print(f"  DAILY DETAIL: Best month around top result ({best_year})")
        print(f"{'─'*70}")
        print()

        best_month = all_results[0]["month"]
        month_results = [r for r in all_results
                         if r["year"] == best_year
                         and abs(r["month"] - best_month) <= 1]
        month_results.sort(key=lambda r: (r["month"], r["day"]))

        print(f"  {'Date':<12} {'RegAlt':>7} {'RegAz':>7} {'SunAlt':>7}"
              f" {'B-V':>6} {'Color':<13} {'Twilight':<20}"
              f" {'Red':>6} {'Imm':>6} {'Az':>6} {'Score':>8}")
        print(f"  {'─'*12} {'─'*7} {'─'*7} {'─'*7}"
              f" {'─'*6} {'─'*13} {'─'*20}"
              f" {'─'*6} {'─'*6} {'─'*6} {'─'*8}")
        for r in month_results:
            ds = f"{r['year']}-{r['month']:02d}-{r['day']:02d}"
            print(f"  {ds:<12} {r['reg_alt']:>7.2f} {r['reg_az']:>7.2f}"
                  f" {r['sun_alt']:>7.2f} {r['bv_obs']:>+6.2f}"
                  f" {r['color_name']:<13} {r['twilight']:<20}"
                  f" {r['redness']:>6.4f} {r['imminence']:>6.4f}"
                  f" {r['az_score']:>6.4f} {r['composite']:>8.6f}")

        print()

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        scored = sorted(all_results, key=lambda r: r["composite"], reverse=True)
        scored = scored[:500]
        scored.sort(key=lambda r: (r["year"], r["month"], r["day"]))

        dates = [r["year"] + (r["month"] - 1) / 12.0 + r["day"] / 365.0
                 for r in scored]

        fig, axes = plt.subplots(4, 1, figsize=(16, 14))

        ax = axes[0]
        ax.scatter(dates, [r["reg_alt"] for r in scored], c="steelblue",
                   s=8, alpha=0.6)
        ax.set_ylabel("Regulus Altitude (deg)")
        ax.set_title("Regulus Altitude at Az=90° Crossing")
        ax.grid(True, alpha=0.3)

        ax = axes[1]
        ax.scatter(dates, [r["sun_alt"] for r in scored], c="orange",
                   s=8, alpha=0.6)
        ax.axhline(y=-6, color="r", ls="--", lw=0.5, label="Civil twi (-6°)")
        ax.axhline(y=-12, color="purple", ls="--", lw=0.5, label="Nautical twi (-12°)")
        ax.set_ylabel("Sun Altitude (deg)")
        ax.set_title("Sun Altitude When Regulus Crosses Az=90°")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        ax = axes[2]
        colors_bv = [r["bv_obs"] for r in scored]
        sc = ax.scatter(dates, colors_bv, c=colors_bv, cmap="RdYlBu_r",
                        s=8, alpha=0.6, vmin=-0.5, vmax=2.0)
        ax.set_ylabel("Observed B-V")
        ax.set_title("Atmospheric Reddening of Regulus at Az=90° Crossing")
        ax.axhline(y=0.8, color="orange", ls="--", lw=0.5, label="Orange threshold")
        ax.axhline(y=1.2, color="red", ls="--", lw=0.5, label="Red threshold")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        plt.colorbar(sc, ax=ax, label="B-V")

        ax = axes[3]
        comps = [r["composite"] for r in scored]
        ax.scatter(dates, comps, c="forestgreen", s=10, alpha=0.7)
        if comps:
            best_i = np.argmax(comps)
            ax.scatter([dates[best_i]], [comps[best_i]], c="gold",
                       s=80, edgecolors="black", zorder=5, label="Best match")
        ax.set_ylabel("Prophecy Score")
        ax.set_xlabel("Date")
        ax.set_title("Prophecy Score (redness × imminence × az_prox)")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plot_path = str(Path(__file__).parent / "regulus_upcoming_scores.png")
        plt.savefig(plot_path, dpi=150)
        print(f"Plot saved to: {plot_path}")
        plt.close()

    except ImportError:
        print("matplotlib not available, skipping plot.")

    print("\nDone.")


if __name__ == "__main__":
    main()
