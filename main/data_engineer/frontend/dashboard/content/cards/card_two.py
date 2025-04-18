import pandas as pd
from dash import html, dcc
import plotly.graph_objs as go

def card_two(df, location, mode):
    if df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

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

    def compute_student_totals(df, level):
        group = grade_groups[level]
        male_cols = [col for col in group if col.endswith('_male')]
        female_cols = [col for col in group if col.endswith('_female')]

        total_male = df[male_cols].sum().sum()
        total_female = df[female_cols].sum().sum()
        total = total_male + total_female

        male_percentage = round((total_male / total) * 100, 1) if total else 0
        female_percentage = round((total_female / total) * 100, 1) if total else 0

        return total_male, total_female, male_percentage, female_percentage

    def compute_school_totals(df, level):
        group = grade_groups[level]
        df['has_students'] = df[group].sum(axis=1) > 0
        total_schools = df[df['has_students']].shape[0]
        return total_schools

    def create_card(level_name, level_key):
        if mode == 'student':
            male_total, female_total, male_pct, female_pct = compute_student_totals(df, level_key)

            bar_chart = dcc.Graph(
                className='gender-bar-chart',
                config={'displayModeBar': False},
                figure={
                    'data': [
                        go.Bar(
                            x=['Male'],
                            y=[male_total],
                            name='Male',
                            marker_color='#2a4d69',
                            text=[f"{male_total:,}"],
                            textposition='inside',
                            insidetextanchor='end'
                        ),
                        go.Bar(
                            x=['Female'],
                            y=[female_total],
                            name='Female',
                            marker_color='#f28cb1',
                            text=[f"{female_total:,}"],
                            textposition='inside',
                            insidetextanchor='end'
                        )
                    ],
                    'layout': go.Layout(
                        barmode='group',
                        height=190,
                        bargap=0.1,
                        margin={'l': 0, 'r': 0, 't': 0, 'b': 5},
                        showlegend=False,
                        xaxis=dict(showline=True, showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showline=False, showgrid=False, zeroline=False, showticklabels=False)
                    )
                }
            )

            return html.Div([
                html.Div([
                    html.Div(level_name.upper(), className='gender-title-main'),
                    html.Div("ENROLLED STUDENTS", className='gender-title-sub')
                ], className='gender-title-wrapper'),

                html.Div(f"{male_total + female_total:,}", className='total-count'),
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
                ], className="custom-legend"),

                html.Div(
                    bar_chart,
                    className="bar-chart-container"
                ),
            ], className='gender-card')

        else:  # SCHOOL MODE
            elem_count = compute_school_totals(df, "elementary")
            jhs_count = compute_school_totals(df, "junior_high")
            shs_count = compute_school_totals(df, "senior_high")

            level_counts = {
                "elementary": elem_count,
                "junior_high": jhs_count,
                "senior_high": shs_count
            }

            labels = ["Elementary", "Junior High", "Senior High"]
            values = [elem_count, jhs_count, shs_count]
            colors = ['#6FA8DC', '#F6A5C0', '#F9CB9C']
            pull = [0.1 if level_key == "elementary" else 0,
                    0.1 if level_key == "junior_high" else 0,
                    0.1 if level_key == "senior_high" else 0]

            donut_chart = dcc.Graph(
                config={'displayModeBar': False},
                className='donut-chart',
                style={
                    "width": "190px",
                    "height": "190px"
                },
                figure={
                    "data": [go.Pie(
                        labels=labels,
                        values=values,
                        hole=0.6,
                        marker=dict(colors=colors),
                        pull=pull,
                        textinfo='none',
                    )],
                    "layout": go.Layout(
                        height=190,
                        margin={'l': 0, 'r': 10, 't': 0, 'b': 0},
                        showlegend=False,
                    )
                }
            )

            return html.Div([
                html.Div([
                    html.Div(
                        level_name.upper() if mode == 'student' else f"TOTAL {level_name.upper()}S",
                        className='gender-title-main'
                    ),
                    html.Div("ENROLLED STUDENTS", className='gender-title-sub') if mode == 'student' else None
                ], className='gender-title-wrapper'),


                html.Div(f"{level_counts[level_key]:,}", className='total-count'),

                html.Div([
                    html.Div([
                        html.Span(className="legend-dot es"),
                        html.Span("ELEMENTARY", className="legend-label es"),
                    ], className="legend-item"),

                    html.Div([
                        html.Span(className="legend-dot jhs"),
                        html.Span("JUNIOR HIGH", className="legend-label jhs"),
                    ], className="legend-item"),

                    html.Div([
                        html.Span(className="legend-dot shs"),
                        html.Span("SENIOR HIGH", className="legend-label shs"),
                    ], className="legend-item")

                ], className="custom-legend-level"),
                
                html.Div([
                    html.Div(donut_chart, className="donut-chart-container"),
                  
                    html.Div([
                        html.Span(
                            f"{round((level_counts[level_key] / sum(values)) * 100, 1) if sum(values) else 0}%",
                            className=f"legend-percentage {level_key.replace('_', '-')}"
                        ),
                        html.Span(
                            f"{level_name.upper()}",
                            className=f"legend-label {level_key.replace('_', '-')}"
                        ),
                    ], className="custom-legend-donut"),
                ], className="donut-wrapper")

            ], className='gender-card')

    return html.Div([
        html.Div([
            create_card("Elementary School", "elementary"),
            create_card("Junior High School", "junior_high"),
            create_card("Senior High School", "senior_high")
        ], className='card-two-container')
    ])
