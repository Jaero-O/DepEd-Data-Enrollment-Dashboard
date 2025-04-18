import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go
import re
import os
from datetime import datetime

def detect_school_year(df, file_path=None):
    if df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")
        
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

def card_one(df, mode):
    if df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

    if mode == 'student':
        school_year = detect_school_year(df)

        male_columns = [col for col in df.columns if col.lower().endswith('_male')]
        female_columns = [col for col in df.columns if col.lower().endswith('_female')]

        total_male = df[male_columns].sum().sum()
        total_female = df[female_columns].sum().sum()
        total_enrollment = total_male + total_female

        male_pct = round((total_male / total_enrollment) * 100, 1) if total_enrollment > 0 else 0
        female_pct = round((total_female / total_enrollment) * 100, 1) if total_enrollment > 0 else 0

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
                text=school_year,
                x=0.5, y=0.5,
                font_size=14,
                showarrow=False,
                align='center'
            )],
            margin=dict(t=0, b=0, l=0, r=0),
            showlegend=False,
            height=180,
            width=180,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        gender_legend = html.Div([
            html.Div([
                html.Span(style={
                    'width': '20px', 'height': '12px',
                    'backgroundColor': '#2a4d69',
                    'borderRadius': '6px',
                    'display': 'inline-block',
                    'marginRight': '6px'
                }),
                html.Span(f"{male_pct}%", style={'fontWeight': 'bold', 'color': '#2a4d69', 'fontSize': '18px'}),
                html.Span(" MALE", style={'fontWeight': '500', 'color': '#2a4d69', 'fontSize': '12px'})
            ], className='mb-1'),

            html.Div([
                html.Span(style={
                    'width': '20px', 'height': '12px',
                    'backgroundColor': '#f28cb1',
                    'borderRadius': '6px',
                    'display': 'inline-block',
                    'marginRight': '6px'
                }),
                html.Span(f"{female_pct}%", style={'fontWeight': 'bold', 'color': '#f28cb1', 'fontSize': '18px'}),
                html.Span(" FEMALE", style={'fontWeight': '500', 'color': '#f28cb1', 'fontSize': '12px'})
            ])
        ], style={'marginTop': '8px'})

        return dbc.Card(
            dbc.CardBody(
                html.Div([
                    html.Div("TOTAL ENROLLMENT", className="gender-title-main"),
                    html.H2(f"{int(total_enrollment):,}", className="fw-bold mb-3", style={'color': '#0a1f44'}),
                    html.Div(
                        dcc.Graph(figure=fig, config={'displayModeBar': False}),
                        style={'height': '180px', 'width': '180px'}
                    ),
                    gender_legend
                ], style={'display': 'inline-block'}) 
            ),
            className="mb-4 p-1",
            style={'display': 'inline-block', 'borderRadius': '12px', 'border':"none", "boxShadow": "0px 2px 10px rgba(0,0,0,0.1)"} 
        )

    elif mode == 'school':
        total_schools = df['beis_school_id'].nunique()
        return dbc.Card(
            dbc.CardBody([
                html.Div("TOTAL SCHOOLS", className="gender-title-main"),
                html.H2(f"{total_schools:,}", className="fw-bold", style={'color': '#0a1f44'}),
            ]),
            className="mb-4 p-1",
            style={'display': 'inline-block', 'borderRadius': '12px', "boxShadow": "0px 2px 10px rgba(0,0,0,0.1)"}
        )

    return dbc.Card(dbc.CardBody(html.Div("Mode not supported")), className="mb-4 p-1", style={'display': 'inline-block', 'borderRadius': '12px', "boxShadow": "0px 2px 10px rgba(0,0,0,0.1)"})



