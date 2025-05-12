import pandas as pd
from dash import html

def card_ten(df, mode):
    location_cols = ['region', 'division', 'district', 'province', 'municipality', 'barangay']
    blue_cols = {'region', 'division', 'district'}
    orange_cols = {'province', 'municipality', 'barangay'}
    cards = []

    for col in location_cols:
        unique_values = sorted(df[col].dropna().unique())
        color_class = "card-ten-blue" if col in blue_cols else "card-ten-orange"
        label_color_class = "card-ten-label-blue" if col in blue_cols else "card-ten-label-orange"

        formatted_count = f"{df[col].nunique():,}"

        card = html.Div([
            html.Div(formatted_count, className="card-ten-count"),
            html.Div("Total", className="card-ten-label-subtitle"),
            html.Div(
                col.replace('_', ' ').title(),
                className=f"card-ten-label {label_color_class}"
            ),
        ], className=f"card card_ten {color_class}")

        cards.append(card)

    return html.Div(cards, className="card-ten-wrapper")
