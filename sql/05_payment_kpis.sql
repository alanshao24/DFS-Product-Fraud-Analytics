-- PRODUCT/FRAUD: daily successful and failed payments + amount of successful deposits.
SELECT date(payment_ts) AS payment_day,
       COUNT(*) AS payment_attempts,
       SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) AS succeeded,
       SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failed,
       ROUND(100.0 * SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) / COUNT(*), 2) AS success_pct,
       ROUND(SUM(CASE WHEN status = 'success' THEN amount_usd ELSE 0 END), 2) AS successful_deposit_total_usd
FROM payments GROUP BY date(payment_ts) ORDER BY payment_day;
