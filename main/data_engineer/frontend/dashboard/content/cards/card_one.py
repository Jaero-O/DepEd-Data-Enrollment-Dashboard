import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go
import re
import os
from datetime import datetime

def detect_school_year(df, file_path=None):
    """Detects the school year from the dataset or filename"""
    for col in df.columns:
        if 'year' in col.lower() or 'sy' in col.lower():
            first_val = str(df[col].dropna().unique()[0])
            return f"<b>A.Y. <br>{first_val}</b>"

    if file_path:
        filename = os.path.basename(file_path)
        match = re.search(r'(\d{4})[_\-](\d{4})', filename)
        if match:
            return f"<b>A.Y. <br>{match.group(1)}–{match.group(2)}</b>"

    today = datetime.today()
    start_year = today.year if today.month >= 6 else today.year - 1
    end_year = start_year + 1
    return f"<b>A.Y. <br>{start_year}–{end_year}</b>"

def card_one(df, mode, location):
    """
    Gender Distribution or School Information Card

    Parameters:
    - df: DataFrame filtered based on user selections
    - mode: str, either 'student' or 'school'
    - location: str, e.g., 'Region', 'Division', etc.

    Returns:
    - dbc.Card Dash component
    """
    if mode == 'student':
        school_year = detect_school_year(df)

        # Gender columns detection
        male_columns = [col for col in df.columns if '_male' in col.lower()]
        female_columns = [col for col in df.columns if '_female' in col.lower()]

        total_male = df[male_columns].sum().sum()
        total_female = df[female_columns].sum().sum()
        total_enrollment = total_male + total_female

        male_pct = round((total_male / total_enrollment) * 100, 1) if total_enrollment > 0 else 0
        female_pct = round((total_female / total_enrollment) * 100, 1) if total_enrollment > 0 else 0

        # Donut chart
        fig = go.Figure(go.Pie(
            labels=['Male', 'Female'],
            values=[total_male, total_female],
            hole=0.6,
            textinfo='none',
            marker=dict(colors=['#2a4d69', '#f28cb1']),
            sort=False,
            direction='clockwise',
            rotation=180
        ))

        fig.update_layout(
            annotations=[dict(
                text=f"<b>{school_year}</b>",
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

                html.Div([
                    html.Div(gender_legend, style={'flex': '0 0 auto', 'marginRight': '10px'}),
                    html.Div(dcc.Graph(figure=fig, config={'displayModeBar': False}), style={'flex': '0 0 auto'})
                ], style={'display': 'flex', 'alignItems': 'center'})
            ]),
            className="mb-4 shadow-sm"
        )

    elif mode == 'school':
        # Example: School-specific card
        total_schools = df['School Name'].nunique()
        school_types = df['School Type'].nunique()

        # Create a simple bar chart to show school type distribution
        school_type_counts = df['School Type'].value_counts()

        fig = go.Figure(go.Bar(
            x=school_type_counts.index,
            y=school_type_counts.values,
            marker=dict(color='#2a4d69')
        ))

        fig.update_layout(
            title="School Type Distribution",
            xaxis_title="School Type",
            yaxis_title="Count",
            height=220,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )

        return dbc.Card(
            dbc.CardBody([
                html.Div("Total Schools", className="text-uppercase text-muted small fw-bold mb-1"),
                html.H2(f"{total_schools}", className="fw-bold mb-3", style={'color': '#0a1f44'}),

                html.Div([
                    html.Div(f"Total School Types: {school_types}", className="text-muted mb-3"),
                    html.Div(dcc.Graph(figure=fig, config={'displayModeBar': False}), style={'flex': '0 0 auto'})
                ], style={'display': 'flex', 'alignItems': 'center'})
            ]),
            className="mb-4 shadow-sm"
        )

    return dbc.Card(dbc.CardBody(html.Div("Mode not supported")), className="mb-4 shadow-sm")
