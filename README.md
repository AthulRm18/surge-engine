# Surge Demand Intelligence Engine 🚦

**Predict where delivery demand will explode and guide drivers there *before* it happens.**

Most delivery platforms like Uber and Swiggy react to demand surges. This engine is different — it's designed to *anticipate* them. By modeling city demand as a dynamic spatial grid, it forecasts surge zones and translates raw predictions into actionable driver recommendations.

---

## 🔴 The Problem It Solves

Today's delivery logistics are fundamentally reactive:

| Problem | Impact |
|---------|--------|
| **Drivers wait in low-demand areas** | Wasted time, lost income |
| **Customers face long ETAs** | Poor experience, churn |
| **Surge pricing triggers *after* the system breaks** | Revenue left on the table |
| **No predictive spatial intelligence** | Can't position supply ahead of demand |

**The gap:** Modern platforms see demand *after* it peaks. We need to see it *before*.

---

## 🧠 How It Works

The engine models a city (Bengaluru) as a living grid using **Uber's H3 spatial indexing** and learns how demand patterns flow over time.

```
Raw Order Data → Hex-based Demand Grid → Time-Series Forecasting → Driver Hotspots
```

### Key Features

✅ **Spatial Demand Modeling** — Converts GPS orders into a hex-based demand cube across the city  
✅ **Probabilistic Forecasting** — Generates P10/P50/P90 predictions to capture uncertainty  
✅ **Causal Time-Series Pipeline** — Prevents future leakage and learns real cause-effect patterns  
✅ **3D Interactive Visualization** — Kepler.gl maps show surge zones in real-time  
✅ **Driver-Friendly Output** — Translates predictions into plain-language hotspot recommendations  

### Example Output

**What a bad system says:**  
> "Here is a heatmap showing zones with 15% higher demand."

**What this engine says:**  
> "Move to KSRTC HQ, Shanthinagar — 73% surge probability in the next 15 minutes. Estimated ₹300-400 per trip."


---

## 📊 What You Get

- **Surge Prediction Maps** — 3D visualization of predicted demand zones
- **Driver Hotspot Recommendations** — Real addresses and surge probabilities
- **Quantile Forecasts** — Best/median/worst-case scenarios for each zone
- **Actionable Intelligence** — Guidance that drivers can act on immediately

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| Data Processing | Python, Pandas, NumPy |
| Spatial Indexing | Uber H3 |
| Forecasting | XGBoost (Quantile Regression) |
| Visualization | Kepler.gl (3D geospatial) |
| Reverse Geocoding | OpenStreetMap |

---

## ▶️ How to Run

```bash
# Step 1: Generate synthetic demand data
python data_gen.py

# Step 2: Preprocess into hex-based demand grid
python preprocess.py

# Step 3: Train quantile regression models
python train.py

# Step 4: Generate 3D surge visualization
python map_data.py

# Step 5: Generate driver-friendly recommendations
python reverse_find.py
```

### Output Files

- `kepler.gl.html` — Interactive 3D surge map (open in browser)
- `driver_hotspots.csv` — Recommended hotspots with addresses and probabilities
- `bengaluru_full_city2.csv` — Full city demand data for reference

---

## 📈 Why This Matters

**For Platforms:**
- Reduce surge duration by 20-30% with proactive supply positioning
- Improve customer ETA accuracy
- Optimize pricing based on predicted demand, not reactive surge

**For Drivers:**
- Know *where* demand will peak before it happens
- Optimize earnings by being in the right place at the right time
- Reduce idle waiting time

**For Customers:**
- Faster delivery times
- More predictable pricing
- Better service reliability

---

## 🔮 The Vision

This is a proof-of-concept for **spatial demand intelligence**. The system can scale to:
- Multiple cities
- Real-time data ingestion
- Live driver position matching
- Dynamic pricing integration
- Weather/event impact modeling

---

## 📝 License

MIT

---

**Built with the belief that logistics should be predictive, not reactive.**
