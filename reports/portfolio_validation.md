# Synthetic DFS Portfolio — Statistical Validation

> **Synthetic data only.** The labels are planted, and this is not evidence of real fraud or customer lift.

## Fraud-review policy tradeoffs

| Policy | TP | FP | FN | TN | Flagged | Precision | Recall | FPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1_baseline | 357 | 91 | 2 | 4550 | 448 | 79.69% | 99.44% | 1.96% |
| 2_stricter_payments | 324 | 3 | 35 | 4638 | 327 | 99.08% | 90.25% | 0.06% |
| 3_stricter_devices | 357 | 88 | 2 | 4553 | 445 | 80.22% | 99.44% | 1.90% |
| 4_both_stricter | 297 | 0 | 62 | 4641 | 297 | 100.00% | 82.73% | 0.00% |

## Simulated onboarding experiment

| Metric | Control A | Treatment B | Difference | z | p-value | 95% CI of difference | Significant (5%) |
|---|---:|---:|---:|---:|---:|---:|---|
| 7-day deposit conversion | 55.48% | 61.90% | +6.42 pp | 4.366 | 0.000013 | [+3.54, +9.29] pp | Yes |
| 7-day first-lineup conversion | 35.88% | 37.93% | +2.04 pp | 1.419 | 0.156021 | [-0.78, +4.86] pp | No |

Two-sided pooled two-proportion z-test; approximate unpooled Wald confidence interval.
Interpret with care: synthetic population, independent-observation assumption, and no real-world causal inference.
