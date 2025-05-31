# 🛰️ Environmental Route Planner and Power Line AI Assistant

This project is an interactive web-based tool for computing and visualizing the shortest path using Dijkstra's algorithm on raster map data. It supports environmental planning by helping users identify cost-effective and potentially more environmentally friendly powerline routes.

---

## 📌 Features

- ✅ **Interactive map** with raster visualization (`.tif`)
- ✅ **Click-to-select** start and goal points
- ✅ **Dijkstra algorithm** with 8-directional movement
- ✅ **Path visualization** and export to `.txt`
- ✅ **Environmental analysis** support via LLM (Streamlit + Meta-LLaMA)

---

## 🖥 Technologies Used

- [Dash](https://dash.plotly.com/) (Plotly) – Interactive UI
- [NumPy](https://numpy.org/) – Matrix computations
- [Rasterio](https://rasterio.readthedocs.io/) – Raster data loading
- [Streamlit](https://streamlit.io/) – Environmental impact assistant
- [OpenAI / LLaMA API](https://featherless.ai/) – Natural language evaluation
- GeoJSON / TXT – Data input/output

---

## 📂 Project Structure

```
📁 root
├── dash_app.py             # Dash UI and Dijkstra pathfinding
├── dijkstra.py             # Dijkstra algorithm (8 directions) + save to txt
├── landuse_cutout.tif      # Raster map (not included here)
├── jihocesky_median_bezoutliers.geojson  # Area map data (geojson)
├── proposed_route.txt      # Example input route
├── villages_layers.txt     # Area environmental layers
├── main.py                 # Streamlit LLM-based analysis tool
```

---

## ▶️ How to Run

### 1. Clone the repository:

```bash
git clone https://github.com/kruzek/GreenHack.git
cd GreenHack
```

### 2. Install dependencies:

```bash
pip install -r requirements.txt
```

> (Make sure you have a Python 3.8–3.11 environment.)

### 3. Run the Dash app:

```bash
python dash_app.py
```

Go to `http://127.0.0.1:8050` in your browser.

### 4. Optional: Run the Streamlit analysis tool:

```bash
streamlit run main.py
```

---

## 🧠 How It Works

### 🗺️ Dijkstra Route Visualization

1. Load the `landuse_cutout.tif` raster.
2. Let the user select start/goal points.
3. Apply Dijkstra's algorithm with cost weighting and 8 directions.
4. Visualize the path on a heatmap.
5. Allow download of path as `.txt`.

### 🌱 Environmental LLM Assistant

- Loads `villages_layers.txt` and `proposed_route.txt`
- Takes user messages and proposed path
- Uses **Meta-LLaMA 3** to provide a structured environmental impact analysis
- Suggests **improved or shortened routes** based on impact

---


## 🤝 Credits

Created for the **GreenHack 2025** challenge by the GreenHulk team.
