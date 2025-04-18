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
    df['total_enrollment'] = df[existing_columns].sum(axis=1)

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

    df['main_category'] = df['school_subclassification'].map(category_mapping)

    if mode == 'student':
        grouped = df.groupby(['school_subclassification', 'main_category'])['total_enrollment'].sum().reset_index()
        y_col = 'total_enrollment'
        title = "Total Enrollment by School Subclassification and Category"
    elif mode == 'school':
        grouped = df.groupby(['school_subclassification', 'main_category'])['beis_school_id'].nunique().reset_index()
        grouped.rename(columns={'beis_school_id': 'total_schools'}, inplace=True)
        y_col = 'total_schools'
        title = "Total Number of Schools by School Subclassification and Category"
    else:
        return html.Div("❌ Invalid mode. Use 'student' or 'school'.")

    grouped = grouped.dropna(subset=['school_subclassification', 'main_category'])

    # Sort values descending
    grouped = grouped.sort_values(by=y_col, ascending=False)

    # Create color map
    color_palette = px.colors.qualitative.Set3
    unique_subs = grouped['school_subclassification'].unique()
    color_map = {sub: color_palette[i % len(color_palette)] for i, sub in enumerate(unique_subs)}

    # Create the plot
    fig = px.bar(
        grouped,
        x='school_subclassification',
        y=y_col,
        color='school_subclassification',
        color_discrete_map=color_map,
        text_auto='.3s',
        title=title
    )


    # Determine tick values based on max
    max_val = grouped[y_col].max()
    max_power = int(np.ceil(np.log10(max_val)))
    min_power = 2 if max_val >= 100 else 0  # start from 10^2 if max is at least 100

    tickvals = [10**i for i in range(min_power, max_power + 1)]
    ticktext = [f"{int(v):,}" for v in tickvals]

    # Log scale and layout tweaks
    fig.update_layout(
        xaxis=dict(
            visible=False,
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        xaxis_title="School Subclassification",
        yaxis=dict(
            title="Count (Log Scale)" if mode == 'school' else "Total Enrollment (Log Scale)",
            type="log",
            tickvals=tickvals,
            ticktext=ticktext
        ),
        margin=dict(t=60, l=40, r=40, b=100),
        legend_title="Main Category",
        bargap=0,
        bargroupgap=0.1,
        barmode='group',
        autosize=False,
        height=400,
        width=800,
    )

    return html.Div([
        html.H4("Card 3: Grouped Vertical Bar Graph (Log Scale)", style={"marginBottom": "15px"}),
        dcc.Graph(figure=fig)
    ])