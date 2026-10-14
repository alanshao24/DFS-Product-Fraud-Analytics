SELECT
    CASE
        WHEN max_failed_payments_24h >= 3
            THEN 'Repeated payment failures'
        WHEN accounts_per_device >= 3
         AND promo_redemptions >= 3
            THEN 'Shared device + promo activity'
        ELSE 'Not flagged'
    END AS review_reason,

    COUNT(*) AS total_accounts,
    SUM(review_flag) AS flagged_accounts,

    ROUND(
        100.0 * SUM(review_flag) / COUNT(*),
        2
    ) AS review_rate_pct

FROM flags
GROUP BY review_reason
ORDER BY flagged_accounts DESC;
