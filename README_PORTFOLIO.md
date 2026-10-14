# DFS Product & Fraud Analytics | SQL Portfolio Project

**SQLite · SQL · Python · Product Analytics · Risk Analytics · Statistical Testing**

An end-to-end, reproducible analytics project simulating a Daily Fantasy Sports (DFS) platform. It connects user signup, session activity, payment attempts, submitted lineups, and promotional activity to study **acquisition funnels, 7-day conversion, user retention, onboarding experiments, fraud-review signals, and operational tradeoffs**.

> **Synthetic-data disclaimer:** All 5,000 users, transactions, events, experiments, account labels, and outcomes are simulated. This project is not affiliated with PrizePicks or Kalshi and does not use proprietary customer data. Fraud scenarios were planted by a data generator. The results are **not real-world fraud performance or product lift**, and no fraud conclusions are drawn about actual people.

## Highlights

| Category | SQL / analytical techniques | Result on synthetic data |
|---|---|---|
| Product acquisition | `JOIN`, `GROUP BY`, `COUNT(DISTINCT)`, time windows | 7-day deposit conversion: **59.51%** paid search; **59.48%** referrals |
| Retention | CTEs, session event deduplication, cohort maturation | Day-7 retention: **36.97%** referral vs **34.46%** organic |
| Fraud-review signals | `COUNT() OVER`, rolling 24-hour windows, device/promo joins | Baseline: **79.69%** precision; **99.44%** recall |
| Policy comparison | Four thresholds; confusion matrices; false-positive analysis | Stricter payment threshold cut false positives **91 → 3**, while recall fell **99.44% → 90.25%** |
| Onboarding experiment | SQL funnel metrics + two-proportion z-tests | Deposit conversion: **55.48% → 61.90%**, **+6.42 pp** (p = 0.000013); first-lineup conversion not significant (p = 0.156) |

**Interpretation:** The stricter fraud-review policy reduced simulated false positives but missed 33 additional planted suspicious accounts. The simulated onboarding treatment shows evidence of a difference in deposit conversion under standard test assumptions, not definitive improvement in first-lineup engagement or real-world causal impact.

## Data model

| Table | Grain | Business purpose |
|---|---|---|
| `users` | One record per synthetic account | Signup time, acquisition channel, experiment variant, device |
| `events` | One record per synthetic app event | Activity, sessions, retention analysis |
| `payments` | One record per payment attempt | Successful/failed payments; first deposit; risk signals |
| `lineups` | One record per lineup submission | First-lineup funnel conversion |
| `promos` | One record per promotion redemption | Promotional behavior and account-review signals |
| `risk_flags` | Derived SQL view, one row per account | Aggregated indicators and heuristic review decision |

The generated project contains **5,000 accounts, 119,122 activity events, 4,374 payment records, 4,580 lineups, and 3,702 promotion records**.

## Reproduce the analysis

Requires Python 3 and SQLite via Python's standard library. No secrets, paid APIs, external services, or dependencies are required.

```bash
cd dfs_product_fraud_sql
bash run_all.command
python3 scripts/portfolio_analysis.py
```

Read the generated reports in `reports/summary.md` and `reports/portfolio_validation.md`. All base SQL analyses are under `sql/`; the practice exercises are under `practice/`. `run_all.command` regenerates deterministic synthetic data and six primary reports; `portfolio_analysis.py` adds fraud-policy and statistical validation.

## How the analyses work

### 1. Acquisition & funnel analytics

Join users to payments and lineups by `user_id`, count distinct accounts to avoid duplication, and restrict conversion to a full 7-day post-signup window. The cohort eligibility cutoff avoids counting users who have not had enough observation time.

### 2. Day-1 and day-7 retention

Deduplicate `session_start` events into active dates; compare activity date with the signup date. This measures activity **on** Day 1 or Day 7, not cumulative activity within seven days.

### 3. Fraud risk and policy evaluation

Rule-based signals use multiple accounts per device, repeated promotional redemptions, and bursts of failed payments within a rolling 24-hour interval. These produce **review flags**, not proof of abuse. Compare the baseline with three stricter policies using precision, recall, false positives, and missed cases. The synthetic scenario labels are held out of the flag generation query and used only for evaluation.

| Policy | TP | FP | FN | Precision | Recall |
|---|---:|---:|---:|---:|---:|
| Baseline | 357 | 91 | 2 | 79.69% | 99.44% |
| Stricter failed payments | 324 | 3 | 35 | 99.08% | 90.25% |
| Stricter shared-device condition | 357 | 88 | 2 | 80.22% | 99.44% |
| Both stricter | 297 | 0 | 62 | 100.00% | 82.73% |

Changing the minimum failed-payment count from 3 to 4 reduced review workload from 448 to 327 accounts, but increased missed planted suspicious accounts from 2 to 35. No policy is universally best: operational cost and risk tolerance matter.

### 4. Simulated onboarding A/B analysis

Use seven-day post-signup funnel rates for eligible cohorts, then compute two-sided pooled two-proportion z-tests and unpooled approximate 95% confidence intervals.

| Metric | Control (A) | Treatment (B) | Difference | Two-sided p-value |
|---|---:|---:|---:|---:|
| 7-day first deposit | 1,240 / 2,235 (55.48%) | 1,397 / 2,257 (61.90%) | +6.42 pp | 0.000013 |
| 7-day first lineup | 802 / 2,235 (35.88%) | 856 / 2,257 (37.93%) | +2.04 pp | 0.156021 |

The approximate confidence interval for the deposit conversion difference is **+3.54 to +9.29 percentage points**. Results assume independent observations and a valid experiment assignment. The dataset is synthetic, and these comparisons do not establish real-world causal effects.

## Project structure

```text
dfs_product_fraud_sql/
├── scripts/
│   ├── generate_data.py
│   ├── build_database.py
│   ├── run_analysis.py
│   ├── smoke_test.py
│   └── portfolio_analysis.py      # Additional validation
├── sql/
│   ├── 01_conversion_funnel.sql
│   ├── 02_retention_cohorts.sql
│   ├── 03_fraud_flags.sql
│   ├── 04_flag_evaluation.sql
│   ├── 05_payment_kpis.sql
│   ├── 06_onboarding_experiment.sql
│   └── 07_fraud_policy_comparison.sql
├── practice/                     # Hands-on SQL exercises
├── reports/
│   ├── summary.md
│   └── portfolio_validation.md    # Reproducible findings
├── data/                          # Locally generated and gitignored
├── run_all.command
└── README.md
```

## Caveats and next steps

- This is a **learning and portfolio project**, not a production service or trained fraud-classification model.
- The generator intentionally produces patterns resembling the rules, so fraud metrics are optimistic and should not be generalized.
- More trustworthy real-world evaluation would require independent labeled cases, holdout testing, review costs, distribution drift monitoring, and bias/privacy considerations.
- Before using a real onboarding experiment, validate randomization, instrumentation, eligibility, exposure, guardrail metrics, and power; consider adjustment for multiple tests.
- An extension could analyze real, consented, non-sensitive user events (with privacy safeguards), implement a simple dashboard, or explore cohort-based segmentation.

## Interview-ready explanation

“I built a reproducible SQL analytics pipeline for a synthetic DFS platform using five relational tables. I analyzed acquisition and seven-day conversion with joins and deduplication, cohort retention with CTEs, and rolling payment-failure signals with SQL window functions. I compared four heuristic fraud-review policies using confusion matrices and precision-recall tradeoffs. I also evaluated a simulated onboarding A/B test using Python two-proportion z-tests, distinguishing statistical significance in deposit conversion from inconclusive first-lineup results.”
