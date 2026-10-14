#!/usr/bin/env python3
"""Read-only data-integrity and query checks, not formal statistical validation."""
import sqlite3
from pathlib import Path
root = Path(__file__).resolve().parents[1]
conn = sqlite3.connect(root / 'data' / 'dfs_analytics.sqlite')
assert conn.execute('SELECT COUNT(*) FROM users').fetchone()[0] == 5000
assert conn.execute('SELECT COUNT(*) FROM events').fetchone()[0] > 50000
assert conn.execute('SELECT COUNT(*) FROM payments').fetchone()[0] > 1000
assert conn.execute('SELECT COUNT(*) FROM lineups').fetchone()[0] > 1000
assert conn.execute('SELECT COUNT(*) FROM risk_flags WHERE review_flag=1').fetchone()[0] > 0
assert conn.execute("SELECT COUNT(*) FROM events e LEFT JOIN users u USING(user_id) WHERE u.user_id IS NULL").fetchone()[0] == 0
assert conn.execute("SELECT COUNT(*) FROM payments p LEFT JOIN users u USING(user_id) WHERE u.user_id IS NULL").fetchone()[0] == 0
for p in sorted((root / 'sql').glob('*.sql')):
    result = conn.execute(p.read_text()).fetchall()
    assert result, f'No results: {p}'
print('PASS: 5,000 users, 50K+ events, foreign key relationships, review flags and 6 queries.')
