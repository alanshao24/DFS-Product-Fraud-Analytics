# Synthetic DFS Product & Fraud Analytics Report

**All data is simulated. None is from PrizePicks or real users.**

## 01_conversion_funnel.sql

8 report rows. Export: `reports/01_conversion_funnel.csv`.

acquisition_channel: organic, experiment_variant: A, eligible_signups: 546, seven_day_depositors: 300, seven_day_lineup_users: 195, deposit_conversion_pct: 54.95, first_lineup_conversion_pct: 35.71
acquisition_channel: organic, experiment_variant: B, eligible_signups: 522, seven_day_depositors: 318, seven_day_lineup_users: 202, deposit_conversion_pct: 60.92, first_lineup_conversion_pct: 38.7
acquisition_channel: paid_search, experiment_variant: A, eligible_signups: 582, seven_day_depositors: 322, seven_day_lineup_users: 201, deposit_conversion_pct: 55.33, first_lineup_conversion_pct: 34.54


## 02_retention_cohorts.sql

4 report rows. Export: `reports/02_retention_cohorts.csv`.

acquisition_channel: referral, users: 1155, day1_returned: 560, day7_returned: 427, day1_retention_pct: 48.48, day7_retention_pct: 36.97
acquisition_channel: paid_search, users: 1146, day1_returned: 547, day7_returned: 418, day1_retention_pct: 47.73, day7_retention_pct: 36.47
acquisition_channel: social, users: 1123, day1_returned: 539, day7_returned: 404, day1_retention_pct: 48.0, day7_retention_pct: 35.98


## 03_fraud_flags.sql

5,000 report rows. Export: `reports/03_fraud_flags.csv`.

user_id: 1, device_id: device_000001, accounts_per_device: 1, promo_redemptions: 0, max_failed_payments_24h: 0, heuristic_risk_score: 0, review_flag: 0
user_id: 3, device_id: device_000003, accounts_per_device: 1, promo_redemptions: 0, max_failed_payments_24h: 0, heuristic_risk_score: 0, review_flag: 0
user_id: 4, device_id: device_000004, accounts_per_device: 1, promo_redemptions: 0, max_failed_payments_24h: 0, heuristic_risk_score: 0, review_flag: 0


## 04_flag_evaluation.sql

1 report rows. Export: `reports/04_flag_evaluation.csv`.

tp: 357, fp: 91, fn: 2, tn: 4550, precision_pct: 79.69, recall_pct: 99.44, false_positive_rate_pct: 1.96


## 05_payment_kpis.sql

61 report rows. Export: `reports/05_payment_kpis.csv`.

payment_day: 2026-08-01, payment_attempts: 3, succeeded: 2, failed: 1, success_pct: 66.67, successful_deposit_total_usd: 150.0
payment_day: 2026-08-02, payment_attempts: 43, succeeded: 27, failed: 16, success_pct: 62.79, successful_deposit_total_usd: 880.0
payment_day: 2026-08-03, payment_attempts: 73, succeeded: 42, failed: 31, success_pct: 57.53, successful_deposit_total_usd: 1400.0


## 06_onboarding_experiment.sql

2 report rows. Export: `reports/06_onboarding_experiment.csv`.

experiment_variant: A, signups: 2235, deposited_7d: 1240, entered_lineup_7d: 802, deposit_rate_pct: 55.48
experiment_variant: B, signups: 2257, deposited_7d: 1397, entered_lineup_7d: 856, deposit_rate_pct: 61.9

