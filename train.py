import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_error
import pickle

def train_model():
    print("Loading data ...")
    df = pd.read_csv("training_data4.csv", parse_dates=['time_bucket'])

    FEATURES = [
    'hour_sin','hour_cos','day_of_week','is_weekend',
    'lag_1h','lag_24h','rolling_mean_3h','rolling_std_6h',
    'mean_capacity','peak_capacity','active_hours'
    ]

    TARGET = 'order_count'

    print(" Performing hex-wise temporal split...")

    train_list, test_list = [], []

    for h in df['h3_index'].unique():
        sub = df[df['h3_index'] == h].sort_values('time_bucket')
        cut = int(len(sub) * 0.9)
        train_list.append(sub.iloc[:cut])
        test_list.append(sub.iloc[cut:])

    train_df = pd.concat(train_list)
    test_df  = pd.concat(test_list)

    X_train = train_df[FEATURES]
    y_train = train_df[TARGET]
    X_test  = test_df[FEATURES]
    y_test  = test_df[TARGET]

    models = {}
    quantiles = [0.1, 0.5, 0.9]

    for q in quantiles:
        print(f" Training P{int(q*100)} Model...")

        model = xgb.XGBRegressor(
            objective='reg:quantileerror',
            quantile_alpha=q,
            n_estimators=300,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            learning_rate=0.05,
            n_jobs=-1
        )

        model.fit(X_train, y_train)
        models[f'p{int(q*100)}'] = model

    print("Evaluating P50 model...")
    p50_preds = models['p50'].predict(X_test)
    mae = mean_absolute_error(y_test, p50_preds)
    print(f"Median MAE: {mae:.2f}")

    print("📏 Evaluating uncertainty coverage...")
    p10_preds = models['p10'].predict(X_test)
    p90_preds = models['p90'].predict(X_test)

    coverage = np.mean((y_test >= p10_preds) & (y_test <= p90_preds)) * 100
    print(f"P10–P90 Coverage: {coverage:.1f}%")

    with open("model_expert.pkl", "wb") as f:
        pickle.dump(models, f)

    print(" model_ok.pkl saved")

if __name__ == "__main__":
    train_model()
