# visualizations/chart_generator.py
from .city_stats import compute_city_groups

def generate_all_charts(df):
    india_stats, global_stats = compute_city_groups(df)

    charts = {}

    def make_vertical_chart(name, stats, column, color, title):
        s = stats.sort_values(column, ascending=False).head(20)

        charts[name] = {
            "data": [{
                "type": "bar",
                "x": list(s["City"]),
                "y": list(s[column]),
                "marker": {"color": color},
                "hovertemplate": "<b>%{x}</b><br>" + title + ": %{y}<extra></extra>"
            }],
            "layout": {
                "template": "plotly_white",
                "height": 550,
                "margin": {"l": 40, "r": 20, "t": 80, "b": 150},
                "xaxis": {"tickangle": -45, "automargin": True},
                "yaxis": {"automargin": True},
                "title": {"text": title, "x": 0.5},
                "bargap": 0.25
            }
        }

    # INDIA
    make_vertical_chart("india_restaurants", india_stats, "Num_Restaurants",
                        "rgba(44,123,229,0.95)", "India: Number of Restaurants")

    make_vertical_chart("india_ratings", india_stats, "Avg_Rating",
                        "rgba(27,158,119,0.95)", "India: Average Rating")

    make_vertical_chart("india_cuisines", india_stats, "Cuisine_Variety",
                        "rgba(255,127,14,0.95)", "India: Cuisine Variety")

    # GLOBAL
    make_vertical_chart("global_restaurants", global_stats, "Num_Restaurants",
                        "rgba(88,80,180,0.95)", "Global: Number of Restaurants")

    make_vertical_chart("global_ratings", global_stats, "Avg_Rating",
                        "rgba(0,180,120,0.95)", "Global: Average Rating")

    make_vertical_chart("global_cuisines", global_stats, "Cuisine_Variety",
                        "rgba(255,80,60,0.95)", "Global: Cuisine Variety")

    return charts
