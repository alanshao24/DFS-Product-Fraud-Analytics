SELECT
    acquisition_channel,
    COUNT(*) AS total_users
FROM users
GROUP BY acquisition_channel
ORDER BY total_users DESC;