WITH labeled AS (
    SELECT
        u.user_id,
        CASE
            WHEN u.synthetic_scenario = 'ordinary'
            THEN 0 ELSE 1
        END AS actual_positive,
        f.accounts_per_device,
        f.promo_redemptions,
        f.max_failed_payments_24h,
        f.review_flag
    FROM users u
    JOIN risk_flags f
        ON u.user_id = f.user_id
),

policies AS (
    SELECT
        '1_baseline' AS policy,
        actual_positive,
        review_flag AS predicted
    FROM labeled

    UNION ALL

    SELECT
        '2_stricter_payments',
        actual_positive,
        CASE
            WHEN (
                accounts_per_device >= 3
                AND promo_redemptions >= 3
            )
            OR max_failed_payments_24h >= 4
            THEN 1 ELSE 0
        END
    FROM labeled

    UNION ALL

    SELECT
        '3_stricter_devices',
        actual_positive,
        CASE
            WHEN (
                accounts_per_device >= 4
                AND promo_redemptions >= 3
            )
            OR max_failed_payments_24h >= 3
            THEN 1 ELSE 0
        END
    FROM labeled

    UNION ALL

    SELECT
        '4_both_stricter',
        actual_positive,
        CASE
            WHEN (
                accounts_per_device >= 4
                AND promo_redemptions >= 4
            )
            OR max_failed_payments_24h >= 4
            THEN 1 ELSE 0
        END
    FROM labeled
),

metrics AS (
    SELECT
        policy,
        SUM(CASE
            WHEN actual_positive = 1 AND predicted = 1
            THEN 1 ELSE 0 END) AS tp,
        SUM(CASE
            WHEN actual_positive = 0 AND predicted = 1
            THEN 1 ELSE 0 END) AS fp,
        SUM(CASE
            WHEN actual_positive = 1 AND predicted = 0
            THEN 1 ELSE 0 END) AS fn,
        SUM(CASE
            WHEN actual_positive = 0 AND predicted = 0
            THEN 1 ELSE 0 END) AS tn
    FROM policies
    GROUP BY policy
)

SELECT
    policy,
    tp,
    fp,
    fn,
    tn,
    tp + fp AS total_flagged,
    ROUND(
        100.0 * tp / NULLIF(tp + fp, 0), 2
    ) AS precision_pct,
    ROUND(
        100.0 * tp / NULLIF(tp + fn, 0), 2
    ) AS recall_pct,
    ROUND(
        100.0 * fp / NULLIF(fp + tn, 0), 2
    ) AS false_positive_rate_pct
FROM metrics
ORDER BY policy;