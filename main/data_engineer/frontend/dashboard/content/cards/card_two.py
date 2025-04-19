import pandas as pd
from dash import html, dcc
import plotly.graph_objs as go

def card_two(df, mode):
    if df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

    def compute_totals(df, level):
        grade_groups = {
            "elementary": ['k_male','k_female','g1_male','g1_female','g2_male','g2_female','g3_male','g3_female',
                           'g4_male','g4_female','g5_male','g5_female','g6_male','g6_female',
                           'elem_ng_male','elem_ng_female'],
            "junior_high": ['g7_male','g7_female','g8_male','g8_female','g9_male','g9_female','g10_male','g10_female',
                            'jhs_ng_male','jhs_ng_female'],
            "senior_high": ['g11_acad_-_abm_male','g11_acad_-_abm_female','g11_acad_-_humss_male','g11_acad_-_humss_female',
                            'g11_acad_stem_male','g11_acad_stem_female','g11_acad_gas_male','g11_acad_gas_female',
                            'g11_acad_pbm_male','g11_acad_pbm_female','g11_tvl_male','g11_tvl_female',
                            'g11_sports_male','g11_sports_female','g11_arts_male','g11_arts_female',
                            'g12_acad_-_abm_male','g12_acad_-_abm_female','g12_acad_-_humss_male','g12_acad_-_humss_female',
                            'g12_acad_stem_male','g12_acad_stem_female','g12_acad_gas_male','g12_acad_gas_female',
                            'g12_acad_pbm_male','g12_acad_pbm_female','g12_tvl_male','g12_tvl_female',
                            'g12_sports_male','g12_sports_female','g12_arts_male','g12_arts_female']
        }

        group = grade_groups[level]
        male_cols = [col for col in group if col.endswith('_male')]
        female_cols = [col for col in group if col.endswith('_female')]

        total_male = df[male_cols].sum().sum()
        total_female = df[female_cols].sum().sum()
        total = total_male + total_female

        male_percentage = round((total_male / total) * 100, 1) if total else 0
        female_percentage = round((total_female / total) * 100, 1) if total else 0

        return total_male, total_female, male_percentage, female_percentage

    def create_card(level_name, level_key):
        male_total, female_total, male_pct, female_pct = compute_totals(df, level_key)

        bar_chart = dcc.Graph(
            className='gender-bar-chart',
            config={'displayModeBar': False},
            figure={
                'data': [
                    go.Bar(
                        x=['Enrollment'],
                        y=[male_total],
                        name='Male',
                        marker_color='#2a4d69',
                    ),
                    go.Bar(
                        x=['Enrollment'],
                        y=[female_total],
                        name='Female',
                        marker_color='#f28cb1',
                    )
                ],
                'layout': go.Layout(
                    barmode='group',  # Changed from 'group' to 'stack'
                    height=120,
                    width=60,
                    bargap=0.1,
                    margin={'l': 0, 'r': 0, 't': 0, 'b': 5},
                    showlegend=False,
                    xaxis=dict(
                        showline=False,
                        showgrid=False,
                        zeroline=False,
                        showticklabels=False
                    ),
                    yaxis=dict(
                        showline=False,
                        showgrid=False,
                        zeroline=False,
                        showticklabels=False
                    )
                )
            }
        )



        return html.Div([
            html.Div([
                html.Div([
                    html.Div(level_name.upper(), className='card-title-main'),
                ], className='card-header-wrapper'),
                html.Div([
                    html.Div(f"{male_total + female_total:,}", className='total-count'),
                    html.Div("STUDENTS", className='card-title-sub')
                ], className='card-header-wrapper'),
                html.Div([
                    html.Div([
                        html.Span(className="legend-dot male"),
                        html.Span(f"{male_pct}%", className="legend-percentage male"),
                        html.Span(" MALE", className="legend-label male"),
                    ], className="legend-item"),

                    html.Div([
                        html.Span(className="legend-dot female"),
                        html.Span(f"{female_pct}%", className="legend-percentage female"),
                        html.Span(" FEMALE", className="legend-label female"),
                    ], className="legend-item")
                ], className="card-one-two-legend"),
            ],className="card-one-two-text"),
            html.Div(
                bar_chart,
                className="bar-chart-container",
                style={"marginTop": "auto"}
            ),
        ], className='card card-one-two')

    return [
        create_card("Elementary School", "elementary"),
        create_card("Junior High School", "junior_high"),
        create_card("Senior High School", "senior_high")
    ]
