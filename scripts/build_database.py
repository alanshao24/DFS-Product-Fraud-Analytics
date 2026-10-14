#!/usr/bin/env python3
"""Import generated CSVs into a local SQLite database with indexed tables."""
from pathlib import Path
import csv, sqlite3

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
DB = DATA / 'dfs_analytics.sqlite'

SCHEMA = '''
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_ts TEXT NOT NULL,
                   experiment_variant TEXT, acquisition_channel TEXT, device_id TEXT,
                   synthetic_scenario TEXT);
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, session_id TEXT,
                    event_type TEXT, event_ts TEXT);
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, user_id INTEGER, payment_ts TEXT,
                      amount_usd REAL, status TEXT);
CREATE TABLE lineups(lineup_id INTEGER PRIMARY KEY, user_id INTEGER, lineup_ts TEXT,
                     entry_fee_usd REAL, pick_count INTEGER);
CREATE TABLE promos(promo_id INTEGER PRIMARY KEY, user_id INTEGER, redeemed_ts TEXT,
                    promo_code TEXT, credit_usd REAL);
CREATE INDEX ix_events_user_ts ON events(user_id, event_ts);
CREATE INDEX ix_events_type_ts ON events(event_type, event_ts);
CREATE INDEX ix_payments_user_ts ON payments(user_id, payment_ts);
CREATE INDEX ix_lineups_user_ts ON lineups(user_id, lineup_ts);
CREATE INDEX ix_promos_user ON promos(user_id);
CREATE INDEX ix_users_device ON users(device_id);
'''

def main():
    if DB.exists():
        DB.unlink()
    conn = sqlite3.connect(DB)
    conn.executescript(SCHEMA)
    for table in ('users', 'events', 'payments', 'lineups', 'promos'):
        with (DATA / f'{table}.csv').open(newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            cols = next(reader)
            marks = ','.join(['?'] * len(cols))
            conn.executemany(f'INSERT INTO {table} VALUES ({marks})', reader)
        print(f'{table}: {conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]:,} rows imported')
    query = (ROOT / 'sql' / '03_fraud_flags.sql').read_text(encoding='utf-8').strip().rstrip(';')
    conn.execute(f'CREATE VIEW risk_flags AS {query}')
    conn.commit()
    conn.close()
    print('Database built:', DB)

if __name__ == '__main__':
    main()
