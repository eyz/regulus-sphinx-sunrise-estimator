# Sequential Two-Stage Experiment Results

This document records the completed run of the sequential morning-arc model (`regulus_optuna_optimizer_sequential.py`).

## Script Run

```bash
PYTHONUNBUFFERED=1 python3 regulus_optuna_optimizer_sequential.py
```

Generated plot artifact:

- `regulus_optuna_sequential_results.png`

## Model Reminder

Sequential score:

```text
sequence_score = stageA_score x stageB_score
```

- Stage A (early): maximize `redness x visibility`
- Stage B (later): maximize `az_proximity x imminence x visibility`
- Constraint: Stage A must occur before Stage B in the same pre-dawn interval.

## Near-Term Results (2026-2031)

Summary:

- Valid episodes: `405`
- Peak score: `0.093960`
- Median score: `0.000099`
- Seasonal pattern: top results cluster around `Sep 19-21`

Top near-term result:

- Date: `2031-09-20`
- Sequence: `0.093960` (`stageA=0.217907`, `stageB=0.431193`)
- Stage A: `alt=8.46°`, `B-V=+0.82` (`yellow-orange`, `moderate`)
- Stage B: `az=89.16°`, `sun=-3.87°`, `B-V=+0.26` (`white`, `very mild`)
- A→B separation: `65.9 min`

Near-term interpretation:

- The two-stage pattern is present now, but Stage A redness is only moderate.
- Near-term bests are strong on visibility and azimuth, limited by incomplete redness.

### Full Near-Term Top 10

| Rank | Date | Sequence | Stage A B-V (color, strength) | Stage A Alt | Stage B Az | Stage B Sun Alt | Stage B B-V (color, strength) | A->B (min) |
|---|---|---:|---|---:|---:|---:|---|---:|
| 1 | 2031-09-20 | 0.093960 | +0.82 (yellow-orange, moderate) | 8.46° | 89.16° | -3.87° | +0.26 (white, very mild) | 65.9 |
| 2 | 2030-09-20 | 0.093924 | +0.80 (yellow-orange, moderate) | 8.71° | 89.21° | -4.02° | +0.26 (white, very mild) | 65.3 |
| 3 | 2029-09-20 | 0.093748 | +0.78 (yellow-orange, moderate) | 8.96° | 89.27° | -4.16° | +0.26 (white, very mild) | 64.6 |
| 4 | 2027-09-20 | 0.093469 | +0.82 (yellow-orange, moderate) | 8.49° | 89.15° | -3.87° | +0.26 (white, very mild) | 65.9 |
| 5 | 2026-09-20 | 0.093444 | +0.80 (yellow-orange, moderate) | 8.74° | 89.25° | -3.95° | +0.26 (white, very mild) | 65.6 |
| 6 | 2028-09-20 | 0.093436 | +0.75 (yellow-orange, moderate) | 9.21° | 89.32° | -4.31° | +0.25 (white, very mild) | 63.9 |
| 7 | 2031-09-21 | 0.093410 | +0.73 (yellow-orange, moderate) | 9.44° | 89.39° | -4.45° | +0.25 (white, very mild) | 63.2 |
| 8 | 2028-09-19 | 0.093364 | +0.85 (yellow-orange, moderate) | 8.24° | 89.10° | -3.73° | +0.26 (white, very mild) | 66.6 |
| 9 | 2029-09-19 | 0.093110 | +0.87 (yellow-orange, moderate) | 7.99° | 89.04° | -3.58° | +0.26 (white, very mild) | 67.3 |
| 10 | 2027-09-21 | 0.093000 | +0.73 (yellow-orange, moderate) | 9.46° | 89.37° | -4.45° | +0.25 (white, very mild) | 63.2 |

## Deep-Time Results (2026-6500, mirror-log)

Summary:

- Valid episodes: `6,686`
- Peak score: `0.357310`
- Median score: `0.029234`
- Best date in this run: `2991-09-26`

Top deep-time result:

- Date: `2991-09-26`
- Sequence: `0.357310` (`stageA=0.757723`, `stageB=0.471558`)
- Stage A: `alt=1.84°`, `B-V=+2.80` (`red`, `extreme`)
- Stage B: `az=89.91°`, `sun=-6.24°`, `B-V=+0.49` (`yellow-white`, `mild`)
- A→B separation: `54.6 min`

Notable trend from optimization trace:

- Early bests start near modern-like solutions, then jump as Stage A altitude drops near ~2°.
- Multiple strong candidates appear around `~2940-3135 CE`.
- Intermediate strong checkpoint noted during run: `2947-09-26` with `score=0.335472` and Stage A `B-V=+2.60` (`red`, `extreme`).

### Full Deep-Time Top 20

| Rank | Date | Sequence | Stage A B-V (color, strength) | Stage A Alt | Stage B Az | Stage B Sun Alt | Stage B B-V (color, strength) | A->B (min) |
|---|---|---:|---|---:|---:|---:|---|---:|
| 1 | 2991-09-26 | 0.357310 | +2.80 (red, extreme) | 1.84° | 89.91° | -6.24° | +0.49 (yellow-white, mild) | 54.6 |
| 2 | 3077-09-27 | 0.356827 | +2.81 (red, extreme) | 1.83° | 90.08° | -6.88° | +0.52 (yellow-white, mild) | 51.6 |
| 3 | 2995-09-26 | 0.355336 | +2.82 (red, extreme) | 1.82° | 89.89° | -6.31° | +0.49 (yellow-white, mild) | 54.3 |
| 4 | 3085-09-27 | 0.354531 | +2.79 (red, extreme) | 1.85° | 90.06° | -6.96° | +0.52 (yellow-white, mild) | 50.9 |
| 5 | 3046-09-27 | 0.354257 | +2.80 (red, extreme) | 1.84° | 90.01° | -6.60° | +0.51 (yellow-white, mild) | 52.6 |
| 6 | 3003-09-27 | 0.353573 | +2.80 (red, extreme) | 1.84° | 89.91° | -6.31° | +0.49 (yellow-white, mild) | 53.9 |
| 7 | 3058-09-27 | 0.352355 | +2.75 (red, extreme) | 1.91° | 90.00° | -6.67° | +0.51 (yellow-white, mild) | 51.6 |
| 8 | 3128-09-28 | 0.351017 | +2.80 (red, extreme) | 1.84° | 90.16° | -7.24° | +0.54 (yellow-white, mild) | 49.6 |
| 9 | 3014-09-27 | 0.350937 | +2.71 (red, extreme) | 1.95° | 89.96° | -6.53° | +0.49 (yellow-white, mild) | 53.3 |
| 10 | 3053-09-27 | 0.349593 | +2.70 (red, extreme) | 1.97° | 90.05° | -6.81° | +0.51 (yellow-white, mild) | 51.9 |
| 11 | 3066-09-27 | 0.349103 | +2.73 (red, extreme) | 1.94° | 90.03° | -6.67° | +0.51 (yellow-white, mild) | 51.3 |
| 12 | 2909-09-25 | 0.348720 | +2.80 (red, extreme) | 1.84° | 89.73° | -5.67° | +0.46 (yellow-white, mild) | 57.3 |
| 13 | 2936-09-25 | 0.348256 | +2.73 (red, extreme) | 1.92° | 89.78° | -5.95° | +0.47 (yellow-white, mild) | 56.0 |
| 14 | 2971-09-26 | 0.348233 | +2.70 (red, extreme) | 1.96° | 89.86° | -6.24° | +0.48 (yellow-white, mild) | 54.6 |
| 15 | 3070-09-27 | 0.348089 | +2.74 (red, extreme) | 1.91° | 90.00° | -6.74° | +0.52 (yellow-white, mild) | 50.9 |
| 16 | 3105-09-28 | 0.347552 | +2.77 (red, extreme) | 1.88° | 90.12° | -6.96° | +0.53 (yellow-white, mild) | 50.2 |
| 17 | 2972-09-25 | 0.347215 | +2.79 (red, extreme) | 1.85° | 89.84° | -6.02° | +0.48 (yellow-white, mild) | 55.0 |
| 18 | 3078-09-27 | 0.346026 | +2.72 (red, extreme) | 1.94° | 90.02° | -6.74° | +0.52 (yellow-white, mild) | 50.6 |
| 19 | 3135-09-29 | 0.343877 | +2.70 (red, extreme) | 1.96° | 90.23° | -7.39° | +0.53 (yellow-white, mild) | 49.2 |
| 20 | 2933-09-25 | 0.343471 | +2.74 (red, extreme) | 1.91° | 89.76° | -5.74° | +0.47 (yellow-white, mild) | 56.0 |

## Near-Term vs Deep-Time Comparison

- Near-term best: `2031-09-20`, `0.093960`, `Δt=65.9 min`
- Deep-time best: `2991-09-26`, `0.357310`, `Δt=54.6 min`

Ratio:

- Deep-time best is about `3.80x` the near-term best score (`0.357310 / 0.093960`).

## Practical Reading

- The sequential interpretation works in both eras, but with different visual character.
- Near-term: Stage A is warmed/yellow-orange, not fully red.
- Deep-time optimum: Stage A becomes strongly red near the horizon while Stage B remains tightly aligned with the Sphinx gaze before sunrise.
