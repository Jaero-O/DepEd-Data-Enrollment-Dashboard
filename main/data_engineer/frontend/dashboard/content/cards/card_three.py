import pandas as pd
import plotly.express as px
from dash import dcc

def card_three(df, location, mode):
    if df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

    # Grade level columns
    grade_levels = [
        'k_male', 'k_female', 'g1_male', 'g1_female', 'g2_male', 'g2_female',
        'g3_male', 'g3_female', 'g4_male', 'g4_female', 'g5_male', 'g5_female',
        'g6_male', 'g6_female', 'elem_ng_male', 'elem_ng_female',
        'g7_male', 'g7_female', 'g8_male', 'g8_female', 'g9_male', 'g9_female',
        'g10_male', 'g10_female', 'jhs_ng_male', 'jhs_ng_female',
        'g11_acad_-_abm_male', 'g11_acad_-_abm_female', 'g11_acad_-_humss_male',
        'g11_acad_-_humss_female', 'g11_acad_stem_male', 'g11_acad_stem_female',
        'g11_acad_gas_male', 'g11_acad_gas_female', 'g11_acad_pbm_male',
        'g11_acad_pbm_female', 'g11_tvl_male', 'g11_tvl_female',
        'g11_sports_male', 'g11_sports_female', 'g11_arts_male',
        'g11_arts_female', 'g12_acad_-_abm_male', 'g12_acad_-_abm_female',
        'g12_acad_-_humss_male', 'g12_acad_-_humss_female',
        'g12_acad_stem_male', 'g12_acad_stem_female', 'g12_acad_gas_male',
        'g12_acad_gas_female', 'g12_acad_pbm_male', 'g12_acad_pbm_female',
        'g12_tvl_male', 'g12_tvl_female', 'g12_sports_male',
        'g12_sports_female', 'g12_arts_male', 'g12_arts_female'
    ]

    if location:
        # lowercase for consistency with CSV column names
        location = location.lower()
        if location in df.columns:
            df = df[df[location].notna()]

    if mode == 'student':
        df['total_enrollment'] = df[grade_levels].sum(axis=1)
        result_df = df.groupby('school_subclassification', as_index=False)['total_enrollment'].sum()

        fig = px.treemap(
            result_df,
            path=['school_subclassification'],
            values='total_enrollment',
            title='Total Enrollment by School Subclassification'
        )

    elif mode == 'school':
        result_df = df.dropna(subset=['beis_school_id'])
        result_df = result_df.groupby('school_subclassification')['beis_school_id'].nunique().reset_index()
        result_df.rename(columns={'beis_school_id': 'total_schools'}, inplace=True)

        fig = px.treemap(
            result_df,
            path=['school_subclassification'],
            values='total_schools',
            title='Total Schools by School Subclassification'
        )

    else:
        return dcc.Markdown("⚠️ Invalid mode. Use `'student'` or `'school'`.")

    fig.update_traces(tiling=dict(pad=2),
    textinfo="label+value",
    textfont_size=14,
    marker=dict(line=dict(width=1, color="white")),
)
    fig.update_layout(
        title=dict(
        text='<b>SCHOOL SUBCLASSIFICATION</b><br>ENROLLMENT',
        xanchor='left',
        yanchor='top'
    ),
    uniformtext=dict(minsize=10, mode='hide'),
    margin=dict(t=50, l=25, r=25, b=25),
    height=400,
    hoverlabel=dict(
        namelength=-1,
        font=dict(
            size=10 
        )
    ),
    autosize=True
    
)

    return dcc.Graph(figure=fig)
