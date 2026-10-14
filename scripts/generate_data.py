#!/usr/bin/env python3
"""Deterministic SYNTHETIC daily-fantasy-sports data generator; no real user data."""
from __future__ import annotations
import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RNG = random.Random(20261014)
N_USERS = 5000
START = datetime(2026, 8, 1, tzinfo=timezone.utc)
END = datetime(2026, 10, 1, tzinfo=timezone.utc)
CHANNELS = ['organic', 'referral', 'social', 'paid_search']


def stamp(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def write_rows(name, fields, rows):
    path = DATA / name
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        writer.writerows(rows)
    print(f'{path.name}: {len(rows):,} rows')


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    users, events, payments, lineups, promos = [], [], [], [], []
    event_id = payment_id = lineup_id = promo_id = 0
    promo_seen = 0
    normal_household = 0

    for user_id in range(1, N_USERS + 1):
        day = RNG.randrange(60)
        signup = START + timedelta(days=day, hours=RNG.randrange(7, 23), minutes=RNG.randrange(60))
        variant = RNG.choice(['A', 'B'])
        channel = RNG.choice(CHANNELS)
        lottery = RNG.random()
        scenario = ('promo_pattern' if lottery < .045 else
                    'payment_pattern' if lottery < .075 else 'ordinary')
        # Intentional planted patterns FOR SYNTHETIC EVALUATION ONLY.
        # Not real fraud labels; shared devices and retries are not proof of fraud.
        if scenario == 'promo_pattern':
            device_id = f'sim_shared_promo_{promo_seen // 5:03d}'
            promo_seen += 1
        elif scenario == 'ordinary' and RNG.random() < .025:
            device_id = f'sim_household_{normal_household // 3:03d}'
            normal_household += 1
        else:
            device_id = f'device_{user_id:06d}'

        users.append((user_id, stamp(signup), variant, channel, device_id, scenario))

        def add_event(kind, when, session_id=None):
            nonlocal event_id
            if when >= END or when < signup:
                return
            event_id += 1
            events.append((event_id, user_id, session_id or '', kind, stamp(when)))

        add_event('signup', signup)
        max_session_offset = min(45, max(0, (END - signup).days - 1))
        offsets = {0}
        if max_session_offset >= 1 and RNG.random() < (.36 if variant == 'B' else .29):
            offsets.add(1)
        if max_session_offset >= 7 and RNG.random() < (.21 if variant == 'B' else .17):
            offsets.add(7)
        for _ in range(RNG.randrange(3, 12)):
            offsets.add(RNG.randrange(max_session_offset + 1))
        for j, off in enumerate(sorted(offsets), 1):
            when = signup + timedelta(days=off, minutes=RNG.randrange(1, 100))
            sid = f's_{user_id}_{j}'
            add_event('session_start', when, sid)
            for _ in range(RNG.randrange(1, 4)):
                add_event(RNG.choice(['view_home', 'view_projection', 'view_promo', 'build_lineup']),
                          when + timedelta(seconds=RNG.randrange(8, 360)), sid)

        def add_payment(status, when):
            nonlocal payment_id
            if when >= END:
                return None
            payment_id += 1
            amount = RNG.choice([10, 15, 20, 25, 30, 50, 75])
            payments.append((payment_id, user_id, stamp(when), amount, status))
            add_event('payment_success' if status == 'success' else 'payment_failed', when)
            return when

        success_prob = (.61 if variant == 'B' else .54)
        if scenario == 'promo_pattern':
            success_prob = .77
        if scenario == 'payment_pattern':
            success_prob = .43
        successful_deposit = RNG.random() < success_prob
        failure_count = (RNG.randint(3, 7) if scenario == 'payment_pattern' else
                         RNG.choice([0] * 87 + [1] * 11 + [3] * 2))
        start_payment = signup + timedelta(hours=RNG.randrange(1, 48))
        for k in range(failure_count):
            add_payment('failed', start_payment + timedelta(minutes=k * RNG.randrange(2, 16)))
        deposit_when = None
        if successful_deposit:
            deposit_when = add_payment('success', start_payment + timedelta(hours=RNG.randrange(2, 18)))

        if deposit_when and RNG.random() < .63:
            for k in range(RNG.randrange(1, 5)):
                when = deposit_when + timedelta(hours=2 + k * RNG.randrange(5, 18))
                if when >= END:
                    continue
                lineup_id += 1
                lineups.append((lineup_id, user_id, stamp(when), RNG.choice([5, 10, 20, 25, 50]), RNG.randrange(2, 7)))
                add_event('lineup_submitted', when)

        promo_count = (RNG.randint(3, 8) if scenario == 'promo_pattern' else
                       RNG.choice([0] * 55 + [1] * 42 + [3] * 3))
        for k in range(promo_count):
            when = signup + timedelta(days=1, hours=RNG.randrange(2, 15), minutes=3 * k)
            if when >= END:
                continue
            promo_id += 1
            promos.append((promo_id, user_id, stamp(when), f'PROMO_{(k % 3) + 1}', RNG.choice([2, 5, 10])))
            add_event('promo_redeemed', when)

    write_rows('users.csv', ['user_id', 'signup_ts', 'experiment_variant', 'acquisition_channel', 'device_id', 'synthetic_scenario'], users)
    write_rows('events.csv', ['event_id', 'user_id', 'session_id', 'event_type', 'event_ts'], events)
    write_rows('payments.csv', ['payment_id', 'user_id', 'payment_ts', 'amount_usd', 'status'], payments)
    write_rows('lineups.csv', ['lineup_id', 'user_id', 'lineup_ts', 'entry_fee_usd', 'pick_count'], lineups)
    write_rows('promos.csv', ['promo_id', 'user_id', 'redeemed_ts', 'promo_code', 'credit_usd'], promos)
    print('SYNTHETIC TEST DATA ONLY: no real accounts, bets, or platform records.\n')


if __name__ == '__main__':
    main()
