import pandas as pd
import h3
import numpy as np

def process_expert_data(input_file="bengaluru_full_city2.csv"):
    print(" Loading data...")
    df = pd.read_csv(input_file)
    df['timestamp']=pd.to_datetime(df['timestamp'])
    
    #  H3 Indexing (Resolution 8)
    
    df['h3_index']=df.apply(lambda row: h3.latlng_to_cell(row['lat'], row['lng'], 8), axis=1)
    
    
    df['time_bucket']=df['timestamp'].dt.floor('h')
    agg_df = df.groupby(['h3_index', 'time_bucket']).size().reset_index(name='order_count')
    
    
    agg_df = agg_df.sort_values(['h3_index','time_bucket'])
    agg_df['gap'] = agg_df.groupby('h3_index')['time_bucket'].diff().dt.total_seconds().div(3600)
    agg_df = agg_df[agg_df['gap'].fillna(1) <= 1]

    
    # A. Cyclic Time Encoding 
    agg_df['hour'] = agg_df['time_bucket'].dt.hour
    agg_df['hour_sin'] = np.sin(2 * np.pi * agg_df['hour']/24)
    agg_df['hour_cos'] = np.cos(2 * np.pi * agg_df['hour']/24)
    agg_df['day_of_week'] = agg_df['time_bucket'].dt.dayofweek
    agg_df['is_weekend'] = (agg_df['day_of_week'] >= 5).astype(int)

    # B. Rolling Window Statistics (Trends)
    
    agg_df = agg_df.sort_values(by=['h3_index', 'time_bucket'])
    
    agg_df['rolling_mean_3h'] = agg_df.groupby('h3_index')['order_count'] \
      .transform(lambda x: x.shift(1).rolling(3).mean())

    agg_df['rolling_std_6h'] = agg_df.groupby('h3_index')['order_count'] \
      .transform(lambda x: x.shift(1).rolling(6).std())


    
    agg_df['lag_1h'] = agg_df.groupby('h3_index')['order_count'].shift(1)
    agg_df['lag_24h'] = agg_df.groupby('h3_index')['order_count'].shift(24) # Same time yesterday
    

    agg_df = agg_df.dropna()

    hex_stats = agg_df.groupby('h3_index')['order_count'].agg(
    mean_capacity='mean',
    peak_capacity='max',
    active_hours=lambda x: (x > 0).sum()
    ).reset_index()

    agg_df = agg_df.merge(hex_stats, on='h3_index', how='left')

    
    
    return agg_df

if __name__ == "__main__":
    df = process_expert_data()
    df.to_csv("training_data4.csv", index=False)
    print("Saved")