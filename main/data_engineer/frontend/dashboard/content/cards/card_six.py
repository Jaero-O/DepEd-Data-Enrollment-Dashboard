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

    # Compute total enrollment if in student mode
    if mode == 'student':
        enrollment_cols = [col for col in df.columns if any(g in col for g in [
            'k_', 'g1_', 'g2_', 'g3_', 'g4_', 'g5_', 'g6_', 'elem_ng_',
            'g7_', 'g8_', 'g9_', 'g10_', 'jhs_ng_',
            'g11_', 'g12_'
        ]) and ('_male' in col or '_female' in col)]
        df['total_enrollment'] = df[enrollment_cols].sum(axis=1)
        value_col = 'total_enrollment'
    else:
        school_identifier = 'beis_school_id'
        df_unique = df.drop_duplicates(subset=[school_identifier])
        value_col = 'total_school'
        df_unique['total_school'] = 1
        df = df_unique

    # Treat 'overall' as 'region'
    group_col = 'region' if location == 'overall' else location

    # Group and sort
    grouped = df.groupby(group_col)[value_col].sum().reset_index()
    grouped = grouped.sort_values(by=value_col, ascending=True).tail(10)

    # Create Plotly horizontal bar chart
    fig = go.Figure(go.Bar(
        x=grouped[value_col],
        y=grouped[group_col],
        orientation='h',
        marker=dict(
            color=grouped[value_col],
            colorscale='Viridis'
        )
    ))

    fig.update_layout(
        title=dict(
            text=f"{group_col.upper()}<br><sup>ENROLLMENT DATA</sup>",
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
        ], className="card-six-inner", style={"width": "100%"}),
    ], className="card-six-container", style={"width": "30em"})

