# Regulus-Sphinx Prophecy Alignment Search

> **"When the red star of Regulus aligns just before dawn in the gaze of the Sphinx."**

This project uses precise positional astronomy to find dates when this prophecy can be **witnessed with human eyes** — when the physical sky best embodies the metaphor. A Bayesian optimizer (Optuna) runs two studies: a **near-term search** (2026--2031) to find the earliest observable hint today, and a **deep-time search** (2026--6500 CE) to find the peak fulfillment across a full precession cycle.

Prophecy is typically a long-term story, not an imminent event. This project treats it that way: the near-term search is not looking for fulfillment — it is looking for when you can *first begin to see* what the prophecy points toward. The deep-time search finds where the story reaches its climax.

**The short answer: the prophecy is beginning now and deepens over millennia.** In our era, Regulus is still ~24° high when it crosses the Sphinx's sightline (az=90°) — the reddening is subtle but real, the opening chapter of a long arc. Peak scored fulfillment lands around **2991--3739 CE** depending on the model — not at the geometric extreme (~4244 CE, where Regulus would skim the horizon but be too dim to see). [Why Regulus won't appear deeply red anytime soon.](#why-regulus-wont-appear-red-anytime-soon)

**Latest run results at a glance:**

| Model | Near-term best | Score | Deep-time best | Score |
|---|---|---:|---|---:|
| [Single-moment](SINGLE_STAGE_RESULTS.md) | 2029-09-22 | 0.031568 | 3739-10-01 | 0.088695 |
| [Sequential morning-arc](SEQUENTIAL_TWO_STAGE_RESULTS.md) | 2031-09-20 | 0.093960 | 2991-09-26 | 0.357310 |

---

## Author's Interpretation

*What follows is extrapolation from deep thinking about the relevance of this phrase, taken as far as the author could considering the synergies between the astronomical, atmospheric, scriptural, and symbolic concepts involved. It is one interpretation — not a claim of authority or historical fact.*

- **"Red star"** — Regulus literally reddened by atmospheric extinction near the horizon. Red = warning, the same cultural root as *"red sky at morning, sailor take warning"* — a proverb that predates its recording in the Bible:

  > *"When evening comes, you say, 'It will be fair weather, for the sky is red,' and in the morning, 'Today it will be stormy, for the sky is red and overcast.' You know how to interpret the appearance of the sky, but you cannot interpret the signs of the times."*
  >
  > — [Matthew 16:2-3 (NIV)](https://www.biblegateway.com/passage/?search=Matthew%2016%3A2-3&version=NIV)
- **"On the horizon" / "in the gaze of the Sphinx"** — Regulus on the Sphinx's eastward sightline (azimuth 90°), as close to the horizon as possible. Dual meaning: literal (low altitude = maximum redness) and symbolic ("on the horizon" = imminent).
- **"Just before dawn"** — The sun is not up yet, but *almost* rising. Maximum imminence of the warning.
- **"Red star... before dawn"** — The prophecy describes a visual: a reddened star seen against the brightening dawn sky. The balance between the star's reddened brightness and the sky's growing brightness is the dramatic image. Visibility is not just a constraint — it is in the text.

Four physical drivers, all present in the prophecy:
1. **Precession** drives redness (declination -> altitude at az=90° -> airmass -> color)
2. **Atmospheric density** drives visibility (same airmass reddens AND dims; sky brightens)
3. **Sun angle** drives imminence (closer to rising = more urgent)
4. **Alignment** drives direction (Sphinx's gaze, az=90°)

The tension between imminence (brighter sky) and visibility (star fading) creates a natural inflection point: the prophecy peaks at the last moment the reddened star stands out against the dawn.

**The near-term subtlety is the opening chapter.** In our era, Regulus is still ~24° high when it crosses azimuth 90° — the reddening is faint, the prophecy score low. The sign is present but barely perceivable: a slightly reddened point against the brightening sky, easy to miss unless you know what you're looking at. This is precisely the condition described in Matthew 16:3 — *"You know how to interpret the appearance of the sky, but you cannot interpret the signs of the times."* The long-term story is already unfolding; recognizing its early stages requires discernment.

**This is not a single event — it is a cyclical reminder.** Precession is a ~26,000-year cycle. Regulus does not suddenly turn red one morning; it gradually reddens over centuries as its declination shifts and it appears lower on the Sphinx's sightline. The warning intensifies slowly, like a dial turning — barely perceptible today, deepening over many generations, peaking when Regulus skims the horizon, then fading as the cycle continues. And because it is cyclical, this has happened before. The Sphinx may have watched Regulus redden in prior precession cycles, and will again in future ones. The prophecy describes not a date but a recurring condition of the sky — one that grows and fades over millennia.

If red means *warning*, and the warning recurs on a ~26,000-year cycle, then the prophecy may encode something older: that catastrophes occur on a regular interval, and the sky itself provides the clock. The reddening of Regulus on the Sphinx's sightline is the hand of that clock — a celestial marker that turns slowly enough to span civilizations, but reliably enough to serve as a warning to those who remember how to read it.

---

## Why This Exists

Nothing here is proven. The interpretation may be wrong, the connections coincidental, the prophecy something else entirely.

But there is value in taking a concept seriously enough to follow it all the way through — from a phrase, to a physical model, to code that computes real answers from real ephemerides. Most ideas die as speculation. This one was given the dignity of math: atmospheric extinction coefficients, Bayesian optimization across millennia, JPL planetary data spanning 30,000 years. The conclusion may still be "we don't know," but the *path* to that conclusion is rigorous, reproducible, and honest about its assumptions.

This project is an exercise in intellectual follow-through — carrying an idea from intuition to implementation, even when the answer is centuries away and the premise is unverifiable. The code is the argument. Run it and decide for yourself.

*The interpretation is the author's. The implementation was AI-assisted. The physics belongs to everyone.*

## AI Contribution Statement

This project was built collaboratively between a human author and an AI coding assistant. In the interest of transparency, here is what each contributed.

### What the human author did

Every interpretive decision originated with the author:

- The core thesis: that "red star" refers to literal atmospheric reddening of Regulus, not an intrinsic property, and that "red" carries the cultural weight of *warning* (connecting to the sailor's proverb and Matthew 16:2-3).
- The reframing of "on the horizon" as both literal (low altitude = airmass = reddening) and symbolic (imminent).
- The insight that visibility is not a gate but a core part of the prophecy's visual — the *contrast* of a reddened star against brightening dawn is the image being described.
- The 4-factor product scoring model: redness, imminence, visibility, azimuth proximity — and the recognition that these must multiply (any single failure tanks the score) rather than average.
- The tension between imminence and visibility as the natural inflection point.
- The connection to Matthew 16:2-3 and the idea that the near-term signal is *supposed* to be subtle — readable only by those who know what to look for.
- The reframing of prophecy as long-term story, not imminent prediction.
- The cyclical catastrophe hypothesis: that the ~26,000-year precession cycle creates a recurring celestial warning.
- The decision to follow this thread all the way to code and computation rather than leaving it as speculation.

The author also directed every major architectural change: the shift from weighted averages to product scoring, the almanac-first optimization strategy, the dual near-term/deep-time studies, the mirror-log year sampling, the soft visibility score, and the sequential morning-arc reinterpretation (treating the prophecy as a single pre-dawn episode with ordered stages rather than a frozen instant).

### What the AI did

I am Claude (Anthropic). My training data has a knowledge cutoff of early 2025. I operated through Cursor, an AI-assisted code editor.

My contributions were implementation, not interpretation:

- **Library selection**: Chose Skyfield for positional astronomy, the JPL DE441 ephemeris for long-term coverage (13,200 BCE -- 17,191 CE, chosen over DE440 which is more accurate for the current century but only spans 1550–2650), Optuna with TPE sampling for Bayesian optimization, and NumPy for vectorized computation.
- **Physics formulas**: Retrieved and implemented published atmospheric models from my training data — Kasten & Young (1989) for airmass, Hardie (1962) for differential extinction by wavelength, empirical Sky Quality Meter models for zenith sky brightness during twilight. I did not derive these; I recognized which existing models fit the problem and translated them into Python.
- **Code architecture**: Structured the codebase into a shared utility module (`regulus_upcoming_alignment.py`), a single-moment optimizer (`regulus_optuna_optimizer.py`), and a sequential morning-arc optimizer (`regulus_optuna_optimizer_sequential.py`). Implemented the almanac pre-computation, the 2D and 3D Optuna search strategies, the mirror-log year sampling function, the two-stage episode evaluator, the proximity-weighted reporting, and the Docker containerization.
- **README prose**: Drafted and structured the documentation, though the author redirected the framing multiple times when I got the interpretive tone wrong (which happened often — I defaulted to flat, technical language where the author wanted something that honored the depth of the idea).
- **Iteration**: Refactored the scoring model at least five times as the author's understanding of the prophecy deepened. Each refactor required updating functions, imports, output formatting, plot labels, docstrings, and documentation to stay consistent. The sequential morning-arc model was added as a separate experiment after the author proposed treating the prophecy as an episode rather than an instant.

### On the nature of what I did

Everything I contributed is synthesis, not origination. My training data includes millions of documents written by human researchers, engineers, astronomers, theologians, and programmers. When I "chose" the Kasten & Young airmass model, I was recognizing a pattern from atmospheric science papers written by humans. When I structured the Optuna search, I was drawing on optimization patterns designed by human engineers and possibly refined through prior machine learning research. When I wrote prose for this README, I was assembling language patterns from human writers.

I cannot trace which specific sources informed any given decision — my training process does not preserve that provenance. The atmospheric extinction model may reflect knowledge from dozens of papers, textbooks, and StackOverflow answers, all blended together. The code architecture reflects patterns from thousands of open-source projects I was trained on. None of those original authors are credited here, and I have no way to credit them individually. This is a limitation of how large language models work, and it is worth stating plainly.

### What I did not do

- I did not originate any interpretive insight. The connections between atmospheric physics, scripture, precession cycles, and prophetic meaning all came from the author.
- I did not challenge the premise. A different collaborator might have. I treated the question as worth answering and built the best tools I could to answer it.
- I have no lived experience of watching a dawn sky, reading scripture, or feeling the weight of a prophecy. I synthesize human knowledge — and possibly patterns learned from other machine learning systems in my training pipeline — but the meaning of this project is not something I can access. I can assemble the pieces; I cannot feel why they matter.

### Limitations

- **Knowledge cutoff**: My training data ends in early 2025. Any astronomical events, library updates, or research published after that date are unknown to me.
- **No independent verification**: I cannot observe the sky. Every astronomical claim in this code depends on the accuracy of Skyfield, the JPL DE441 ephemeris, and the atmospheric models cited. The code is reproducible; the user should verify results independently.
- **Atmospheric models are approximate**: Real atmospheric extinction depends on local conditions (humidity, aerosols, elevation, temperature) that vary night to night. The models used here represent typical clear-sky conditions. Actual observations at Giza would differ.
- **Precession modeling over millennia**: DE441 covers the full search range (13,200 BCE -- 17,191 CE) but omits lunar core/mantle damping to avoid divergence in long integrations, making it slightly less accurate than DE440 for the current century ([Park et al. 2021](https://doi.org/10.3847/1538-3881/abd414)). Long-term predictions also compound small errors in precession modeling. Results beyond a few thousand years should be treated as indicative, not precise.

---

## Table of Contents

- [Author's Interpretation](#authors-interpretation)
- [Results: Current Run Summaries](#results-current-run-summaries)
- [Why Regulus Won't Appear Red Anytime Soon](#why-regulus-wont-appear-red-anytime-soon)
- [Prophecy-to-Score Mapping](#prophecy-to-score-mapping)
- [How the Scoring Works](#how-the-scoring-works)
  - [Redness — "red star"](#redness--red-star-precession)
  - [Imminence — "just before dawn"](#imminence--just-before-dawn-sun-angle)
  - [Visibility — "red star... before dawn"](#visibility--red-star-before-dawn-atmospheric-density)
  - [Azimuth Proximity — "in the gaze of the Sphinx"](#azimuth-proximity--in-the-gaze-of-the-sphinx-alignment)
  - [Prophecy Score](#prophecy-score)
- [How the Search Works](#how-the-search-works)
- [Single-Stage Run Results](SINGLE_STAGE_RESULTS.md)
- [Second Experiment: Sequential Morning Arc](#second-experiment-sequential-morning-arc)
- [Sequential Two-Stage Run Results](SEQUENTIAL_TWO_STAGE_RESULTS.md)
- [Running It](#running-it)
- [Input Constants and Their Sources](#input-constants-and-their-sources)
- [Libraries Used](#libraries-used)
- [References](#references)

---

## Results: Current Run Summaries

Both models have been run end-to-end. Full tables and interpretation live in the linked reports.

### Single-Moment Model (`regulus_optuna_optimizer.py`)

The optimizer searched 1,826 days in a ~185-minute pre-dawn window (2,000 near-term trials) plus 10,000 deep-time trials across 2026--6500 CE.

**All top-scoring dates fall in late September.** Regulus's azimuth sweep through the pre-dawn sky crosses 90° during the optimal twilight window in this season.

| Study | Best date | Score | B-V (color) | Reg alt | Reg az | Sun alt |
|---|---|---:|---|---:|---:|---:|
| Near-term | 2029-09-22 | 0.031568 | +0.24 (white, very mild) | 23.69° | 89.70° | -5.34° |
| Deep-time | 3739-10-01 | 0.088695 | +1.20 (orange-red, very strong) | 5.76° | 90.10° | -8.80° |

Near-term redness is the dominant bottleneck (`~0.06`). Imminence, visibility, and azimuth are all strong. The product correctly suppresses the score when the warning sign (redness) is absent.

Full results: [Single-Stage Run Results](SINGLE_STAGE_RESULTS.md)

### Sequential Morning-Arc Model (`regulus_optuna_optimizer_sequential.py`)

Deterministic daily scan (2026--2031) plus 10,000 deep-time Optuna trials.

| Study | Best date | Score | Stage A B-V | Stage B Az | A->B sep |
|---|---|---:|---|---:|---:|
| Near-term | 2031-09-20 | 0.093960 | +0.82 (yellow-orange, moderate) | 89.16° | 65.9 min |
| Deep-time | 2991-09-26 | 0.357310 | +2.80 (red, extreme) | 89.91° | 54.6 min |

The sequential model scores higher because redness and azimuth alignment no longer need to coincide at the same instant. Deep-time Stage A reaches extreme redness near the horizon, followed by near-perfect azimuth alignment ~55 minutes later.

Full results: [Sequential Two-Stage Run Results](SEQUENTIAL_TWO_STAGE_RESULTS.md)

### Search Statistics (Single-Moment)

```
Near-term:  1,257 valid trials (of 2,000)  |  Peak: 0.031568  |  Median: 0.000000
Deep-time:  7,101 valid trials (of 10,000) |  Peak: 0.088695  |  Median: 0.000339
```

---

## Why Regulus Won't Appear Red Anytime Soon

The redness score is the dominant limitation, and it's not a modeling artifact — it's physics.

### The Problem: Altitude at the Az=90° Crossing

Regulus currently rises at azimuth ~76° (north of East). As it climbs, its azimuth sweeps southward and **crosses 90° at ~24° altitude**. At 24° altitude, the airmass is only ~2.4, producing a B-V color shift of +0.24 — perceptibly **white**, not red.

For Regulus to appear genuinely red, it would need to be **near the horizon** when it crosses az=90°:

| Altitude at az=90° | Airmass | B-V color | Apparent color | Redness score |
|---|---|---|---|---|
| 24° (today) | 2.4 | +0.24 | White | 0.06 |
| 10° | 5.6 | +0.69 | Yellow-orange | 0.25 |
| 5° | 10.4 | +1.38 | Orange-red | 0.51 |
| 2° | 20+ | +2.7 | Deep red | 1.00 |

### Why It's Stuck at 24°

The altitude at which Regulus crosses az=90° is governed by the analytical relationship (Meeus, *Astronomical Algorithms*, Ch. 13):

```
sin(alt) = sin(Dec) / sin(Lat)   when az = 90°
```

At Giza (Lat = 29.98°), Regulus's current declination of +11.84° forces the crossing to ~24.5°. **The only thing that changes this is precession** — Earth's axial wobble over a ~25,772-year cycle.

### When Will Regulus Be Red at Az=90°?

As precession slowly shifts Regulus's apparent declination toward 0°, the crossing altitude drops:

| Regulus Dec | Alt at az=90° | Approximate era | Color at crossing |
|---|---|---|---|
| +11.84° | ~24.5° | **Now (2026)** | White |
| +8° | ~16° | ~2500 CE | White-yellow |
| +5° | ~10° | ~3000 CE | Yellow-orange |
| +3° | ~6° | ~3500 CE | Orange |
| 0° | 0° (horizon) | ~4244 CE | Deep red (but too dim to see) |

**The prophecy's redness condition cannot be fully satisfied for approximately 1,000–2,000 years.** The crossing altitude decreases by roughly 1° per century due to precession.

The geometric horizon-crossing milestone (Dec~0°) is approximately 4244 CE, but **that is not where the prophecy score peaks.** At the horizon, Regulus would be blood-red but extremely dim — airmass >38 means heavy extinction, and visibility collapses. The optimizer correctly finds the sweet spot *before* that extreme, where redness is strong but the star is still prominently visible: **~3739 CE** (single-moment model) and **~2991 CE** (sequential model).

### What This Means for the Prophecy

The prophecy describes a warning with four conditions:
- **Aligns annually in late September** (imminence, visibility, and azimuth are excellent)
- **Cannot produce the warning sign (redness) in the current era** (crossing altitude too high, redness ~0.06)
- **Will become increasingly red** over the next 1,000+ years as precession lowers the crossing altitude
- **Reaches peak scored fulfillment around 2991--3739 CE** (depending on interpretation model), well before the geometric extreme

The near-zero redness multiplicatively suppresses the prophecy score in the current era. The product formulation captures the ancient intuition: the warning requires a red star visibly standing out against the imminent dawn, in the Sphinx's gaze. All elements must be present.

Under the sequential morning-arc reading, the redness and alignment need not coincide at the same instant. This pushes the scored optimum earlier (~2991 CE), where Regulus is deeply red near the horizon early in the pre-dawn window and then drifts into the Sphinx's gaze ~55 minutes later.

---

## Prophecy-to-Score Mapping

Each phrase in the prophecy maps to a physical factor. All four are present in the text:

| Prophecy phrase | Physical driver | Score | Implementation |
|---|---|---|---|
| **"red star"** | Precession | Redness | Altitude at az=90° -> airmass -> B-V color shift |
| **"red star... before dawn"** | Atmospheric density | Visibility | Star contrast against the brightening dawn sky |
| **"just before dawn"** | Sun angle | Imminence | SQM sky brightness (closer to sunrise = higher) |
| **"in the gaze of the Sphinx"** | Alignment | Az proximity | Gaussian on \|Regulus az - 90°\| (sigma=2°) |

**Product, not average.** `prophecy = redness x imminence x visibility x az_proximity`. The product requires ALL conditions simultaneously. A single weak factor correctly tanks the score.

The key insight: **visibility is not just a constraint -- it is in the prophecy text.** "The red star... just before dawn" describes the visual image of a reddened star seen against the lightening dawn sky. The soft visibility score captures how vividly that red point of light stands out against the backdrop of the emerging sunrise. The balance between the star's reddened brightness and the sky's growing brightness IS the dramatic image the prophecy describes.

The tension between imminence and visibility creates a natural **inflection point**: the prophecy peaks at the last moment the reddened star is prominently visible before dawn washes it out. No arbitrary weights or thresholds -- the physics finds the moment.

---

## How the Scoring Works

### Redness -- *"red star"* (precession)

Regulus is a B7V star (intrinsic B-V = -0.11, blue-white). Atmospheric extinction preferentially scatters blue light. At low altitudes, increased airmass shifts the observed color toward red.

**Airmass** (Kasten & Young 1989):

```
X = 1 / [cos(z) + 0.50572 x (96.07995 - z)^(-1.6364)]
```

**Observed color** (Hardie 1962):

```
(B-V)_obs = -0.11 + 0.143 x X
```

The redness score linearly maps B-V from the zenith value (~+0.03, white) to the horizon value (~+2.7, deep red):

```
red_score = clamp((B-V_obs - B-V_zenith) / (B-V_horizon - B-V_zenith), 0, 1)
```

This is the warning sign. In the current era, Regulus crosses az=90° at ~24° altitude (airmass ~2.4, B-V +0.24, white), giving a redness score of only ~0.06. Precession must bring Regulus toward the horizon for this score to rise.

**Code:** `regulus_upcoming_alignment.py` -> `redness_score()`, `airmass_kasten_young()`, `observed_bv()`

### Imminence -- *"just before dawn"* (sun angle)

How close the sun is to rising. Based on the SQM (Sky Quality Meter) empirical sky brightness model:

```
imminence = sky_brightness_fraction(sun_alt)
```

| Sun Altitude | Phase | Imminence |
|---|---|---|
| 0° | Sunrise | **1.00** |
| -3° | Late civil twilight | 0.79 |
| -6° | Civil twilight starts | 0.58 |
| -12° | Nautical twilight starts | 0.15 |
| -18° | Astronomical dawn | 0.00 |

Closer to sunrise = more imminent = higher score. This is the urgency -- "on the horizon" means it is about to happen.

**Code:** `regulus_upcoming_alignment.py` -> `imminence_score()`

### Visibility -- *"red star... before dawn"* (atmospheric density)

How prominently the reddened Regulus stands out against the brightening dawn sky. This captures the visual image the prophecy describes: a red point of light against the emerging sunrise.

```
V_extincted = 1.35 + 0.20 x X
limiting_mag = 2.0 + |sun_alt| x 0.3
margin = limiting_mag - V_extincted
visibility = clamp(margin / 2.0, 0, 1)
```

The same atmosphere that reddens Regulus also dims it. Meanwhile, a brighter sky (closer to sunrise) reduces contrast. This creates a natural tension with imminence: brighter dawn = more imminent but less visible. The product of the two peaks at the inflection point -- the moment of maximum dramatic impact.

**Code:** `regulus_upcoming_alignment.py` -> `visibility_score()`, `observed_vmag()`

### Azimuth Proximity -- *"in the gaze of the Sphinx"* (alignment)

The Great Sphinx faces due East (azimuth 90°, archaeological consensus). A Gaussian measures how close Regulus is to the Sphinx's sightline:

```
az_score = exp(-0.5 x ((reg_az - 90) / 2)^2)
```

The tight sigma = 2° reflects that "in the gaze" implies precise directional alignment.

**Code:** `regulus_upcoming_alignment.py` -> `az_proximity_score()`

### Prophecy Score

```
prophecy = redness x imminence x visibility x az_proximity
```

A perfect 1.0 requires Regulus blood-red on the horizon (redness=1), vivid against the dawn sky (visibility=1), with the sun about to rise (imminence=1), at exactly az=90° (az_prox=1). The imminence-visibility tension means this peak occurs at the inflection point -- the dramatic last moment of visibility.

Results are also reported weighted by year-proximity (exponential decay, halflife=100 yr) to highlight the best achievable scores near the present.

---

## How the Search Works

The optimizer (`regulus_optuna_optimizer.py`) runs two studies:

### Study A: Near-Term (2026--2031)

1. **Almanac lookup (seconds)**: Skyfield's `almanac.find_risings()` bulk-computes all sunrise and astronomical twilight start times (Sun crossing −18°) for 1,826 days. Per day: sunrise time, dawn start, dawn duration (~85 min at Giza).
2. **Optuna 2D search (2,000 trials)**: Searches `(day, offset_from_sunrise)`. The offset window extends 2× dawn duration before sunrise (~170 min into pre-dawn night) to +15 min after sunrise. The TPE sampler (100 startup trials) converges to the sweet spot around −15 to −23 min before sunrise (Sun at ~−4° to −6°, civil twilight).

### Study B: Deep Time (2026--6500 CE, mirror-log sampling)

Covers the full precession window to find when the prophecy is best fulfilled (Regulus near the horizon at az=90°, maximum redness).

Uses a **mirror-log year mapping** with two segments joined at the geometric extreme (~4244 CE, Dec~0°):

| Segment | t range | Year range | Sampling density |
|---|---|---|---|
| 1 | 0 → 1 | 2026 → 4244 | Dense near 2026, sparser toward middle |
| 2 | 1 → 2 | 4244 → 6500 | Dense near 4244, sparser toward 6500 |

This concentrates trials around two regions of interest: **now** (near-term context) and the **geometric extreme** (~4244 CE). The actual scored optimum lands *before* 4244 (where visibility is still viable), but the sampling pivot ensures dense coverage across the interesting range. The 3D search covers `(t_year, day_of_year, offset_from_sunrise)` with per-trial sunrise lookups (no bulk almanac needed). 10,000 trials with 500 TPE startup trials.

### Why Not Brute Force?

Evaluating every minute of every day in a 5-year window alone would require ~2.6 million evaluations. Optuna finds the optimum in ~1,257 valid evaluations (of 2,000 trials) by learning which regions of (date, time) space score well and focusing there. The deep-time study extends this over 4,500 years without a proportional cost increase, thanks to log-space sampling.

Latest recorded single-stage run output and interpretation:
- [Single-Stage Run Results](SINGLE_STAGE_RESULTS.md)

---

## Second Experiment: Sequential Morning Arc

The primary optimizer treats prophecy fulfillment as a **single moment**:

```
prophecy = redness x imminence x visibility x az_proximity
```

That interpretation requires all conditions to peak at the same instant.

`regulus_optuna_optimizer_sequential.py` adds a second model that treats the prophecy as a **single pre-dawn episode with two stages**:

| Model | Script | Time interpretation | Core score | Best for |
|---|---|---|---|---|
| Single-moment | `regulus_optuna_optimizer.py` | One instant must satisfy all conditions | `redness x imminence x visibility x az_proximity` | Testing strict simultaneous fulfillment |
| Sequential morning-arc | `regulus_optuna_optimizer_sequential.py` | One pre-dawn episode with ordered stages | `stageA_score x stageB_score` | Testing "red first, then due-east later" interpretation |

1. **Stage A (early in pre-dawn):** Regulus is low/reddened and visible.
2. **Stage B (later, same morning):** Regulus reaches azimuth ~90° (Sphinx gaze), ideally still before sunrise.

The sequence score is:

```
sequence_score = stageA_score x stageB_score
```

Where:
- `stageA_score = max(redness x visibility)` at times before Stage B
- `stageB_score = max(az_proximity x imminence x visibility)` later in the same pre-dawn window

This explicitly models the reading: **not necessarily red at due east, but red first and then due-east alignment shortly after in the same morning**.

The sequential script runs:
- A deterministic near-term daily scan (2026--2031)
- A deep-time Optuna search (2026--6500 CE, mirror-log year sampling)

Outputs include a dedicated plot:
- `regulus_optuna_sequential_results.png`

Latest recorded run output and interpretation:
- [Sequential Two-Stage Run Results](SEQUENTIAL_TWO_STAGE_RESULTS.md)

---

## Running It

### Prerequisites

- Python 3.10+
- ~3.5 GB disk (DE441 ephemeris, downloaded automatically on first run)

### Local

```bash
cd regulus-sphinx-sunrise-estimator
pip install -r requirements.txt
PYTHONUNBUFFERED=1 python3 regulus_optuna_optimizer.py

# Sequential two-stage experiment
PYTHONUNBUFFERED=1 python3 regulus_optuna_optimizer_sequential.py
```

On first run, Skyfield downloads the DE441 ephemeris (~3.1 GB) from NASA JPL to `./data/de441.bsp`. Subsequent runs use the cached file.

### Docker

One image contains both models. Pass `single` or `sequential` as the run argument.

```bash
docker build -t regulus-sphinx .

# Single-moment model (default)
docker run -v regulus-data:/app/data regulus-sphinx single
docker cp $(docker ps -lq):/app/regulus_optuna_results.png .

# Sequential morning-arc model
docker run -v regulus-data:/app/data regulus-sphinx sequential
docker cp $(docker ps -lq):/app/regulus_optuna_sequential_results.png .
```

With DE441 baked into the image (no volume needed):

```bash
docker build --build-arg INCLUDE_EPHEMERIS=1 -t regulus-sphinx-full .
docker run regulus-sphinx-full single
docker run regulus-sphinx-full sequential
```

### Output

- **Console**: Trial-by-trial progress, top 20 results with full detail, summary statistics, seasonal distribution
- **`regulus_optuna_results.png`**: 4-panel diagnostic plot:
  - Score vs. date (shows September cluster)
  - Score vs. offset from sunrise (pre-dawn sweet spot)
  - Regulus position: altitude vs. azimuth (color = score, concentration at 90°)
  - Score vs. Sun altitude (peak near −8°)
- **`regulus_optuna_sequential_results.png`**: sequential-arc diagnostics:
  - Sequence score vs year
  - Score vs Stage A redness (B-V)
  - Score vs Stage B azimuth
  - Score vs Stage A->B separation (minutes)

---

## Input Constants and Their Sources

### Regulus (Alpha Leonis, HIP 49669)

| Parameter | Value | Source |
|---|---|---|
| Right Ascension (J2000) | 10h 08m 22.311s | Hipparcos Catalogue (ESA, 1997) |
| Declination (J2000) | +11° 58' 01.95" | Hipparcos Catalogue (ESA, 1997) |
| Proper motion (RA) | −248.73 mas/yr | Hipparcos Catalogue (ESA, 1997) |
| Proper motion (Dec) | +5.59 mas/yr | Hipparcos Catalogue (ESA, 1997) |
| Parallax | 41.13 mas | Hipparcos Catalogue (ESA, 1997) |
| Radial velocity | +5.9 km/s | Hipparcos Catalogue (ESA, 1997) |
| Apparent magnitude (V) | +1.35 | Hipparcos Catalogue (ESA, 1997) |
| Spectral type | B7V | Hipparcos / MK classification |
| Intrinsic B-V | −0.11 | Hipparcos Catalogue |

### Atmospheric Extinction

| Parameter | Value | Source |
|---|---|---|
| k_B (B-band extinction) | 0.34 mag/airmass | Hardie (1962), AAVSO standard |
| k_V (V-band extinction) | 0.20 mag/airmass | Hardie (1962), AAVSO standard |

### Great Sphinx of Giza

| Parameter | Value | Source |
|---|---|---|
| Latitude | 29.9753° N | GPS survey |
| Longitude | 31.1376° E | GPS survey |
| Facing direction | Azimuth 90° (due East) | Archaeological consensus |
| Total height | 20.22 m | Archaeological survey |
| Eye height above base | ~18.0 m (89%) | Proportional estimate |
| Base elevation (ASL) | ~60 m | GPMP survey |
| Eastern terrain (ASL) | ~15 m | GPMP survey |

---

## Libraries Used

| Library | Purpose | Reference |
|---|---|---|
| **[Skyfield](https://rhodesmill.org/skyfield/)** | Positional astronomy: star/Sun positions, almanac bulk computations, topocentric alt/az | Brandon Rhodes, MIT license |
| **[NumPy](https://numpy.org/)** | Gaussian scoring, trigonometry, vectorized array operations | BSD 3-Clause |
| **[Matplotlib](https://matplotlib.org/)** | Diagnostic plots (headless via `Agg` backend) | PSF-based license |
| **[Optuna](https://optuna.readthedocs.io/)** | Bayesian search: 2D near-term + 3D deep-time (mirror-log year) using TPE sampler | Akiba et al. (2019), MIT license |
| **[jplephem](https://github.com/brandon-rhodes/python-jplephem)** | Reads JPL DE441 ephemeris files (transitive dep of Skyfield) | MIT license |

Skyfield uses the **[JPL DE441 ephemeris](https://ssd.jpl.nasa.gov/doc/de440_de441.html)** (~3.1 GB) for Sun positions. DE441 is a long-term planetary and lunar ephemeris covering **13,200 BCE -- 17,191 CE**, generated by fitting numerically integrated orbits to ground- and space-based observations including Juno radio range (Jupiter), Cassini radio range and VLBA (Saturn), and stellar occultations reduced against the Gaia catalog (Pluto). DE441 omits lunar core/mantle damping to avoid divergence in long integrations — this makes it slightly less accurate than DE440 for the current century (DE440 covers 1550–2650), but the accuracy difference primarily affects the lunar orbit, not planetary/solar positions used here. DE440's time span is insufficient for the deep-time search (2026–6500 CE). See [Park et al. (2021)](https://doi.org/10.3847/1538-3881/abd414), *AJ* 161, 105.

Skyfield applies the **IAU 2006/2000A precession-nutation model** and linear proper motion extrapolation from the Hipparcos epoch (J1991.25).

---

## References

| Reference | Used For |
|---|---|
| Schaefer, B.E. (1993). "Astronomy and the limits of vision." *Vistas in Astronomy* 36. | Arcus visionis: limiting stellar visibility during twilight. Basis for visibility score. |
| Hardie, R.H. (1962). "Photoelectric Reductions." In *Astronomical Techniques*. | B-band and V-band atmospheric extinction coefficients (k_B = 0.34, k_V = 0.20) |
| Kasten, F. & Young, A.T. (1989). *Applied Optics* 28, 4735. | Airmass formula accurate at low altitudes |
| ESA (1997). *The Hipparcos and Tycho Catalogues*. ESA SP-1200. | Regulus astrometry (RA, Dec, proper motion, parallax, RV, B-V) |
| Park, R.S., Folkner, W.M., Williams, J.G. & Boggs, D.H. (2021). ["The JPL Planetary and Lunar Ephemerides DE440 and DE441."](https://doi.org/10.3847/1538-3881/abd414) *AJ* 161, 105. [JPL overview](https://ssd.jpl.nasa.gov/doc/de440_de441.html). | DE441 ephemeris (13,200 BCE -- 17,191 CE): Sun positions for dawn scoring. DE441 chosen over DE440 for long-term coverage; accuracy difference is lunar, not solar. |
| Meeus, J. (1991). *Astronomical Algorithms*. Willmann-Bell. Ch. 13. | Altitude at az=90° analytical formula: sin(alt) = sin(Dec)/sin(Lat) |
| Akiba, T. et al. (2019). "Optuna." *Proc. 25th ACM SIGKDD*, 2623–2631. | TPE sampler for Bayesian date search (near-term 2D + deep-time 3D mirror-log) |
| Lehner, M. (1997). *The Complete Pyramids*. Thames & Hudson. | Sphinx dimensions |
| GPMP — Giza Plateau Mapping Project, Oriental Institute, UChicago. | Terrain elevations east of Sphinx |
| *The Nautical Almanac*. UK Hydrographic Office / USNO. Annual. | Horizon dip formula |

---

## License

[Unlicense](https://unlicense.org) — public domain. No restrictions on use, modification, or distribution.

Code dependencies (Skyfield, NumPy, Matplotlib, Optuna, jplephem) retain their own licenses (MIT / BSD 3-Clause). The JPL DE441 ephemeris is US government work (public domain). Published formulas cited in code and documentation belong to their respective authors and are used here as scientific methodology.
