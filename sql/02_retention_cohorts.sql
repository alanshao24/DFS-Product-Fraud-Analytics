-- PRODUCT ANALYTICS: D1/D7 retention, observed first-session logins by signup cohort.
-- Matured cohorts only: exclude recent signups without a full seven-day window.
WITH eligible AS (
    SELECT user_id, acquisition_channel, date(signup_ts) AS signup_date
    FROM users WHERE signup_ts < '2026-09-24 00:00:00'
), active_days AS (
    SELECT DISTINCT user_id, date(event_ts) AS active_date
    FROM events WHERE event_type = 'session_start'
), retention AS (
    SELECT e.user_id, e.acquisition_channel,
           MAX(CASE WHEN julianday(a.active_date) - julianday(e.signup_date) = 1
                    THEN 1 ELSE 0 END) AS returned_d1,
           MAX(CASE WHEN julianday(a.active_date) - julianday(e.signup_date) = 7
                    THEN 1 ELSE 0 END) AS returned_d7
    FROM eligible e
    LEFT JOIN active_days a ON a.user_id = e.user_id
    GROUP BY e.user_id, e.acquisition_channel
)
SELECT acquisition_channel, COUNT(*) AS users,
       SUM(returned_d1) AS day1_returned,
       SUM(returned_d7) AS day7_returned,
       ROUND(100.0 * SUM(returned_d1) / COUNT(*), 2) AS day1_retention_pct,
       ROUND(100.0 * SUM(returned_d7) / COUNT(*), 2) AS day7_retention_pct
FROM retention GROUP BY acquisition_channel ORDER BY day7_retention_pct DESC;
