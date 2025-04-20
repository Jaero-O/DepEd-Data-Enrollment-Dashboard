import pandas as pd
import json
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc
from pathlib import Path

def card_choropleth(df=None, location=None, mode='school'):
    if df is None or df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

    # Standardize region names to match GeoJSON
    region_map = {
        "Region I": "Region I (Ilocos Region)",
        "Region II": "Region II (Cagayan Valley)",
        "Region III": "Region III (Central Luzon)",
        "Region IV-A": "Region IV-A (CALABARZON)",
        "Region IV-B": "Region IV-B (MIMAROPA)",
        "Region V": "Region V (Bicol Region)",
        "Region VI": "Region VI (Western Visayas)",
        "Region VII": "Region VII (Central Visayas)",
        "Region VIII": "Region VIII (Eastern Visayas)",
        "Region IX": "Region IX (Zamboanga Peninsula)",
        "Region X": "Region X (Northern Mindanao)",
        "Region XI": "Region XI (Davao Region)",
        "Region XII": "Region XII (SOCCSKSARGEN)",
        "NCR": "National Capital Region (NCR)",
        "CAR": "Cordillera Administrative Region (CAR)",
        "BARMM": "Bangsamoro Autonomous Region in Muslim Mindanao (BARMM)",
        "PSO": None  # Optional: exclude foreign/undefined entries
    }

    df['region'] = df['region'].map(region_map)
    df = df.dropna(subset=['region'])  # Drop unmatched regions like 'PSO'

    # Group data
    if mode == 'student' and 'enrollment' in df.columns:
        region_counts = df.groupby('region')['enrollment'].sum().reset_index(name='Total')
    else:
        region_counts = df.groupby('region').size().reset_index(name='Total')

    # Load GeoJSON
    geojson_path = Path("main/data_engineer/frontend/assets/geojson/country/lowres/country.0.001.json")
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    # Plot
    fig = px.choropleth(
        region_counts,
        geojson=geojson_data,
        featureidkey="properties.adm1_en",  # Match region names to GeoJSON
        locations="region",
        color="Total",
        color_continuous_scale="Blues",
        title="Total Number of Schools per Region (SY 2023-2024)" if mode == 'school' else "Total Enrollment per Region (SY 2023-2024)"
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
    fig.update_traces(hovertemplate="<b>%{location}</b><br>Total: %{z}<extra></extra>")

    return dbc.Card([
        dbc.CardHeader("Enrollment Choropleth Map"),
        dbc.CardBody([dcc.Graph(figure=fig)])
    ], className="mt-4 shadow", style={"height": "100%", "overflow": "hidden", 'width': '1000px'})
