# Single-Stage Experiment Results

This document records the completed run of the single-moment almanac optimizer (`regulus_optuna_optimizer.py`).

## Script Run

```bash
PYTHONUNBUFFERED=1 python3 regulus_optuna_optimizer.py
```

Generated plot artifact:

- `regulus_optuna_results.png`

## Model Reminder

Single-stage score:

```text
prophecy = redness x imminence x visibility x az_proximity
```

One timestamp must satisfy all four factors simultaneously.

## Near-Term Results (2026-2031)

Summary:

- Trials evaluated: `1,257`
- Peak prophecy score: `0.031568`
- Median score: `0.000000`
- Best raw date: `2029-09-22`
- Best proximity-weighted date: `2027-09-22`

Top near-term interpretation:

- Near-term winners are tightly aligned in azimuth and timing (civil twilight, ~15-23 min before sunrise).
- Redness remains very low (`B-V ~ +0.22 to +0.26`, white/very mild), which is the primary bottleneck.

### Full Near-Term Top 10 (Raw)

| Rank | Date | Time UTC | Prophecy | Red | Imm | Vis | Az | Reg Alt | Reg Az | Sun Alt | B-V (color, strength) | Vmag | Twilight | Airmass | Offset (min) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|---:|---:|
| 1 | 2029-09-22 | 03:24:07.0 | 0.031568 | 0.0584 | 0.6223 | 0.8789 | 0.9889 | 23.69° | 89.70° | -5.34° | +0.24 (white, very mild) | 1.85 | civil twilight | 2.48 | -20.9 |
| 2 | 2029-09-23 | 03:22:59.9 | 0.031408 | 0.0561 | 0.5967 | 0.9388 | 0.9997 | 24.30° | 90.05° | -5.70° | +0.24 (white, very mild) | 1.83 | civil twilight | 2.42 | -22.5 |
| 3 | 2027-09-22 | 03:23:56.5 | 0.031372 | 0.0601 | 0.6239 | 0.8709 | 0.9600 | 23.24° | 89.43° | -5.32° | +0.25 (white, very mild) | 1.85 | civil twilight | 2.52 | -20.7 |
| 4 | 2029-09-21 | 03:23:27.8 | 0.030720 | 0.0624 | 0.6207 | 0.8721 | 0.9099 | 22.69° | 89.13° | -5.37° | +0.26 (white, very mild) | 1.87 | civil twilight | 2.58 | -21.0 |
| 5 | 2027-09-21 | 03:25:20.0 | 0.029659 | 0.0624 | 0.6535 | 0.8023 | 0.9065 | 22.68° | 89.11° | -4.90° | +0.26 (white, very mild) | 1.87 | civil twilight | 2.58 | -18.8 |
| 6 | 2027-09-23 | 03:26:13.8 | 0.029467 | 0.0550 | 0.6505 | 0.8275 | 0.9947 | 24.59° | 90.21° | -4.94° | +0.23 (white, very mild) | 1.83 | civil twilight | 2.39 | -19.0 |
| 7 | 2030-09-21 | 03:28:40.2 | 0.028777 | 0.0587 | 0.7022 | 0.7083 | 0.9855 | 23.60° | 89.66° | -4.21° | +0.25 (white, very mild) | 1.85 | civil twilight | 2.49 | -15.6 |
| 8 | 2029-09-20 | 03:26:07.2 | 0.028544 | 0.0636 | 0.6696 | 0.7653 | 0.8765 | 22.41° | 88.97° | -4.67° | +0.26 (white, very mild) | 1.87 | civil twilight | 2.61 | -17.8 |
| 9 | 2029-09-24 | 03:24:12.8 | 0.027616 | 0.0522 | 0.6069 | 0.9271 | 0.9405 | 25.41° | 90.70° | -5.56° | +0.22 (white, very mild) | 1.81 | civil twilight | 2.32 | -21.8 |
| 10 | 2028-09-21 | 03:30:05.6 | 0.027264 | 0.0559 | 0.7198 | 0.6783 | 0.9993 | 24.35° | 90.08° | -3.96° | +0.24 (white, very mild) | 1.83 | civil twilight | 2.41 | -14.5 |

### Full Near-Term Top 10 (Proximity-Weighted)

| Rank | Date | Time UTC | Weighted | Prophecy | Weight | Years From 2026 | Red | Imm | Vis | Az | Reg Alt | Reg Az | Sun Alt | B-V (color, strength) | Twilight |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | 2027-09-22 | 03:23:56.5 | 0.031156 | 0.031372 | 0.9931 | +1 | 0.0601 | 0.6239 | 0.8709 | 0.9600 | 23.24° | 89.43° | -5.32° | +0.25 (white, very mild) | civil twilight |
| 2 | 2029-09-22 | 03:24:07.0 | 0.030918 | 0.031568 | 0.9794 | +3 | 0.0584 | 0.6223 | 0.8789 | 0.9889 | 23.69° | 89.70° | -5.34° | +0.24 (white, very mild) | civil twilight |
| 3 | 2029-09-23 | 03:22:59.9 | 0.030762 | 0.031408 | 0.9794 | +3 | 0.0561 | 0.5967 | 0.9388 | 0.9997 | 24.30° | 90.05° | -5.70° | +0.24 (white, very mild) | civil twilight |
| 4 | 2029-09-21 | 03:23:27.8 | 0.030088 | 0.030720 | 0.9794 | +3 | 0.0624 | 0.6207 | 0.8721 | 0.9099 | 22.69° | 89.13° | -5.37° | +0.26 (white, very mild) | civil twilight |
| 5 | 2027-09-21 | 03:25:20.0 | 0.029454 | 0.029659 | 0.9931 | +1 | 0.0624 | 0.6535 | 0.8023 | 0.9065 | 22.68° | 89.11° | -4.90° | +0.26 (white, very mild) | civil twilight |
| 6 | 2027-09-23 | 03:26:13.8 | 0.029263 | 0.029467 | 0.9931 | +1 | 0.0550 | 0.6505 | 0.8275 | 0.9947 | 24.59° | 90.21° | -4.94° | +0.23 (white, very mild) | civil twilight |
| 7 | 2030-09-21 | 03:28:40.2 | 0.027990 | 0.028777 | 0.9727 | +4 | 0.0587 | 0.7022 | 0.7083 | 0.9855 | 23.60° | 89.66° | -4.21° | +0.25 (white, very mild) | civil twilight |
| 8 | 2029-09-20 | 03:26:07.2 | 0.027957 | 0.028544 | 0.9794 | +3 | 0.0636 | 0.6696 | 0.7653 | 0.8765 | 22.41° | 88.97° | -4.67° | +0.26 (white, very mild) | civil twilight |
| 9 | 2029-09-24 | 03:24:12.8 | 0.027047 | 0.027616 | 0.9794 | +3 | 0.0522 | 0.6069 | 0.9271 | 0.9405 | 25.41° | 90.70° | -5.56° | +0.22 (white, very mild) | civil twilight |
| 10 | 2028-09-21 | 03:30:05.6 | 0.026888 | 0.027264 | 0.9862 | +2 | 0.0559 | 0.7198 | 0.6783 | 0.9993 | 24.35° | 90.08° | -3.96° | +0.24 (white, very mild) | civil twilight |

## Deep-Time Results (2026-6500, mirror-log)

Summary:

- Trials evaluated: `7,101`
- Peak prophecy score: `0.088695`
- Median score: `0.000339`
- Best raw date: `3739-10-01`
- Best proximity-weighted date: `2027-09-25`

Top deep-time interpretation:

- Deep-time optima move Regulus much lower (`~5-7°`) than near-term winners (`~22-25°`).
- This raises redness strongly (B-V up to `+1.20` and beyond), while preserving near-exact azimuth alignment and useful visibility in nautical twilight.

### Full Deep-Time Top 20 (Raw)

| Rank | Date | Time UTC | Prophecy | Red | Imm | Vis | Az | Reg Alt | Reg Az | Sun Alt | B-V (color, strength) | Vmag | Twilight | Airmass | Offset (min) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|---:|---:|
| 1 | 3739-10-01 | 06:27:30.6 | 0.088695 | 0.3222 | 0.3781 | 0.7290 | 0.9986 | 5.76° | 90.10° | -8.80° | +1.20 (orange-red, very strong) | 3.18 | nautical twilight | 9.16 | -36.8 |
| 2 | 3731-10-01 | 06:24:18.6 | 0.088446 | 0.3376 | 0.3552 | 0.7385 | 0.9985 | 5.48° | 89.89° | -9.12° | +1.26 (orange-red, very strong) | 3.26 | nautical twilight | 9.55 | -38.3 |
| 3 | 3684-09-30 | 06:14:33.0 | 0.088158 | 0.2900 | 0.3510 | 0.8681 | 0.9977 | 6.42° | 90.14° | -9.18° | +1.09 (orange, strong) | 3.02 | nautical twilight | 8.34 | -38.6 |
| 4 | 3637-09-30 | 06:04:33.2 | 0.087928 | 0.2908 | 0.3477 | 0.8731 | 0.9961 | 6.40° | 89.82° | -9.23° | +1.09 (orange, strong) | 3.02 | nautical twilight | 8.36 | -38.8 |
| 5 | 3615-09-30 | 06:01:38.5 | 0.087864 | 0.2895 | 0.3744 | 0.8199 | 0.9890 | 6.43° | 89.70° | -8.85° | +1.08 (orange, strong) | 3.02 | nautical twilight | 8.33 | -37.0 |
| 6 | 3681-09-30 | 06:16:22.4 | 0.087283 | 0.2756 | 0.3905 | 0.8208 | 0.9882 | 6.76° | 90.31° | -8.62° | +1.03 (orange, strong) | 2.94 | nautical twilight | 7.97 | -36.0 |
| 7 | 3616-09-29 | 06:05:14.1 | 0.087210 | 0.2678 | 0.4281 | 0.7607 | 1.0000 | 6.95° | 90.01° | -8.09° | +1.00 (orange, strong) | 2.91 | nautical twilight | 7.78 | -33.5 |
| 8 | 3641-09-29 | 06:07:28.7 | 0.087178 | 0.3106 | 0.3877 | 0.7380 | 0.9809 | 5.98° | 89.61° | -8.66° | +1.16 (orange, strong) | 3.12 | nautical twilight | 8.86 | -36.2 |
| 9 | 3770-10-01 | 06:34:55.1 | 0.086987 | 0.3121 | 0.3877 | 0.7344 | 0.9790 | 5.95° | 90.41° | -8.66° | +1.17 (orange, strong) | 3.13 | nautical twilight | 8.90 | -36.2 |
| 10 | 3589-09-29 | 05:58:54.6 | 0.086880 | 0.2786 | 0.4154 | 0.7603 | 0.9874 | 6.68° | 89.68° | -8.27° | +1.04 (orange, strong) | 2.96 | nautical twilight | 8.05 | -34.4 |
| 11 | 3629-09-30 | 06:01:58.9 | 0.086825 | 0.2982 | 0.3330 | 0.8855 | 0.9874 | 6.24° | 89.68° | -9.44° | +1.11 (orange, strong) | 3.06 | nautical twilight | 8.55 | -39.8 |
| 12 | 3575-09-30 | 05:56:39.0 | 0.086751 | 0.2547 | 0.4190 | 0.8131 | 0.9997 | 7.30° | 89.95° | -8.22° | +0.96 (orange, strong) | 2.84 | nautical twilight | 7.45 | -34.1 |
| 13 | 3714-09-30 | 06:23:34.8 | 0.086628 | 0.3330 | 0.4051 | 0.6447 | 0.9964 | 5.56° | 89.83° | -8.42° | +1.24 (orange-red, very strong) | 3.24 | nautical twilight | 9.43 | -35.0 |
| 14 | 3556-09-29 | 05:51:32.9 | 0.086200 | 0.2701 | 0.3993 | 0.8160 | 0.9795 | 6.89° | 89.59° | -8.50° | +1.01 (orange, strong) | 2.92 | nautical twilight | 7.84 | -35.4 |
| 15 | 3761-09-30 | 06:34:29.7 | 0.086162 | 0.3257 | 0.4167 | 0.6384 | 0.9945 | 5.70° | 90.21° | -8.25° | +1.21 (orange-red, very strong) | 3.20 | nautical twilight | 9.24 | -34.3 |
| 16 | 3736-09-30 | 06:29:58.6 | 0.085902 | 0.2982 | 0.4277 | 0.6844 | 0.9839 | 6.24° | 90.36° | -8.09° | +1.11 (orange, strong) | 3.06 | nautical twilight | 8.55 | -33.6 |
| 17 | 3705-09-30 | 06:19:01.3 | 0.085888 | 0.3516 | 0.3623 | 0.6882 | 0.9797 | 5.25° | 89.60° | -9.02° | +1.31 (orange-red, very strong) | 3.33 | nautical twilight | 9.90 | -37.8 |
| 18 | 3651-09-29 | 06:12:32.1 | 0.085880 | 0.3023 | 0.4373 | 0.6540 | 0.9935 | 6.15° | 89.77° | -7.96° | +1.13 (orange, strong) | 3.08 | nautical twilight | 8.65 | -32.9 |
| 19 | 3571-09-30 | 05:56:55.2 | 0.085679 | 0.2459 | 0.4352 | 0.8010 | 0.9994 | 7.55° | 90.07° | -7.99° | +0.93 (orange, strong) | 2.79 | nautical twilight | 7.22 | -33.1 |
| 20 | 3635-09-29 | 06:10:24.9 | 0.085386 | 0.2867 | 0.4546 | 0.6567 | 0.9977 | 6.49° | 89.86° | -7.72° | +1.07 (orange, strong) | 3.00 | nautical twilight | 8.26 | -31.8 |

### Full Deep-Time Top 20 (Proximity-Weighted)

| Rank | Date | Time UTC | Weighted | Prophecy | Weight | Years From 2026 | Red | Imm | Vis | Az | Reg Alt | Reg Az | Sun Alt | B-V (color, strength) | Twilight |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | 2027-09-25 | 03:18:01.9 | 0.027816 | 0.028010 | 0.9931 | +1 | 0.0553 | 0.5082 | 1.0000 | 0.9966 | 24.51° | 90.16° | -6.96° | +0.23 (white, very mild) | nautical twilight |
| 2 | 2029-09-26 | 03:10:11.0 | 0.020910 | 0.021349 | 0.9794 | +3 | 0.0569 | 0.3755 | 1.0000 | 0.9993 | 24.07° | 89.92° | -8.83° | +0.24 (white, very mild) | nautical twilight |
| 3 | 2056-09-25 | 03:16:58.0 | 0.020874 | 0.025699 | 0.8123 | +30 | 0.0546 | 0.4825 | 1.0000 | 0.9751 | 24.70° | 90.45° | -7.32° | +0.23 (white, very mild) | nautical twilight |
| 4 | 2032-09-26 | 03:10:51.8 | 0.020433 | 0.021300 | 0.9593 | +6 | 0.0557 | 0.3837 | 1.0000 | 0.9976 | 24.41° | 90.14° | -8.72° | +0.24 (white, very mild) | nautical twilight |
| 5 | 2028-09-26 | 03:08:41.6 | 0.019740 | 0.020016 | 0.9862 | +2 | 0.0573 | 0.3503 | 1.0000 | 0.9975 | 23.97° | 89.86° | -9.19° | +0.24 (white, very mild) | nautical twilight |
| 6 | 2035-09-27 | 03:08:36.6 | 0.018478 | 0.019667 | 0.9395 | +9 | 0.0567 | 0.3466 | 1.0000 | 1.0000 | 24.12° | 89.98° | -9.24° | +0.24 (white, very mild) | nautical twilight |
| 7 | 2032-09-27 | 03:09:42.8 | 0.017813 | 0.018570 | 0.9593 | +6 | 0.0535 | 0.3575 | 1.0000 | 0.9705 | 25.02° | 90.49° | -9.09° | +0.23 (white, very mild) | nautical twilight |
| 8 | 2081-09-25 | 03:15:00.8 | 0.017717 | 0.025939 | 0.6830 | +55 | 0.0578 | 0.4497 | 1.0000 | 0.9985 | 23.85° | 90.11° | -7.78° | +0.24 (white, very mild) | nautical twilight |
| 9 | 2043-09-26 | 03:06:49.6 | 0.016876 | 0.018986 | 0.8888 | +17 | 0.0619 | 0.3273 | 1.0000 | 0.9379 | 22.82° | 89.28° | -9.52° | +0.26 (white, very mild) | nautical twilight |
| 10 | 2086-09-21 | 03:16:34.9 | 0.016487 | 0.024990 | 0.6598 | +60 | 0.0725 | 0.5082 | 1.0000 | 0.6782 | 20.51° | 88.24° | -6.96° | +0.30 (white, very mild) | nautical twilight |
| 11 | 2049-09-27 | 03:19:16.6 | 0.014882 | 0.017454 | 0.8526 | +23 | 0.0480 | 0.5033 | 1.0000 | 0.7232 | 26.75° | 91.61° | -7.03° | +0.21 (white, very mild) | nautical twilight |
| 12 | 2027-09-29 | 03:10:32.1 | 0.014679 | 0.014781 | 0.9931 | +1 | 0.0493 | 0.3593 | 1.0000 | 0.8340 | 26.30° | 91.20° | -9.06° | +0.21 (white, very mild) | nautical twilight |
| 13 | 2032-09-28 | 03:05:28.0 | 0.014279 | 0.014885 | 0.9593 | +6 | 0.0538 | 0.2840 | 1.0000 | 0.9750 | 24.95° | 90.45° | -10.13° | +0.23 (white, very mild) | nautical twilight |
| 14 | 2031-09-29 | 03:11:44.4 | 0.014028 | 0.014523 | 0.9659 | +5 | 0.0486 | 0.3775 | 1.0000 | 0.7913 | 26.53° | 91.37° | -8.80° | +0.21 (white, very mild) | nautical twilight |
| 15 | 2030-09-29 | 03:10:38.2 | 0.013507 | 0.013886 | 0.9727 | +4 | 0.0487 | 0.3584 | 1.0000 | 0.7960 | 26.51° | 91.35° | -9.08° | +0.21 (white, very mild) | nautical twilight |
| 16 | 2028-09-18 | 03:15:49.6 | 0.012643 | 0.012820 | 0.9862 | +2 | 0.0828 | 0.5274 | 1.0000 | 0.2937 | 18.69° | 86.87° | -6.69° | +0.33 (yellow-white, mild) | nautical twilight |
| 17 | 2104-09-27 | 03:10:24.0 | 0.012290 | 0.021104 | 0.5824 | +78 | 0.0584 | 0.3628 | 1.0000 | 0.9967 | 23.69° | 90.16° | -9.01° | +0.24 (white, very mild) | nautical twilight |
| 18 | 2028-09-22 | 03:05:52.7 | 0.012174 | 0.012344 | 0.9862 | +2 | 0.0755 | 0.3417 | 1.0000 | 0.4785 | 19.95° | 87.57° | -9.31° | +0.31 (yellow-white, mild) | nautical twilight |
| 19 | 2042-09-29 | 03:12:06.7 | 0.012038 | 0.013450 | 0.8950 | +16 | 0.0480 | 0.3799 | 1.0000 | 0.7382 | 26.75° | 91.56° | -8.77° | +0.21 (white, very mild) | nautical twilight |
| 20 | 2119-09-23 | 03:13:37.9 | 0.011888 | 0.022649 | 0.5249 | +93 | 0.0742 | 0.4481 | 1.0000 | 0.6811 | 20.18° | 88.25° | -7.81° | +0.30 (yellow-white, mild) | nautical twilight |

## Near-Term vs Deep-Time Comparison

- Near-term best: `2029-09-22`, `0.031568`
- Deep-time best: `3739-10-01`, `0.088695`
- Improvement: `+0.057127` (deep-time is about `2.81x` near-term)

Best-moment component comparison:

- Near-term best: `red=0.058`, `imm=0.622`, `vis=0.879`, `az=0.989`
- Deep-time best: `red=0.322`, `imm=0.378`, `vis=0.729`, `az=0.999`

Interpretation:

- Deep-time improvement is driven primarily by higher redness (lower altitude/higher airmass), while maintaining very strong azimuth alignment and acceptable visibility.
