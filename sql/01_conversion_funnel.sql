-- PRODUCT ANALYTICS: signup -> successful deposit -> DFS lineup within 7 days
-- Exclude users whose first 7 days have not yet completed in the synthetic period.
WITH first_deposit AS (
    SELECT user_id, payment_ts,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY payment_ts, payment_id) AS rn
    FROM payments WHERE status = 'success'
), first_lineup AS (
    SELECT user_id, lineup_ts,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY lineup_ts, lineup_id) AS rn
    FROM lineups
), cohort AS (
    SELECT u.user_id, u.acquisition_channel, u.experiment_variant,
           CASE WHEN d.payment_ts >= u.signup_ts
                  AND d.payment_ts < datetime(u.signup_ts, '+7 days') THEN 1 ELSE 0 END AS deposited_7d,
           CASE WHEN l.lineup_ts >= d.payment_ts
                  AND l.lineup_ts < datetime(u.signup_ts, '+7 days') THEN 1 ELSE 0 END AS lined_up_7d
    FROM users u
    LEFT JOIN first_deposit d ON d.user_id = u.user_id AND d.rn = 1
    LEFT JOIN first_lineup l ON l.user_id = u.user_id AND l.rn = 1
    WHERE u.signup_ts <= '2026-09-23 23:59:59'
)
SELECT acquisition_channel, experiment_variant,
       COUNT(*) AS eligible_signups,
       SUM(deposited_7d) AS seven_day_depositors,
       SUM(lined_up_7d) AS seven_day_lineup_users,
       ROUND(100.0 * SUM(deposited_7d) / NULLIF(COUNT(*), 0), 2) AS deposit_conversion_pct,
       ROUND(100.0 * SUM(lined_up_7d) / NULLIF(COUNT(*), 0), 2) AS first_lineup_conversion_pct
FROM cohort
GROUP BY acquisition_channel, experiment_variant
ORDER BY acquisition_channel, experiment_variant;
