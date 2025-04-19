import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re

def preserve_parentheses_title(text):
    return re.sub(r'\((.*?)\)', lambda m: f"({m.group(1)})", text.title())

def card_five(df, mode='student'):
    if df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

    if mode == 'school':
        df = df.groupby(['school_type']).size().reset_index(name='total')
        card_five_title = 'No. of Schools'

    elif mode == 'student':
        grade_cols = [col for col in df.columns if '_male' in col or '_female' in col]
        df = df[['school_type'] + grade_cols].copy()
        df['total'] = df[grade_cols].sum(axis=1)
        card_five_title = 'Enrollment'

    # Group and sort
    grouped = df.groupby('school_type')[['total']].sum().sort_values(by='total', ascending=False)
    categories = [{"name": idx, "value": row["total"]} for idx, row in grouped.iterrows()]

    # Add some breathing room on the right for the labels
    x_max = grouped['total'].max() * 1.45

    # Create subplots
    subplots = make_subplots(
        rows=len(categories),
        cols=1,
        subplot_titles=[preserve_parentheses_title(x["name"]) for x in categories],
        shared_xaxes=True,
        vertical_spacing=(0.01 / len(categories)),
    )

    for k, x in enumerate(categories):
        subplots.add_trace(go.Bar(
            orientation='h',
            y=[x["name"]],
            x=[x["value"]],
            text=[f"{x['value']:,}"],
            textfont=dict(family="Inter", size=14, color="#081434", weight="bold"),
            textposition='outside',
            marker=dict(color="#7986cb"),
            hoverinfo='text',
        ), row=k + 1, col=1)

    # Update layout
    for ann in subplots["layout"]["annotations"]:
        ann["x"] = 0
        ann["xanchor"] = "left"
        ann["align"] = "left"
        ann["font"] = dict(size=12, family="Inter", weight="bold", color='#2a4d69')
        if len(categories) > 1:
            ann["yshift"] = -60 * (1/(len(categories)))
        else:
            ann["yshift"] = -45

    if len(categories) > 1:
            width_gap = max(0.65, min(0.9, 1.5 / (len(categories))))
    else:
        width_gap = 0.82
    
    layout_updates = {
        "showlegend": False,
        "height": min(240, 60 + 40 * len(categories)),        
        "margin": dict(t=10, b=0, l=0, r=10),
        "template": "simple_white",
        "paper_bgcolor": 'rgba(0,0,0,0)',
        "plot_bgcolor": 'rgba(0,0,0,0)',
        "xaxis": {
            "range": [0, x_max],
            "showgrid": False,
            "zeroline": False,
            "visible": False,
        },
        "yaxis": {
            "showgrid": False,
            "zeroline": False,
            "visible": False,
        },
        "bargroupgap": width_gap,
        "font": dict(family="Inter", size=12, color="black"),
    }

    for i in range(1, len(categories) + 1):
        layout_updates[f'xaxis{i}'] = dict(visible=False, range=[0, x_max])
        layout_updates[f'yaxis{i}'] = dict(visible=False)

    subplots.update_layout(**layout_updates)

    return html.Div([
            html.Div([
                html.Div(
                f"Enrollment by School Type".upper(),
                className='card-title-main'),
            ],className='card-header-wrapper'),
            html.Div([
                dcc.Graph(figure=subplots, config={'displayModeBar': False}),
            ], 
            className='card-five-graph'),
        ], className='card card-five')

