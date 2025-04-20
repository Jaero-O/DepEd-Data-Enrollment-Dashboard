import plotly.graph_objects as go
from dash import html, dcc

def card_seven_jhs(df, mode):
    elem_labels = ['K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6']
    jhs_labels = ['G7', 'G8', 'G9', 'G10']

    elem_male = ['k_male', 'g1_male', 'g2_male', 'g3_male', 'g4_male', 'g5_male', 'g6_male']
    elem_female = ['k_female', 'g1_female', 'g2_female', 'g3_female', 'g4_female', 'g5_female', 'g6_female']

    jhs_male = ['g7_male', 'g8_male', 'g9_male', 'g10_male']
    jhs_female = ['g7_female', 'g8_female', 'g9_female', 'g10_female']

    strand_columns = {
        'ABM': {'male': ['g11_acad_-_abm_male', 'g12_acad_-_abm_male'], 'female': ['g11_acad_-_abm_female', 'g12_acad_-_abm_female']},
        'HUMSS': {'male': ['g11_acad_-_humss_male', 'g12_acad_-_humss_male'], 'female': ['g11_acad_-_humss_female', 'g12_acad_-_humss_female']},
        'STEM': {'male': ['g11_acad_stem_male', 'g12_acad_stem_male'], 'female': ['g11_acad_stem_female', 'g12_acad_stem_female']},
        'GAS': {'male': ['g11_acad_gas_male', 'g12_acad_gas_male'], 'female': ['g11_acad_gas_female', 'g12_acad_gas_female']},
        'PBM': {'male': ['g11_acad_pbm_male', 'g12_acad_pbm_male'], 'female': ['g11_acad_pbm_female', 'g12_acad_pbm_female']},
        'TVL': {'male': ['g11_tvl_male', 'g12_tvl_male'], 'female': ['g11_tvl_female', 'g12_tvl_female']},
        'Sports': {'male': ['g11_sports_male', 'g12_sports_male'], 'female': ['g11_sports_female', 'g12_sports_female']},
        'Arts': {'male': ['g11_arts_male', 'g12_arts_male'], 'female': ['g11_arts_female', 'g12_arts_female']}
    }

    if mode == 'student':
        elem_m = df[elem_male].sum().tolist()
        elem_f = df[elem_female].sum().tolist()
        jhs_m = df[jhs_male].sum().tolist()
        jhs_f = df[jhs_female].sum().tolist()
        strand_m = [df[strand_columns[s]['male']].sum().sum() for s in strand_columns]
        strand_f = [df[strand_columns[s]['female']].sum().sum() for s in strand_columns]
    elif mode == 'school':
        df_unique = df.drop_duplicates(subset='beis_school_id')

        def count_nonzero(cols):
            return df_unique[cols].gt(0).sum().tolist()

        elem_m = count_nonzero(elem_male)
        elem_f = count_nonzero(elem_female)
        jhs_m = count_nonzero(jhs_male)
        jhs_f = count_nonzero(jhs_female)
        strand_m = [df_unique[strand_columns[s]['male']].gt(0).sum().sum() for s in strand_columns]
        strand_f = [df_unique[strand_columns[s]['female']].gt(0).sum().sum() for s in strand_columns]

    strand_labels = list(strand_columns.keys())

    def create_area_chart(x_labels, male_data, female_data, title=None):
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=x_labels,
            y=male_data,
            name='Male',
            fill='tozeroy',
            mode='lines+markers',
            line=dict(color='blue', shape='spline'),
            marker=dict(size=4)
        ))

        fig.add_trace(go.Scatter(
            x=x_labels,
            y=female_data,
            name='Female',
            fill='tozeroy',
            mode='lines+markers',
            line=dict(color='deeppink', shape='spline'),
            marker=dict(size=4)
        ))

        fig.update_layout(
            title=title if title else None,
            yaxis_type='log',
            yaxis=dict(
                showline=True,
                linecolor='black',
                tickvals=[1, 10, 100, 1000, 10000, 100000, 1000000],  # Skip 2, 5
                ticktext=['1', '10', '100', '1k', '10k', '100k', '1M']
            ),
            xaxis=dict(
                showline=True,
                linecolor='black',
                tickmode='array',
                tickvals=x_labels
            ),
            height=250,
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor='white',
            paper_bgcolor='white',
            legend=dict(
                orientation="h",
                y=-0.15,
                x=1,
                xanchor='right'
            )
        )

        return fig

    return html.Div([
        html.Div([
            html.Div("ENROLLMENT DISTRIBUTION (GRADE 7 - GRADE 10)", className='card-title-main'),
        ], className='card-header-wrapper'),
        html.Div([
            # html.Div(dcc.Graph(figure=create_area_chart(elem_labels, elem_m, elem_f, "Kinder to Grade 6"), config={'displayModeBar': False}), style={'flex': 1}),
            html.Div(dcc.Graph(figure=create_area_chart(jhs_labels, jhs_m, jhs_f, "Grade 7 to Grade 10"), config={'displayModeBar': False}), style={'flex': 1}),
            # html.Div(dcc.Graph(figure=create_area_chart(strand_labels, strand_m, strand_f, "Senior High Strands"), config={'displayModeBar': False}), style={'flex': 1}),
        ], style={'display': 'flex'}),
    ], className="card card-seven jhs")