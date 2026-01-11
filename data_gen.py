import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

NUM_ORDERS = 60000

HUBS = {
    "Koramangala":     (12.9352, 77.6245),
    "Indiranagar":     (12.9716, 77.6412),
    "Whitefield":      (12.9698, 77.7500),
    "Electronic City": (12.8452, 77.6602),
    "Malleshwaram":    (13.0031, 77.5643),
    "Hebbal":          (13.0354, 77.5988),
    "Jayanagar":       (12.9250, 77.5938),
    "MG Road":         (12.9756, 77.6066)
}

# Economic strength of each hub
HUB_WEIGHTS = {
    "Koramangala": 1.6,
    "Indiranagar": 1.5,
    "MG Road": 1.7,
    "Whitefield": 1.1,
    "Electronic City": 1.0,
    "Malleshwaram": 0.8,
    "Hebbal": 0.7,
    "Jayanagar": 0.9
}

def generate_chaos_data():
    print("Generating Bengaluru Uber-grade Chaos Data")

    all_lats, all_lngs = [], []

    total_weight = sum(HUB_WEIGHTS.values())
    orders_by_hub = {k: int(NUM_ORDERS*0.8*(HUB_WEIGHTS[k]/total_weight)) for k in HUBS}

    for hub, coords in HUBS.items():
        print(f"{hub}")
        spread = 0.04 if hub in ["Whitefield","Electronic City"] else 0.02
        n = orders_by_hub[hub]

        all_lats.append(np.random.normal(coords[0], spread, n))
        all_lngs.append(np.random.normal(coords[1], spread, n))

    remaining = NUM_ORDERS - sum(orders_by_hub.values())
    all_lats.append(np.random.uniform(12.84, 13.05, remaining))
    all_lngs.append(np.random.uniform(77.50, 77.75, remaining))

    final_lats = np.concatenate(all_lats)
    final_lngs = np.concatenate(all_lngs)

    base_time = datetime.now() - timedelta(days=60)
    timestamps = []

    weights = np.array([0.01]*10 + [0.1,0.2,0.1] + [0.05]*4 + [0.1,0.2,0.1] + [0.01]*4)
    weights /= weights.sum()

    for _ in range(len(final_lats)):
        day_offset = random.randint(0,60)
        current_day = base_time + timedelta(days=day_offset)
        is_weekend = current_day.weekday() >= 5
        is_surge_day = random.random() < 0.1

        daily_weights = weights.copy()

        if is_weekend:
            daily_weights[22] += 0.2
            daily_weights[23] += 0.2

        if is_surge_day:
            daily_weights[19] += 0.5
            daily_weights[20] += 0.5

        # Breakfast commute
        if not is_weekend:
            daily_weights[9] += 0.15

        # Monsoon seasonality
        if current_day.month in [6,7,8]:
            daily_weights[19] += 0.2

        # Festival burst
        if random.random() < 0.03:
            daily_weights[20] += 0.8

        daily_weights /= daily_weights.sum()

        hour = np.random.choice(range(24), p=daily_weights)
        minute = random.randint(0,59)

        timestamps.append(current_day + timedelta(hours=int(hour), minutes=minute))

    df = pd.DataFrame({
        'order_id': range(len(timestamps)),
        'lat': final_lats,
        'lng': final_lngs,
        'timestamp': timestamps
    })

    df['timestamp'] += pd.to_timedelta(np.random.normal(0,15,len(df)), unit='m')

    df.to_csv("bengaluru_full_city2.csv", index=False)
    print("✅ bengaluru_full_city2.csv generated")

if __name__ == "__main__":
    generate_chaos_data()
