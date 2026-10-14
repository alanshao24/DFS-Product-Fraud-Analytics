-- PRODUCT ANALYTICS: simulated onboarding A/B variants; descriptive rates, not proof of effect.
WITH first_deposits AS (
    SELECT user_id, MIN(payment_ts) AS first_payment_ts
    FROM payments WHERE status = 'success' GROUP BY user_id
), first_lineups AS (
    SELECT user_id, MIN(lineup_ts) AS first_lineup_ts FROM lineups GROUP BY user_id
)
SELECT u.experiment_variant, COUNT(*) AS signups,
       SUM(CASE WHEN d.first_payment_ts >= u.signup_ts
                 AND d.first_payment_ts < datetime(u.signup_ts, '+7 days') THEN 1 ELSE 0 END) AS deposited_7d,
       SUM(CASE WHEN l.first_lineup_ts >= d.first_payment_ts
                 AND l.first_lineup_ts < datetime(u.signup_ts, '+7 days') THEN 1 ELSE 0 END) AS entered_lineup_7d,
       ROUND(100.0 * SUM(CASE WHEN d.first_payment_ts >= u.signup_ts
                 AND d.first_payment_ts < datetime(u.signup_ts, '+7 days') THEN 1 ELSE 0 END)
             / COUNT(*), 2) AS deposit_rate_pct
FROM users u
LEFT JOIN first_deposits d ON u.user_id = d.user_id
LEFT JOIN first_lineups l ON u.user_id = l.user_id
WHERE u.signup_ts < '2026-09-24 00:00:00'
GROUP BY u.experiment_variant ORDER BY u.experiment_variant;
