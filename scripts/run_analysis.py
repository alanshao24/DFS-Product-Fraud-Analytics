#!/usr/bin/env python3
"""Run reproducible SQL reports and export results as CSV + markdown summary."""
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'data' / 'dfs_analytics.sqlite'
SQL = ROOT / 'sql'
REPORTS = ROOT / 'reports'
FILES = ['01_conversion_funnel.sql', '02_retention_cohorts.sql', '03_fraud_flags.sql',
         '04_flag_evaluation.sql', '05_payment_kpis.sql', '06_onboarding_experiment.sql']

def main():
    if not DB.exists():
        raise SystemExit('Database missing. Run ./run_all.command or python3 scripts/build_database.py first.')
    REPORTS.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB)
    lines = ['# Synthetic DFS Product & Fraud Analytics Report', '',
             '**All data is simulated. None is from PrizePicks or real users.**', '']
    for filename in FILES:
        query = (SQL / filename).read_text(encoding='utf-8')
        cur = conn.execute(query)
        cols = [c[0] for c in cur.description]
        rows = cur.fetchall()
        output = REPORTS / filename.replace('.sql', '.csv')
        with output.open('w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            writer.writerows(rows)
        lines += [f'## {filename}', '', f'{len(rows):,} report rows. Export: `reports/{output.name}`.', '']
        for row in rows[:min(3, len(rows))]:
            lines.append(', '.join(f'{k}: {v}' for k, v in zip(cols, row)))
        lines += ['', '']
        print(f'{filename}: {len(rows):,} rows -> {output.name}')
    (REPORTS / 'summary.md').write_text('\n'.join(lines), encoding='utf-8')
    conn.close()
    print('Summary:', REPORTS / 'summary.md')

if __name__ == '__main__':
    main()
