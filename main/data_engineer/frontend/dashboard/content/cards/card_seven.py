import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

def card_seven(df, mode):
    # Define relevant grade level columns
    male_cols = [
        'k_male', 'g1_male', 'g2_male', 'g3_male', 'g4_male', 'g5_male',
        'g6_male', 'g7_male', 'g8_male', 'g9_male',
        'g10_male', 'elem_ng_male', 'jhs_ng_male'
    ]
    female_cols = [
        'k_female', 'g1_female', 'g2_female', 'g3_female', 'g4_female', 'g5_female',
        'g6_female', 'g7_female', 'g8_female', 'g9_female',
        'g10_female', 'elem_ng_female', 'jhs_ng_female'
    ]

    grade_labels = [
        'K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6',
        'G7', 'G8', 'G9', 'G10', 'Elem NG', 'JHS NG'
    ]

    if mode == 'student':
        # Sum total enrollment per grade level across the entire DataFrame
        total_male = df[male_cols].sum()
        total_female = df[female_cols].sum()

    elif mode == 'school':
        # Count unique schools with non-zero values per grade level
        df_unique = df.drop_duplicates(subset='beis_school_id')

        def count_nonzero(cols):
            return df_unique[cols].gt(0).sum()

        total_male = count_nonzero(male_cols)
        total_female = count_nonzero(female_cols)

    else:
        raise ValueError("Mode must be either 'student' or 'school'")

    y_male = total_male.tolist()
    y_female = total_female.tolist()

    # Plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=grade_labels,
        y=y_male,
        mode='lines+markers',
        name='Male',
        line=dict(color='blue'),
        marker=dict(size=8)
    ))

    fig.add_trace(go.Scatter(
        x=grade_labels,
        y=y_female,
        mode='lines+markers',
        name='Female',
        line=dict(color='deeppink'),
        marker=dict(size=8)
    ))

    fig.update_layout(
        title=dict(
            text="Grade Level Enrollment by Gender",
            x=0.05,
            font=dict(size=20, color='darkblue')
        ),
        xaxis_title="Grade Level",
        yaxis_title="Total Enrollment" if mode == 'student' else "Total Schools",
        margin=dict(l=60, r=20, t=60, b=40),
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(orientation="h", y=-0.2, x=0.3)
    )

    return html.Div([
        dcc.Graph(figure=fig, config={'displayModeBar': False}),
    ], className="card-seven-container", style={"width": "50em", "height": "10em"})