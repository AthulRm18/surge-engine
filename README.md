Surge Demand Intelligence Engine 🚦

Ever wondered how apps like Uber or Swiggy seem to know where demand is about to explode?

This project is my attempt at building that brain.

It predicts where delivery demand will surge before it happens and converts that intelligence into clear movement guidance for drivers — not just charts.

🔴 The real problem

Most platforms react to demand.

• Drivers wait in empty streets
• Customers face long ETAs
• Surge pricing kicks in only after the system breaks

What’s missing is proactive spatial intelligence.

🧠 What this system does

This engine models Bengaluru as a living grid using Uber’s H3 hexagons and learns how demand moves across the city over time.

It:

Simulates chaotic city demand (events, weekends, weather-style spikes)

Converts raw GPS orders into a hex-based demand cube

Builds a causal time-series forecasting pipeline (no future leakage)

Trains probabilistic models (P10 / P50 / P90) to capture uncertainty

Visualizes surge zones in 3D Kepler.gl maps

Translates predictions into driver-friendly hotspot instructions using reverse geocoding

📊 What comes out

Instead of saying:

“Here is a heatmap.”

The system tells a driver:

Move to KSRTC HQ, Shanthinagar — high surge probability in the next 15 minutes.

That is not prediction.
That is income optimization.

🛠 Tech stack

Python, Pandas, NumPy

Uber H3 Spatial Indexing

XGBoost (Quantile Regression)

Kepler.gl (3D geospatial visualization)

OpenStreetMap Reverse Geocoding

▶️ Run the pipeline
python data_generator.py
python preprocess.py
python train.py
python generate_surge_map.py
python driver_recommendation.py
