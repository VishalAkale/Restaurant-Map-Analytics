# visualizations/city_stats.py

import pandas as pd
import unicodedata
from ftfy import fix_text as ftfy_fix

# ---------------------------
# AUTO FIX BROKEN TEXT
# ---------------------------
def fix_text(s):
    if not isinstance(s, str):
        return s
    return ftfy_fix(s)

# ---------------------------
# MANUAL NAME CORRECTIONS
# ---------------------------
CITY_CORRECTIONS = {
    "S��o Paulo": "São Paulo",
    "SÃO Paulo": "São Paulo",
    "S��O PAULO": "São Paulo",
    "S_O Paulo": "São Paulo",
    "S?o Paulo": "São Paulo",
    "S_o Paulo": "São Paulo",
    "São paulo": "São Paulo",
    "Bras�_Lia": "Brasília",
    "Bras�lia": "Brasília",
    "Bras�_lia": "Brasília",
    "Brasilia": "Brasília",
    "��Stanbul": "İstanbul",
    "�stanbul": "İstanbul",
    "Istanbul": "İstanbul",
    "ISTANBUL": "İstanbul",
}

# ---------------------------
# COLUMN FINDER
# ---------------------------
def _find_col(df, cand):
    for c in cand:
        if c in df.columns:
            return c
    return None

# ---------------------------
# INDIA REGION (LAT/LON)
# ---------------------------
INDIA_LAT_MIN, INDIA_LAT_MAX = 6, 38
INDIA_LON_MIN, INDIA_LON_MAX = 68, 98

# ---------------------------
# COUNT UNIQUE CUISINES
# ---------------------------
def count_unique_cuisines(series):
    s = set()
    for v in series.dropna():
        for c in str(v).split(","):
            c = c.strip()
            if c:
                s.add(c)
    return len(s)

# ---------------------------
# MAIN FUNCTION
# ---------------------------
def compute_city_groups(df):
    df = df.copy()

    # Detect columns
    city = _find_col(df, ["City", "city"])
    rest = _find_col(df, ["Restaurant Name", "Restaurant_Name", "Name"])
    cuisines = _find_col(df, ["Cuisines", "Cuisine"])
    rating = _find_col(df, ["Aggregate rating", "Rating"])
    country = _find_col(df, ["Country Code"])
    lat = _find_col(df, ["Latitude"])
    lon = _find_col(df, ["Longitude"])

    # ---------------------------
    # FIX TEXT ENCODING ERRORS
    # ---------------------------
    if city:
        df[city] = df[city].apply(fix_text)
        df[city] = df[city].replace(CITY_CORRECTIONS)

    if cuisines:
        df[cuisines] = df[cuisines].apply(fix_text)

    # Fix numeric
    df[rating] = pd.to_numeric(df[rating], errors="coerce")

    # Remove duplicates
    df = df.drop_duplicates(subset=[rest, city], keep="first")

    # ---------------------------
    # SPLIT INDIA VS GLOBAL
    # ---------------------------
    india_df = df[
        ((df[country] == 1) if country in df.columns else False)
        |
        ((df[lat].between(INDIA_LAT_MIN, INDIA_LAT_MAX))
         & (df[lon].between(INDIA_LON_MIN, INDIA_LON_MAX)))
    ]

    global_df = df[~df.index.isin(india_df.index)]

    # ---------------------------
    # PROCESS FUNCTION
    # ---------------------------
    def process(group_df):
        if group_df.empty:
            return pd.DataFrame(columns=["City", "Num_Restaurants", "Avg_Rating", "Cuisine_Variety"])

        # Keep only cities with 5+ restaurants
        counts = group_df.groupby(city)[rest].count()
        valid = counts[counts >= 5].index
        group_df = group_df[group_df[city].isin(valid)]

        # Cap big cities
        capped = []
        for c in group_df[city].unique():
            part = group_df[group_df[city] == c]
            if len(part) > 300:
                part = part.sample(300, random_state=42)
            capped.append(part)

        group_df = pd.concat(capped, ignore_index=True)

        # Top 20 cities
        top_20 = (
            group_df.groupby(city)[rest]
            .count()
            .sort_values(ascending=False)
            .head(20)
            .index
        )

        group_df = group_df[group_df[city].isin(top_20)]

        # Build final dataframe
        result = pd.DataFrame({
            "City": top_20,
            "Num_Restaurants": group_df.groupby(city)[rest].count(),
            "Avg_Rating": group_df.groupby(city)[rating].mean(),
            "Cuisine_Variety": group_df.groupby(city)[cuisines].apply(count_unique_cuisines)
        }).reset_index(drop=True)

        return result.sort_values("Num_Restaurants", ascending=False)

    # Return: (INDIA_DATA, GLOBAL_DATA)
    return process(india_df), process(global_df)
