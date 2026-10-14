SELECT
    u.acquisition_channel,
    COUNT(DISTINCT u.user_id) AS total_users,
    COUNT(DISTINCT CASE
        WHEN p.status = 'success' THEN u.user_id
    END) AS paying_users,
    ROUND(
        100.0 * COUNT(DISTINCT CASE
            WHEN p.status = 'success' THEN u.user_id
        END) / COUNT(DISTINCT u.user_id),
        2
    ) AS conversion_rate
FROM users u
LEFT JOIN payments p
    ON u.user_id = p.user_id
GROUP BY u.acquisition_channel
ORDER BY conversion_rate DESC;
