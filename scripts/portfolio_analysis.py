#!/usr/bin/env python3
"""Reproduce synthetic fraud policy comparison and onboarding z-tests.

Requires only standard-library Python. Nothing here evaluates real fraud or
establishes real-world product lift; scenarios and experiment are simulated.
"""
import csv
import math
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'data' / 'dfs_analytics.sqlite'
REPORTS = ROOT / 'reports'


def experiment_test(a, b, success_col, label):
    n1, n2 = int(a['signups']), int(b['signups'])
    x1, x2 = int(a[success_col]), int(b[success_col])
    p1, p2 = x1/n1, x2/n2
    p = (x1+x2)/(n1+n2)
    pooled_se = math.sqrt(p*(1-p)*(1/n1 + 1/n2))
    z = (p2-p1) / pooled_se
    p_value = math.erfc(abs(z)/math.sqrt(2))
    unpooled_se = math.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
    low, high = (p2-p1-1.96*unpooled_se), (p2-p1+1.96*unpooled_se)
    return {
        'metric': label, 'a': f'{p1:.2%}', 'b': f'{p2:.2%}',
        'lift': f'{100*(p2-p1):+.2f} pp', 'z': f'{z:.3f}',
        'p': f'{p_value:.6f}',
        'ci': f'[{100*low:+.2f}, {100*high:+.2f}] pp',
        'significant': 'Yes' if p_value < 0.05 else 'No',
    }


def main():
    REPORTS.mkdir(exist_ok=True)
    if not DB.exists():
        raise SystemExit('Database missing; run bash run_all.command first.')
    with sqlite3.connect(DB) as conn:
        q = (ROOT/'sql'/'07_fraud_policy_comparison.sql').read_text()
        cur = conn.execute(q)
        cols = [c[0] for c in cur.description]
        policies = [dict(zip(cols, row)) for row in cur.fetchall()]
    if len(policies) != 4:
        raise SystemExit(f'Expected four policies, got {len(policies)}')
    with (REPORTS/'06_onboarding_experiment.csv').open(newline='') as f:
        variants = {r['experiment_variant']: r for r in csv.DictReader(f)}
    if set(variants) != {'A','B'}:
        raise SystemExit('Expected A/B experiment variants in report.')
    experiments = [experiment_test(variants['A'], variants['B'], col, label) for col, label in [
        ('deposited_7d','7-day deposit conversion'),
        ('entered_lineup_7d','7-day first-lineup conversion')
    ]]
    lines = [
        '# Synthetic DFS Portfolio — Statistical Validation', '',
        '> **Synthetic data only.** The labels are planted, and this is not evidence of real fraud or customer lift.', '',
        '## Fraud-review policy tradeoffs', '',
        '| Policy | TP | FP | FN | TN | Flagged | Precision | Recall | FPR |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|'
    ]
    for r in policies:
        lines.append(f"| {r['policy']} | {r['tp']} | {r['fp']} | {r['fn']} | {r['tn']} | {r['total_flagged']} | {r['precision_pct']:.2f}% | {r['recall_pct']:.2f}% | {r['false_positive_rate_pct']:.2f}% |")
    lines += [
        '', '## Simulated onboarding experiment', '',
        '| Metric | Control A | Treatment B | Difference | z | p-value | 95% CI of difference | Significant (5%) |',
        '|---|---:|---:|---:|---:|---:|---:|---|'
    ]
    for r in experiments:
        lines.append(f"| {r['metric']} | {r['a']} | {r['b']} | {r['lift']} | {r['z']} | {r['p']} | {r['ci']} | {r['significant']} |")
    lines += [
        '', 'Two-sided pooled two-proportion z-test; approximate unpooled Wald confidence interval.',
        'Interpret with care: synthetic population, independent-observation assumption, and no real-world causal inference.', ''
    ]
    out = REPORTS/'portfolio_validation.md'
    out.write_text('\n'.join(lines), encoding='utf-8')
    print('\n'.join(lines))
    print(f'\nSaved report: {out}')

if __name__ == '__main__':
    main()
