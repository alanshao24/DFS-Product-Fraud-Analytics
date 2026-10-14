# SQL learning lab: complete before adding SQL to your resume

Work with `data/dfs_analytics.sqlite` via Python's built-in `sqlite3` module. The six completed SQL analyses in `sql/` are references; try these three yourself first.

## Exercise 1 (15 min): basic metrics

Count users in each acquisition channel with `SELECT`, `COUNT(*)`, `GROUP BY`, `ORDER BY`. Answer: which channel has the most synthetic users?

## Exercise 2 (20 min): join + aggregation

Join `users` with `payments`. Calculate the number of unique users with a successful deposit by A/B experiment variant. Be careful: a payment table has multiple rows per user, so use `COUNT(DISTINCT ...)` to avoid inflating a user-level metric.

## Exercise 3 (25 min): window functions

Write a CTE that uses `ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY payment_ts)` to find each user's first successful deposit. Then join to users and calculate the first-deposit rate.

## Exercise 4 (20 min): suspicious activity

Without referencing `synthetic_scenario`, find users who (a) used a device shared by at least three accounts and (b) redeemed at least three promos. Explain why these should trigger human review rather than automatic sanctions.

## Exercise 5 (20 min): false positives

Open `sql/04_flag_evaluation.sql`; explain TP, FP, FN and TN. Which two metrics are in tension when changing rule thresholds? Note: the synthetic test label is **planted**, not real fraud ground truth.

## Exercise 6 (20 min): retention

Reproduce seven-day user retention using `session_start` events. Why is it misleading to include users who signed up within the last seven days?

## How to practice a query interactively

Open a Mac Terminal from this folder and enter:

```bash
python3
```

Then:

```python
import sqlite3
conn = sqlite3.connect('data/dfs_analytics.sqlite')
print(conn.execute("SELECT acquisition_channel, COUNT(*) FROM users GROUP BY acquisition_channel").fetchall())
```

`conn.execute("...SQL...").fetchall()` runs your query. Type `exit()` to leave Python.

## Put this on your resume only after you can explain it

Discuss database schema and join grain; conversion funnels and cohort eligibility; window functions; fraud signal precision vs recall; difference between synthetic planted labels and real fraud investigations.
