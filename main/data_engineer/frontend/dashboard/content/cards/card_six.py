import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

def card_six(df, location, mode):
    # Load backup data if df is empty
    if df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

    # Validate mode input
    if mode not in ['student', 'school']:
        raise ValueError("Mode must be either 'student' or 'school'")

    # Define column to aggregate
    value_col = 'total_enrollment' if mode == 'student' else 'total_school'

    # Handle "Overall" mode (no groupby)
    if location == 'overall':
        total = df[value_col].sum()
        data = {
            'Location': ['Overall'],
            value_col: [total]
        }
    else:
        grouped = df.groupby(location)[value_col].sum().reset_index()
        grouped = grouped.sort_values(by=value_col, ascending=False).head(10)
        data = {
            'Location': grouped[location],
            value_col: grouped[value_col]
        }

    # Create Plotly horizontal bar chart
    fig = go.Figure(go.Bar(
        x=data[value_col],
        y=data['Location'],
        orientation='h',
        marker=dict(
            color=data[value_col],
            colorscale='Viridis'
        )
    ))

    fig.update_layout(
        title=dict(
            text="GEOGRAPHICAL LOCATION TYPE<br><sup>ENROLLMENT DATA</sup>",
            x=0.05,
            font=dict(size=20, color='darkblue')
        ),
        xaxis_title='',
        yaxis_title='',
        margin=dict(l=100, r=20, t=60, b=20),
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )

    fig.update_yaxes(autorange="reversed")

    return html.Div([
        html.Div([
            dcc.Graph(figure=fig, config={'displayModeBar': False}),
            html.Div("Highest/Lowest", className="highlight-label")
        ], className="card-six-inner")
    ], className="card-six-container")
