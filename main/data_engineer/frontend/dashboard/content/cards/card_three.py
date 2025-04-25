import pandas as pd
import plotly.express as px
from dash import dcc, html
import numpy as np

def card_three(df, mode):
    enrollment_columns = [
        'k_male', 'k_female', 'g1_male', 'g1_female', 'g2_male',
        'g2_female', 'g3_male', 'g3_female', 'g4_male', 'g4_female',
        'g5_male', 'g5_female', 'g6_male', 'g6_female', 'elem_ng_male',
        'elem_ng_female', 'g7_male', 'g7_female', 'g8_male', 'g8_female',
        'g9_male', 'g9_female', 'g10_male', 'g10_female', 'jhs_ng_male',
        'jhs_ng_female', 'g11_acad_-_abm_male', 'g11_acad_-_abm_female',
        'g11_acad_-_humss_male', 'g11_acad_-_humss_female',
        'g11_acad_stem_male', 'g11_acad_stem_female',
        'g11_acad_gas_male', 'g11_acad_gas_female',
        'g11_acad_pbm_male', 'g11_acad_pbm_female',
        'g11_tvl_male', 'g11_tvl_female', 'g11_sports_male',
        'g11_sports_female', 'g11_arts_male', 'g11_arts_female',
        'g12_acad_-_abm_male', 'g12_acad_-_abm_female',
        'g12_acad_-_humss_male', 'g12_acad_-_humss_female',
        'g12_acad_stem_male', 'g12_acad_stem_female',
        'g12_acad_gas_male', 'g12_acad_gas_female',
        'g12_acad_pbm_male', 'g12_acad_pbm_female',
        'g12_tvl_male', 'g12_tvl_female', 'g12_sports_male',
        'g12_sports_female', 'g12_arts_male', 'g12_arts_female'
    ]

    existing_columns = [col for col in enrollment_columns if col in df.columns]
    df['total_enrollment'] = np.floor(df[existing_columns].sum(axis=1))

    if 'school_subclassification' not in df.columns:
        return html.Div("❌ Missing 'school_subclassification' column.")

    category_mapping = {
        'DepED Managed': 'Government-Managed Schools',
        'DOST Managed': 'Government-Managed Schools',
        'SUC Managed': 'Government-Managed Schools',
        'Local International School': 'Private and Non-Government Schools',
        'LUC': 'Private and Non-Government Schools',
        'Non-Sectarian ': 'Private and Non-Government Schools',
        'Sectarian ': 'Private and Non-Government Schools',
        'Other GA Managed': 'Private and Non-Government Schools',
        'SCHOOL ABROAD': 'International Schools'
    }

    label_mapping = {
        'DepED Managed': 'DepED<br>Managed',
        'DOST Managed': 'DOST<br>Managed',
        'SUC Managed': 'SUC<br>Managed',
        'Local International School': 'Local<br>Intl School',
        'LUC': 'LUC',
        'Non-Sectarian ': 'Non-<br>Sectarian',
        'Sectarian ': 'Sectarian',
        'Other GA Managed': 'Other GA<br>Managed',
        'SCHOOL ABROAD': 'School<br>Abroad'
    }

    df['main_category'] = df['school_subclassification'].map(category_mapping)

    if mode == 'student':
        grouped = df.groupby(['school_subclassification', 'main_category'])['total_enrollment'].sum().apply(np.floor).reset_index()
        y_col = 'total_enrollment'
        title = "Total Enrollment by School Subclassification and Category"
    elif mode == 'school':
        grouped = df.groupby(['school_subclassification', 'main_category'])['beis_school_id'].nunique().reset_index()
        grouped.rename(columns={'beis_school_id': 'total_schools'}, inplace=True)
        grouped['total_schools'] = np.floor(grouped['total_schools'])
        y_col = 'total_schools'
        title = "Total Number of Schools by School Subclassification and Category"
    else:
        return html.Div("❌ Invalid mode. Use 'student' or 'school'.")

    grouped = grouped.dropna(subset=['school_subclassification', 'main_category'])
    grouped['school_subclassification_label'] = grouped['school_subclassification'].map(label_mapping)

    grouped = grouped.sort_values(by=y_col, ascending=False)

    color_palette = [
        '#FFD06C',
        '#3377FF',
        '#53CC5B',
        '#D176F2',
        '#3CC1FF',
        '#FF828B',
        '#FFA486'
    ]
    unique_subs = grouped['school_subclassification'].unique()
    color_map = {sub: color_palette[i % len(color_palette)] for i, sub in enumerate(unique_subs)}

    grouped['formatted_value'] = grouped[y_col].apply(lambda x: f"{int(x):,}")

    fig = px.bar(
        grouped,
        x='school_subclassification_label',
        y=y_col,
        color='school_subclassification',
        color_discrete_map=color_map,
        text=grouped['formatted_value'],
        custom_data=['school_subclassification', 'formatted_value']
    )

    fig.update_traces(
        textposition='outside',
        cliponaxis=False,
        hovertemplate=(
            "School Subclassification = %{customdata[0]}<br>" +
            "Total Enrollment = %{customdata[1]}<extra></extra>"
        ),
        textfont=dict(
            family="Inter",
            size=12,
            weight="bold", 
            color="#44647E"
        )
    )

    max_val = grouped[y_col].max()
    if pd.isna(max_val) or max_val <= 0:
        tickvals = []
        ticktext = []
        y_range = None
    else:
        max_power = int(np.ceil(np.log10(max_val)))  # power of 10
        min_power = 2 if max_val >= 100 else 0
        tickvals = [10 ** i for i in range(min_power, max_power + 1)]
        ticktext = [f"{int(v):,}" for v in tickvals]
        y_range = [min_power, max_power + 1]  # +1 for extra padding

    fig.update_layout(
        xaxis=dict(
            title=None,
            tickfont=dict(family="Inter", size=12, color="#616C7E"),
            tickangle=0,
        ),
        yaxis=dict(
            title=None,
            type="log",
            tickvals=tickvals,
            ticktext=ticktext,
            tickfont=dict(family="Inter", size=12, color="#616C7E"),
            gridcolor='#F1E1CE',
            range=y_range
        ),
        showlegend=False,
        plot_bgcolor="#FFF9F1",
        paper_bgcolor='white',
        margin=dict(t=0, l=80, r=0, b=20),
        bargap=0,
        bargroupgap=0.1,
        barmode='group',
        barcornerradius=10,
        autosize=True,
    )

    return html.Div([
        html.Div([
            html.Div([
                html.Div(
                    "Enrollment by Classification",
                    className='card-title-main',
                    style={
                        'fontFamily': 'Inter',
                        'fontSize': '1em',
                        'fontWeight': '700',
                        'color': '#44647E',
                        'marginBottom': '10px'
                    }
                ),
            ], className='card-header-wrapper'),
        ], className="card-one-two-text"),
        dcc.Graph(
            figure=fig,
            config={'displayModeBar': False},
            className='card-three-graph',
            style={'width': '100%', 'height': '100%'}
        )
    ], className="card card-three")

def card_three_register_callbacks(app):
    return None