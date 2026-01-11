import pandas as pd
import numpy as np
import pickle
import h3

print("Loading probabilistic models...")
with open("model_expert.pkl","rb") as f:
    models = pickle.load(f)

p10 = models['p10']
p50 = models['p50']
p90 = models['p90']

print("📊 Loading training data...")
df = pd.read_csv("training_data4.csv")

# Spatial baseline per hexagon
hex_stats = df.groupby('h3_index').agg(
    mean_capacity=('mean_capacity','first'),
    peak_capacity=('peak_capacity','first'),
    active_hours=('active_hours','first')
).reset_index()

scenario = hex_stats.copy()


# Simulate Friday 8 PM peak
scenario['hour_sin'] = np.sin(2*np.pi*20/24)
scenario['hour_cos'] = np.cos(2*np.pi*20/24)
scenario['day_of_week'] = 4
scenario['is_weekend'] = 0

scenario['lag_1h'] = scenario['mean_capacity'] * np.random.uniform(0.6, 1.1, len(scenario))
scenario['lag_24h'] = scenario['mean_capacity'] * np.random.uniform(0.6, 1.1, len(scenario))
scenario['rolling_mean_3h'] = scenario['mean_capacity'] * np.random.uniform(0.7, 1.0, len(scenario))
scenario['rolling_std_6h'] = scenario['mean_capacity'] * 0.3


FEATURES = ['hour_sin','hour_cos','day_of_week','is_weekend',
            'lag_1h','lag_24h','rolling_mean_3h','rolling_std_6h',
            'mean_capacity','peak_capacity','active_hours']


print("🔮 Predicting surge bands...")
scenario['p10_demand'] = p10.predict(scenario[FEATURES])
scenario['p50_demand'] = p50.predict(scenario[FEATURES])
scenario['p90_demand'] = p90.predict(scenario[FEATURES])

scenario[['p10_demand','p50_demand','p90_demand']] = scenario[['p10_demand','p50_demand','p90_demand']].clip(lower=0)

scenario['lat'] = scenario['h3_index'].apply(lambda x: h3.cell_to_latlng(x)[0])
scenario['lng'] = scenario['h3_index'].apply(lambda x: h3.cell_to_latlng(x)[1])

scenario.to_csv("kepler_surge_map.csv", index=False)
print(" kepler_surge_map.csv ready")
