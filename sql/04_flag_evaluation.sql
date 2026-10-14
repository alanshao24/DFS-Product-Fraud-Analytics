-- Synthetic ONLY: evaluate heuristics against scenario labels planted by the generator.
-- Not validated on real-world fraud cases. Never treat a flag as proof of wrongdoing.
WITH classified AS (
    SELECT CASE WHEN u.synthetic_scenario = 'ordinary' THEN 0 ELSE 1 END AS planted_positive,
           f.review_flag
    FROM users u JOIN risk_flags f USING (user_id)
), matrix AS (
    SELECT SUM(CASE WHEN planted_positive = 1 AND review_flag = 1 THEN 1 ELSE 0 END) AS tp,
           SUM(CASE WHEN planted_positive = 0 AND review_flag = 1 THEN 1 ELSE 0 END) AS fp,
           SUM(CASE WHEN planted_positive = 1 AND review_flag = 0 THEN 1 ELSE 0 END) AS fn,
           SUM(CASE WHEN planted_positive = 0 AND review_flag = 0 THEN 1 ELSE 0 END) AS tn
    FROM classified
)
SELECT tp, fp, fn, tn,
       ROUND(100.0 * tp / NULLIF(tp + fp, 0), 2) AS precision_pct,
       ROUND(100.0 * tp / NULLIF(tp + fn, 0), 2) AS recall_pct,
       ROUND(100.0 * fp / NULLIF(fp + tn, 0), 2) AS false_positive_rate_pct
FROM matrix;
