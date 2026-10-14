-- FRAUD ANALYTICS: heuristic ACCOUNT REVIEW flags, not proof of fraudulent activity.
-- No synthetic_scenario field may be used in this query: that's held out for evaluation.
WITH device_counts AS (
    SELECT device_id, COUNT(DISTINCT user_id) AS device_account_count
    FROM users GROUP BY device_id
), promo_counts AS (
    SELECT user_id, COUNT(*) AS promo_redemptions
    FROM promos GROUP BY user_id
), failed_payment_windows AS (
    SELECT user_id,
           COUNT(*) OVER (
               PARTITION BY user_id
               ORDER BY CAST(strftime('%s', payment_ts) AS INTEGER)
               RANGE BETWEEN 86400 PRECEDING AND CURRENT ROW
           ) AS failures_in_24h
    FROM payments WHERE status = 'failed'
), failed_payment_counts AS (
    SELECT user_id, MAX(failures_in_24h) AS max_failures_24h
    FROM failed_payment_windows GROUP BY user_id
), features AS (
    SELECT u.user_id, u.device_id,
           COALESCE(d.device_account_count, 1) AS accounts_per_device,
           COALESCE(p.promo_redemptions, 0) AS promo_redemptions,
           COALESCE(f.max_failures_24h, 0) AS max_failed_payments_24h
    FROM users u
    LEFT JOIN device_counts d ON d.device_id = u.device_id
    LEFT JOIN promo_counts p ON p.user_id = u.user_id
    LEFT JOIN failed_payment_counts f ON f.user_id = u.user_id
)
SELECT *,
       (CASE WHEN accounts_per_device >= 3 THEN 25 ELSE 0 END
        + CASE WHEN promo_redemptions >= 3 THEN 40 ELSE 0 END
        + CASE WHEN max_failed_payments_24h >= 3 THEN 45 ELSE 0 END) AS heuristic_risk_score,
       CASE WHEN (accounts_per_device >= 3 AND promo_redemptions >= 3)
                 OR max_failed_payments_24h >= 3 THEN 1 ELSE 0 END AS review_flag
FROM features;
