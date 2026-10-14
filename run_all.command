#!/bin/bash
set -e
cd "$(dirname "$0")"
echo '=== Step 1: generate synthetic data ==='
python3 scripts/generate_data.py
echo '=== Step 2: build local SQLite database ==='
python3 scripts/build_database.py
echo '=== Step 3: execute six SQL analyses ==='
python3 scripts/run_analysis.py
echo '=== Step 4: smoke-test ==='
python3 scripts/smoke_test.py
echo 'DONE. Open reports/summary.md and the SQL files in sql/.'
