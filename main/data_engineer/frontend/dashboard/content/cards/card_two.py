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
    
    def compute_school_modes(df):
    # Define the columns that represent each level
        es_cols = ['k_male','k_female','g1_male','g1_female','g2_male','g2_female','g3_male','g3_female',
                'g4_male','g4_female','g5_male','g5_female','g6_male','g6_female','elem_ng_male','elem_ng_female']
        
        jhs_cols = ['g7_male','g7_female','g8_male','g8_female','g9_male','g9_female','g10_male','g10_female',
                    'jhs_ng_male','jhs_ng_female']
        
        shs_cols = ['g11_acad_-_abm_male','g11_acad_-_abm_female','g11_acad_-_humss_male','g11_acad_-_humss_female',
                    'g11_acad_stem_male','g11_acad_stem_female','g11_acad_gas_male','g11_acad_gas_female',
                    'g11_acad_pbm_male','g11_acad_pbm_female','g11_tvl_male','g11_tvl_female',
                    'g11_sports_male','g11_sports_female','g11_arts_male','g11_arts_female',
                    'g12_acad_-_abm_male','g12_acad_-_abm_female','g12_acad_-_humss_male','g12_acad_-_humss_female',
                    'g12_acad_stem_male','g12_acad_stem_female','g12_acad_gas_male','g12_acad_gas_female',
                    'g12_acad_pbm_male','g12_acad_pbm_female','g12_tvl_male','g12_tvl_female',
                    'g12_sports_male','g12_sports_female','g12_arts_male','g12_arts_female']

        # Compute booleans for school offerings
        df['has_es'] = df[es_cols].sum(axis=1) > 0
        df['has_jhs'] = df[jhs_cols].sum(axis=1) > 0
        df['has_shs'] = df[shs_cols].sum(axis=1) > 0

        # Count each mode
        label_map = {
            "purely_es": "Purely ES",
            "es_jhs": "ES and JHS",
            "jhs_shs": "JHS with SHS",
            "all_levels": "All Offering",
            "purely_jhs": "Purely JHS",
            "purely_shs": "Purely SHS"
        }

        coc_counts = df['modified_coc'].value_counts()

        mode_counts = {key: coc_counts.get(label, 0) for key, label in label_map.items()}
        return mode_counts

    def create_student_card(level_name, level_key):
        male_total, female_total, male_pct, female_pct = compute_totals(df, level_key)

        bar_chart = dcc.Graph(
            className='bar-chart-card-two',
            config={'displayModeBar': False},
            figure={
                'data': [
                    go.Bar(
                        x=['Male'],
                        y=[male_total],
                        name='Male',
                        marker_color='#0080FF',
                        hovertemplate='Male: %{y:,.0f}<extra></extra>'
                    ),
                    go.Bar(
                        x=['Female'],
                        y=[female_total],
                        name='Female',
                        marker_color='#FF5C85',
                        hovertemplate='Female: %{y:,.0f}<extra></extra>'
                    )
                ],
                'layout': go.Layout(
                    barmode='group', 
                    barcornerradius=7,
                    height=130,
                    width=150,
                    bargap=0.1,
                    margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',  
                    paper_bgcolor='rgba(0,0,0,0)',
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
                html.Div(level_name.title(), className='card-title-main'),
                html.Div(f"{male_total + female_total:,}", className='total-count-level'),
                html.Div("students", className='card-title-sub')
            ], className='header-wrapper'),
                
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span(className="legend-oblong male"),
                            html.Span(" MALE", className="legend-label male"),
                        ], className="legend-item"),
                        html.Span(f"{male_pct}%", className="legend-percentage male"),
                        html.Div(className="legend-line"),
                    ], className="legend-all-wrapper"),

                    html.Div([
                        html.Div([
                            html.Span(className="legend-oblong female"),
                            html.Span(" FEMALE", className="legend-label female"),
                        ], className="legend-item"),
                        html.Span(f"{female_pct}%", className="legend-percentage female"),
                    ], className="legend-all-wrapper"),
                ], className="legend-wrapper"),

                html.Div(bar_chart, className="bar-chart-container",),
            ],className="header-legend-wrapper"),                     
        ], className='card card-two')

    def create_school_card(level_name, level_key):
        mode_counts = compute_school_modes(df)

        if level_key == "elementary":
            values = [mode_counts["purely_es"], mode_counts["es_jhs"], mode_counts["all_levels"]]
            labels = ["Purely ES", "ES and JHS", "All Offering"]
            title = "Total\nElementary\nSchools"
            colors = ['#0063B3', '#008EFF', '#59B6FF']
        elif level_key == "junior_high":
            values = [mode_counts["purely_jhs"], mode_counts["es_jhs"], mode_counts["jhs_shs"], mode_counts["all_levels"]]
            labels = ["Purely JHS", "ES and JHS", "JHS and SHS", "All Offering"]
            title = "Total\nJunior High\nSchools"
            colors = ['#8C393F', '#BF4E56', '#FF6873', '#FF959D']
        else:
            values = [mode_counts["purely_shs"], mode_counts["jhs_shs"], mode_counts["all_levels"]]
            labels = ["Purely SHS", "JHS and SHS", "All Offering"]
            title = "Total\nSenior High\nSchools"
            colors = ['#CC7E00', '#FF9D00', '#FFD38C']
        
        total = sum(values)       

        donut_chart = dcc.Graph(
            config={'displayModeBar': False},
            className='donut-chart-card-two',
            figure={
                "data": [go.Pie(
                    labels=labels, 
                    values=values, 
                    hole=0.6, 
                    marker=dict(colors=colors),
                    textinfo='none')],
                "layout": go.Layout(
                    height=200,
                    width=150,
                    margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=False,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
            }
        )

        return html.Div([
            html.Div([              
                html.Div([
                    html.Div(f"{sum(values):,}", className='total-count-level-donut'),
                    html.Div("schools", className='card-title-sub-donut')
                ]),   
                html.Div(dcc.Markdown(title.replace("\n", "<br>"), dangerously_allow_html=True), className='card-title-main-donut')               
            ], className='header-wrapper-donut'),

            html.Div([
                html.Div([
                    html.Div([
                        html.Span(className=f"legend-oblong-donut {level_key}-{label.lower().replace('and', '').replace(' ', '-')}"),
                        html.Div([
                            html.Span(f"{round((value / total) * 100, 1) if total else 0}%", className=f"legend-percentage-donut {level_key}-{label.lower().replace('and', '').replace(' ', '-')}"),
                            html.Span(label.upper(), className=f"legend-label-donut {level_key}-{label.lower().replace('and', '').replace(' ', '-')}")
                        ], className="percent-label")                        
                    ], className="legend-item-donut")
                    for label, value in zip(labels, values)
                ], className="legend-wrapper-donut"),
                            
                html.Div(donut_chart, className="card-two-donut-chart-container"),
            ], className="header-legend-wrapper-donut"),
        ], className='card card-two')

    create_card = create_student_card if mode == "student" else create_school_card
    return [
        create_card("Elementary School", "elementary"),
        create_card("Junior High School", "junior_high"),
        create_card("Senior High School", "senior_high")
    ]


def card_two_register_callbacks(app):
    return None
