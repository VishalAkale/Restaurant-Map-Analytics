import pandas as pd
from visualizations.city_stats import compute_city_groups

print("Loading dataset...")
df = pd.read_csv("Dataset.csv", encoding="latin1")

print("Computing statistics (India + Global)...")
india_stats, global_stats = compute_city_groups(df)

print("\n===== INDIA STATS =====\n")
print(india_stats)

print("\n===== GLOBAL STATS =====\n")
print(global_stats)
