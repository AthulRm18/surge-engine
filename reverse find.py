import pandas as pd
import h3
import requests
import time

print("Loading surge map...")
df = pd.read_csv("kepler_surge_map.csv")


df['driver_score'] = df['p50_demand'] / (df['active_hours'] + 1)

top = df.sort_values('driver_score', ascending=False).head(5)

def get_center(h):
    lat, lng = h3.cell_to_latlng(h)
    return pd.Series({'lat': lat, 'lng': lng})

top[['lat','lng']] = top['h3_index'].apply(get_center)


def reverse_geocode(lat, lng):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "format": "json",
        "lat": lat,
        "lon": lng,
        "zoom": 16
    }
    headers = {"User-Agent": "athul-surge-engine"}

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        data = r.json()
        return data.get("display_name","Unknown location")
    except:
        return "Location lookup failed"

print("Converting to place names...")

place_names = []
for _, row in top.iterrows():
    place = reverse_geocode(row['lat'], row['lng'])
    place_names.append(place)
    time.sleep(1)   # avoid OSM rate-limit

top['location_name'] = place_names

top.to_csv("driver_hotspots.csv", index=False)

print("\nDRIVER RECOMMENDATIONS:\n")

for i, row in top.iterrows():
    print(f" Move to: {row['location_name']}")
    print(f"   Expected Demand Score: {row['driver_score']:.2f}\n")

print("driver_hotspots.csv generated")
