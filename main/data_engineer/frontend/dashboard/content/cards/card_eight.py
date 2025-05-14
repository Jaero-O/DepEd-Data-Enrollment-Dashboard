import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

def card_eight(current_year_df, previous_year_df,current_sy, previous_sy):
    levels = {
        'Kindergarten': ['k_male', 'k_female'],
        'Grade 1': ['g1_male', 'g1_female'],
        'Grade 2': ['g2_male', 'g2_female'],
        'Grade 3': ['g3_male', 'g3_female'],
        'Grade 4': ['g4_male', 'g4_female'],
        'Grade 5': ['g5_male', 'g5_female'],
        'Grade 6': ['g6_male', 'g6_female'],
        'Elem NG': ['elem_ng_male', 'elem_ng_female'],
        'Grade 7': ['g7_male', 'g7_female'],
        'Grade 8': ['g8_male', 'g8_female'],
        'Grade 9': ['g9_male', 'g9_female'],
        'Grade 10': ['g10_male', 'g10_female'],
        'JHS NG': ['jhs_ng_male', 'jhs_ng_female'],
        'G11 ABM': ['g11_acad_-_abm_male', 'g11_acad_-_abm_female'],
        'G11 HUMSS': ['g11_acad_-_humss_male', 'g11_acad_-_humss_female'],
        'G11 STEM': ['g11_acad_stem_male', 'g11_acad_stem_female'],
        'G11 GAS': ['g11_acad_gas_male', 'g11_acad_gas_female'],
        'G11 PBM': ['g11_acad_pbm_male', 'g11_acad_pbm_female'],
        'G11 TVL': ['g11_tvl_male', 'g11_tvl_female'],
        'G11 Sports': ['g11_sports_male', 'g11_sports_female'],
        'G11 Arts': ['g11_arts_male', 'g11_arts_female'],
        'G12 ABM': ['g12_acad_-_abm_male', 'g12_acad_-_abm_female'],
        'G12 HUMSS': ['g12_acad_-_humss_male', 'g12_acad_-_humss_female'],
        'G12 STEM': ['g12_acad_stem_male', 'g12_acad_stem_female'],
        'G12 GAS': ['g12_acad_gas_male', 'g12_acad_gas_female'],
        'G12 PBM': ['g12_acad_pbm_male', 'g12_acad_pbm_female'],
        'G12 TVL': ['g12_tvl_male', 'g12_tvl_female'],
        'G12 Sports': ['g12_sports_male', 'g12_sports_female'],
        'G12 Arts': ['g12_arts_male', 'g12_arts_female']
    }

    current_totals = []
    previous_totals = []
    level_names = []

    for level, cols in levels.items():
        current_total = current_year_df[cols].sum().sum()
        previous_total = previous_year_df[cols].sum().sum()
        current_totals.append(current_total)
        previous_totals.append(previous_total)
        level_names.append(level)

    fig = go.Figure()

    for i, level in enumerate(level_names):
        color = '#2E8B57' if current_totals[i] > previous_totals[i] else '#B22222' if current_totals[i] < previous_totals[i] else '#808080'
        fig.add_trace(go.Scatter(
            x=[level, level],
            y=[previous_totals[i], current_totals[i]],
            mode='lines',
            line=dict(color=color, width=2),
            showlegend=False
        ))

    fig.add_trace(go.Scatter(
        x=level_names,
        y=previous_totals,
        mode='markers',
        name='Previous Year',
        marker=dict(color='#084C53', size=8, symbol='circle'),
    ))

    fig.add_trace(go.Scatter(
        x=level_names,
        y=current_totals,
        mode='markers',
        name='Current Year',
        marker=dict(color='#29C8E4', size=8, symbol='circle'),
    ))

    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        autosize=True,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Segoe UI, sans-serif', size=12, color='#333'),
        xaxis=dict(
            tickangle=-50,
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='#ccc'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#f0f0f0',
            zeroline=False
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1,
            xanchor='right',
            x=1
        )
    )

    return html.Div([
        html.Div([
            html.Div([
                html.Div(f"S.Y. {current_sy} vs S.Y. {previous_sy}", className='card-title-main'),
                html.Div("Enrollment Comparison", className='card-subtitle'),
        ], className='card-header-wrapper'),

        ], className='card-header-wrapper'),
        html.Div([
            dcc.Graph(
                figure=fig,
                config={'displayModeBar': False},
                style={'width': '100%', 'height': '100%', },
            ),
        ], className='card-eight-graph-wrapper'),
    ], className='card card-eight')
