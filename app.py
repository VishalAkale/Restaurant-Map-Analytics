# app.py
from flask import Flask, render_template, request, jsonify
import pandas as pd
from math import floor
from visualizations.chart_generator import generate_all_charts

app = Flask(__name__)

# Load dataset (ensure this path is correct)
df = pd.read_csv("Dataset.csv")
# require latitude/longitude columns (tolerant to names)
lat_col = next((c for c in ["Latitude", "latitude", "LATITUDE", "Lat"] if c in df.columns), None)
lon_col = next((c for c in ["Longitude", "longitude", "LONGITUDE", "Lon"] if c in df.columns), None)
if lat_col is None or lon_col is None:
    raise ValueError("Dataset must contain 'Latitude' and 'Longitude' columns.")

# Normalize column names to standard names used by our code
df = df.rename(columns={lat_col: "Latitude", lon_col: "Longitude"})

# drop rows missing lat/lon
df = df.dropna(subset=["Latitude", "Longitude"])

# generate charts payloads
charts = generate_all_charts(df)

def _find_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

def rating_color(value):
    try:
        r = float(value)
    except:
        return "gray"
    if r >= 4.5:
        return "green"
    elif r >= 3.5:
        return "orange"
    return "red"

@app.route("/")
def home():
    # detect city & cuisine columns
    city_col = _find_col(df, ["City", "city", "CITY"])
    cuisine_col = _find_col(df, ["Cuisines", "Cuisine", "cuisines", "cuisine"])
    rest_col = _find_col(df, ["Restaurant Name", "Restaurant_Name", "Name", "restaurant_name"])

    if city_col is None:
        cities = []
    else:
        cities = sorted(df[city_col].dropna().unique())

    if cuisine_col is None:
        cuisines = []
    else:
        # cuisines column may contain comma-separated lists — extract unique tokens
        allc = df[cuisine_col].dropna().astype(str).str.split(",")
        cuisines_set = set()
        for row in allc:
            for token in row:
                tok = token.strip()
                if tok:
                    cuisines_set.add(tok)
        cuisines = sorted(cuisines_set)

    return render_template(
        "index.html",
        cities=cities,
        cuisines=cuisines,
        charts=charts
    )

@app.route("/map_data")
def map_data():
    bbox = request.args.get("bbox", None)
    zoom = int(request.args.get("zoom", 5))
    city = request.args.get("city", "All")
    cuisine = request.args.get("cuisine", "All")

    filtered = df.copy()

    # detect city & cuisine columns again
    city_col = _find_col(df, ["City", "city", "CITY"])
    cuisine_col = _find_col(df, ["Cuisines", "Cuisine", "cuisines", "cuisine"])
    rest_col = _find_col(df, ["Restaurant Name", "Restaurant_Name", "Name", "restaurant_name"])
    rating_col = _find_col(df, ["Aggregate rating", "Aggregate_rating", "Rating", "rating"])

    if city != "All" and city_col:
        filtered = filtered[filtered[city_col] == city]

    if cuisine != "All" and cuisine_col:
        filtered = filtered[
            filtered[cuisine_col].fillna("").str.contains(cuisine, case=False, regex=False)
        ]

    if bbox:
        try:
            minLat, minLon, maxLat, maxLon = map(float, bbox.split(","))
            filtered = filtered[
                (filtered["Latitude"] >= minLat)
                & (filtered["Latitude"] <= maxLat)
                & (filtered["Longitude"] >= minLon)
                & (filtered["Longitude"] <= maxLon)
            ]
        except:
            pass

    # show individual markers at high zoom
    if zoom >= 14 or len(filtered) <= 300:
        payload = []
        for _, r in filtered.iterrows():
            payload.append({
                "is_cluster": False,
                "name": r.get(rest_col, r.get("Restaurant Name", "Restaurant")),
                "lat": float(r["Latitude"]),
                "lon": float(r["Longitude"]),
                "rating": float(r[rating_col]) if rating_col in r and pd.notna(r[rating_col]) else 0.0,
                "cuisine": r.get(cuisine_col, ""),
                "city": r.get(city_col, ""),
                "color": rating_color(r[rating_col]) if rating_col in r else "gray"
            })
        return jsonify(payload)

    # else perform simple grid clustering
    if zoom <= 4:
        cell_deg = 4
    elif zoom <= 6:
        cell_deg = 2
    elif zoom <= 8:
        cell_deg = 1
    else:
        cell_deg = 0.4

    buckets = {}
    for _, r in filtered.iterrows():
        lat = float(r["Latitude"])
        lon = float(r["Longitude"])
        key = (floor(lat / cell_deg), floor(lon / cell_deg))
        if key not in buckets:
            buckets[key] = {"count": 0, "sumLat": 0.0, "sumLon": 0.0, "examples": []}
        b = buckets[key]
        b["count"] += 1
        b["sumLat"] += lat
        b["sumLon"] += lon
        if len(b["examples"]) < 4:
            b["examples"].append(r.get(rest_col, r.get("Restaurant Name", "Restaurant")))

    payload = []
    for b in buckets.values():
        payload.append({
            "is_cluster": True,
            "lat": b["sumLat"] / b["count"],
            "lon": b["sumLon"] / b["count"],
            "count": b["count"],
            "examples": b["examples"]
        })

    return jsonify(payload)

if __name__ == "__main__":
    # show both local and LAN links
    app.run(host="0.0.0.0", port=5000, debug=False)
