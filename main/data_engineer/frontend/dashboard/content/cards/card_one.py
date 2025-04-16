import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go
import re
import os
from datetime import datetime

# Load dataset
file_path = 'enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv'
df = pd.read_csv(file_path)

# Identify gender-related columns dynamically
male_columns = [col for col in df.columns if '_male' in col]
female_columns = [col for col in df.columns if '_female' in col]

def detect_school_year(df, file_path):
    """Detects the school year from the dataset"""
    for col in df.columns:
        if 'year' in col.lower() or 'sy' in col.lower():
            first_val = str(df[col].dropna().unique()[0])
            return f"A.Y.{first_val}"

    filename = os.path.basename(file_path)
    match = re.search(r'(\d{4})[_\-](\d{4})', filename)
    if match:
        return f"A.Y. {match.group(1)}–{match.group(2)}"

    today = datetime.today()
    start_year = today.year if today.month >= 6 else today.year - 1
    end_year = start_year + 1
    return f"A.Y. {start_year}–{end_year}"

def create_gender_card():
    school_year = detect_school_year(df, file_path)

    total_male = df[male_columns].sum().sum()
    total_female = df[female_columns].sum().sum()
    total_enrollment = total_male + total_female

    male_pct = round((total_male / total_enrollment) * 100, 1)
    female_pct = round((total_female / total_enrollment) * 100, 1)

    # Donut chart
    fig = go.Figure(go.Pie(
        labels=['Male', 'Female'],
        values=[total_male, total_female],
        hole=0.6,
        textinfo='none',
        marker=dict(colors=['#2a4d69', '#f28cb1']),
        sort=False
    ))

    fig.update_layout(
    annotations=[dict(
        text=f"<b>A.Y.<br>{school_year[4:]}</b>",
        x=0.5, y=0.5,
        font_size=16,
        showarrow=False,
        align='center'
    )],
    margin=dict(t=0, b=0, l=0, r=0),
    showlegend=False,
    height=220,
    width=220,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    )

    # Gender legend
    gender_legend = html.Div([
    html.Div([
        html.Span(style={
            'width': '26px', 'height': '13px',
            'backgroundColor': '#2a4d69',
            'borderRadius': '8px',
            'display': 'inline-block',
            'marginRight': '8px'
        }),
        html.Span([
            html.Span(f"{male_pct}%", style={'fontSize': '20px', 'fontWeight': 'bold', 'color': '#2a4d69'}),
            html.Span(" MALE", style={'fontSize': '14px', 'fontWeight': 'bold', 'color': '#2a4d69'})
        ])
    ], className='mb-2'),

    html.Div([
        html.Span(style={
            'width': '26px', 'height': '13px',
            'backgroundColor': '#f28cb1',
            'borderRadius': '8px',
            'display': 'inline-block',
            'marginRight': '8px'
        }),
        html.Span([
            html.Span(f"{female_pct}%", style={'fontSize': '20px', 'fontWeight': 'bold', 'color': '#f28cb1'}),
            html.Span(" FEMALE", style={'fontSize': '14px', 'fontWeight': 'bold', 'color': '#f28cb1'})
        ])
    ])
], style={'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'})

    return dbc.Card(
        dbc.CardBody([
            html.Div("TOTAL ENROLLMENT", className="text-uppercase text-muted small fw-bold mb-1"),
            html.H2(f"{int(total_enrollment):,}", className="fw-bold mb-3", style={'color': '#0a1f44'}),

            # Tight horizontal layout
            html.Div([
                html.Div(gender_legend, style={'flex': '0 0 auto', 'marginRight': '10px'}),
                html.Div(dcc.Graph(figure=fig, config={'displayModeBar': False}), style={'flex': '0 0 auto'})
            ], style={'display': 'flex', 'alignItems': 'center'})
        ]),
        className="mb-4 shadow-sm",
        # style={
        #     'backgroundColor': '#f9fbfc',
        #     'border': '4px solid #9ac3db',
        #     'borderRadius': '20px'
        # }
    )
