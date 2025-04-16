import pandas as pd
import plotly.graph_objs as go
from dash import html, dcc

def card_six(df, mode, location):
    # Validate mode input
    if mode not in ['student', 'school']:
        raise ValueError("Mode must be either 'student' or 'school'")

    # Define column to aggregate
    value_col = 'total_enrollment' if mode == 'student' else 'total_school'

    # Group by the given location and sum values
    grouped = df.groupby(location)[value_col].sum().reset_index()

    # Sort and get top 10
    top10 = grouped.sort_values(by=value_col, ascending=False).head(10)

    # Create Plotly horizontal bar chart
    fig = go.Figure(go.Bar(
        x=top10[value_col],
        y=top10[location],
        orientation='h',
        marker=dict(
            color=top10[value_col],
            colorscale='Viridis'
        )
    ))

    fig.update_layout(
        title=dict(
            text="GEOGRAPHICAL LOCATION TYPE<br><sup>ENROLLMENT DATA</sup>",
            x=0.05,
            font=dict(size=20, color='darkblue')
        ),
        xaxis=dict(title=''),
        yaxis=dict(title=''),
        margin=dict(l=100, r=20, t=60, b=20),
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
    )

    fig.update_yaxes(autorange="reversed")  # Reverse y-axis for descending bars

    return html.Div([
        html.Div([
            dcc.Graph(figure=fig, config={'displayModeBar': False}),
            html.Div("Highest/Lowest", className="highlight-label")
        ], className="card-six-inner")
    ], className="card-six-container")
