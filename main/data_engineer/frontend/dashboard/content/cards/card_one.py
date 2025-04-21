import pandas as pd
from dash import html, dcc
import plotly.graph_objs as go

def card_one(df, mode):
    if df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

    def compute_totals_all_levels(df):
        all_columns = [
            'k_male','k_female','g1_male','g1_female','g2_male','g2_female','g3_male','g3_female',
            'g4_male','g4_female','g5_male','g5_female','g6_male','g6_female','elem_ng_male','elem_ng_female',
            'g7_male','g7_female','g8_male','g8_female','g9_male','g9_female','g10_male','g10_female',
            'jhs_ng_male','jhs_ng_female',
            'g11_acad_-_abm_male','g11_acad_-_abm_female','g11_acad_-_humss_male','g11_acad_-_humss_female',
            'g11_acad_stem_male','g11_acad_stem_female','g11_acad_gas_male','g11_acad_gas_female',
            'g11_acad_pbm_male','g11_acad_pbm_female','g11_tvl_male','g11_tvl_female',
            'g11_sports_male','g11_sports_female','g11_arts_male','g11_arts_female',
            'g12_acad_-_abm_male','g12_acad_-_abm_female','g12_acad_-_humss_male','g12_acad_-_humss_female',
            'g12_acad_stem_male','g12_acad_stem_female','g12_acad_gas_male','g12_acad_gas_female',
            'g12_acad_pbm_male','g12_acad_pbm_female','g12_tvl_male','g12_tvl_female',
            'g12_sports_male','g12_sports_female','g12_arts_male','g12_arts_female'
        ]

        male_cols = [col for col in all_columns if col.endswith('_male')]
        female_cols = [col for col in all_columns if col.endswith('_female')]

        total_male = df[male_cols].sum().sum()
        total_female = df[female_cols].sum().sum()
        total = total_male + total_female

        male_percentage = round((total_male / total) * 100, 1) if total else 0
        female_percentage = round((total_female / total) * 100, 1) if total else 0

        return total_male, total_female, male_percentage, female_percentage

    def create_card():
        male_total, female_total, male_pct, female_pct = compute_totals_all_levels(df)

        bar_chart = dcc.Graph(
            className='card-one-gender-bar-chart',
            config={'displayModeBar': False},
            figure={
                'data': [
                    go.Bar(x=['Male'], y=[male_total], name='Male', marker_color='#0080FF', hovertemplate='Male: %{y}<extra></extra>'),
                    go.Bar(x=['Female'], y=[female_total], name='Female', marker_color='#FF5C85', hovertemplate='Female: %{y}<extra></extra>')
                ],
                'layout': go.Layout(
                    barmode='group',
                    barcornerradius=7,
                    height=120,
                    width=150,
                    bargap=0.1, 
                    margin={'l': 0, 'r': 0, 't': 0, 'b': 5},
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',  
                    paper_bgcolor='rgba(0,0,0,0)', 
                    xaxis=dict(showline=False, showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showline=False, showgrid=False, zeroline=False, showticklabels=False)
                )
            }
        )


        return html.Div([
            html.Div([
                html.Div("Total Enrollment", className='card-one-title-main'),
                html.Div(f"{male_total + female_total:,}", className='card-one-total-count'),
                html.Div("students", className='card-one-title-sub')
            ], className='card-one-header-wrapper'),

            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span(className="card-one-legend-dot male"),
                            html.Span("MALE", className="card-one-legend-label male")
                        ], className="card-one-legend-header"),
                        html.Span(f"{male_pct}%", className="card-one-legend-percentage male"),
                        html.Div(className="card-one-legend-divider") 
                    ], className="card-one-legend-item"),

                    html.Div([
                        html.Div([
                            html.Span(className="card-one-legend-dot female"),
                            html.Span("FEMALE", className="card-one-legend-label female")
                        ], className="card-one-legend-header"),
                        html.Span(f"{female_pct}%", className="card-one-legend-percentage female")
                    ], className="card-one-legend-item")
                ], className="card-one-legend"),

                html.Div(bar_chart, className="card-one-bar-chart-container")
            ], className="card-one-bottom-section")
        ], className='card card-one')

    return create_card()


def card_one_register_callbacks(app):
    return None
