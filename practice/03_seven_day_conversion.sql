WITH ranked_deposits AS (
    SELECT
        user_id,
        payment_ts,
        ROW_NUMBER() OVER (
            PARTITION BY user_id
            ORDER BY payment_ts, payment_id
        ) AS rn
    FROM payments
    WHERE status = 'success'
),
eligible_users AS (
    SELECT
        user_id,
        acquisition_channel,
        signup_ts
    FROM users
    WHERE signup_ts <= '2026-09-23 23:59:59'
)
SELECT
    u.acquisition_channel,
    COUNT(*) AS eligible_signups,
    SUM(
        CASE
            WHEN d.payment_ts >= u.signup_ts
             AND d.payment_ts < datetime(
                 u.signup_ts, '+7 days'
             )
            THEN 1 ELSE 0
        END
    ) AS depositors_7d,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN d.payment_ts >= u.signup_ts
                 AND d.payment_ts < datetime(
                     u.signup_ts, '+7 days'
                 )
                THEN 1 ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS conversion_7d_pct
FROM eligible_users u
LEFT JOIN ranked_deposits d
    ON d.user_id = u.user_id
   AND d.rn = 1
GROUP BY u.acquisition_channel
ORDER BY conversion_7d_pct DESC;
