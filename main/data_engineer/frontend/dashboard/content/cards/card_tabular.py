import pandas as pd
from dash import html, dash_table
import dash_bootstrap_components as dbc

# Column labels with proper capitalization and translation
COLUMN_LABELS = {
    'school_name': 'School Name',
    'beis_school_id': 'BEIS School ID',
    'k_male': 'Kinder Male',
    'k_female': 'Kinder Female',
    'g1_male': 'Grade 1 Male',
    'g1_female': 'Grade 1 Female',
    'g2_male': 'Grade 2 Male',
    'g2_female': 'Grade 2 Female',
    'g3_male': 'Grade 3 Male',
    'g3_female': 'Grade 3 Female',
    'g4_male': 'Grade 4 Male',
    'g4_female': 'Grade 4 Female',
    'g5_male': 'Grade 5 Male',
    'g5_female': 'Grade 5 Female',
    'g6_male': 'Grade 6 Male',
    'g6_female': 'Grade 6 Female',
    'elem_ng_male': 'Elementary Male',
    'elem_ng_female': 'Elementary Female',
    'g7_male': 'Grade 7 Male',
    'g7_female': 'Grade 7 Female',
    'g8_male': 'Grade 8 Male',
    'g8_female': 'Grade 8 Female',
    'g9_male': 'Grade 9 Male',
    'g9_female': 'Grade 9 Female',
    'g10_male': 'Grade 10 Male',
    'g10_female': 'Grade 10 Female',
    'jhs_ng_male': 'Junior High Male',
    'jhs_ng_female': 'Junior High Female',
    'g11_acad_-_abm_male': 'Grade 11 ABM Male',
    'g11_acad_-_abm_female': 'Grade 11 ABM Female',
    'g11_acad_-_humss_male': 'Grade 11 HUMSS Male',
    'g11_acad_-_humss_female': 'Grade 11 HUMSS Female',
    'g11_acad_stem_male': 'Grade 11 STEM Male',
    'g11_acad_stem_female': 'Grade 11 STEM Female',
    'g11_acad_gas_male': 'Grade 11 GAS Male',
    'g11_acad_gas_female': 'Grade 11 GAS Female',
    'g11_acad_pbm_male': 'Grade 11 PBM Male',
    'g11_acad_pbm_female': 'Grade 11 PBM Female',
    'g11_tvl_male': 'Grade 11 TVL Male',
    'g11_tvl_female': 'Grade 11 TVL Female',
    'g11_sports_male': 'Grade 11 Sports Male',
    'g11_sports_female': 'Grade 11 Sports Female',
    'g11_arts_male': 'Grade 11 Arts Male',
    'g11_arts_female': 'Grade 11 Arts Female',
    'g12_acad_-_abm_male': 'Grade 12 ABM Male',
    'g12_acad_-_abm_female': 'Grade 12 ABM Female',
    'g12_acad_-_humss_male': 'Grade 12 HUMSS Male',
    'g12_acad_-_humss_female': 'Grade 12 HUMSS Female',
    'g12_acad_stem_male': 'Grade 12 STEM Male',
    'g12_acad_stem_female': 'Grade 12 STEM Female',
    'g12_acad_gas_male': 'Grade 12 GAS Male',
    'g12_acad_gas_female': 'Grade 12 GAS Female',
    'g12_acad_pbm_male': 'Grade 12 PBM Male',
    'g12_acad_pbm_female': 'Grade 12 PBM Female',
    'g12_tvl_male': 'Grade 12 TVL Male',
    'g12_tvl_female': 'Grade 12 TVL Female',
    'g12_sports_male': 'Grade 12 Sports Male',
    'g12_sports_female': 'Grade 12 Sports Female',
    'g12_arts_male': 'Grade 12 Arts Male',
    'g12_arts_female': 'Grade 12 Arts Female',
}

def card_tabular(df, mode):
    if df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

    if mode not in ['student', 'school']:
        raise ValueError("Mode must be either 'student' or 'school'")

    student_columns = list(COLUMN_LABELS.keys())
    school_columns = [
        'school_name', 'beis_school_id', 'sector', 'school_subclassification', 'school_type',
        'modified_coc', 'region', 'division', 'district', 'street_address',
        'province', 'municipality', 'legislative_district', 'barangay'
    ]

    selected_columns = student_columns if mode == 'student' else school_columns
    display_df = df.loc[:, selected_columns].copy()
    display_df.reset_index(drop=True, inplace=True)

    return dbc.Card(
        dbc.CardBody([
            html.Div(
                f"{mode.upper()} DATA (Tabular Form)",
                className="text-uppercase text-muted small fw-bold mb-3",
                style={'fontSize': '18px', 'color': '#2a4d69'}
            ),
            html.Div(
                dash_table.DataTable(
                    data=display_df.to_dict("records"),
                    columns=[
                        {"name": COLUMN_LABELS.get(col, col.replace("_", " ").title()), "id": col}
                        for col in display_df.columns
                    ],
                    page_size=10,
                    style_table={
                        'overflowX': 'auto',
                        'overflowY': 'auto',
                        'maxHeight': '500px',
                        'maxWidth': '100%'
                    },
                    style_header={
                        'backgroundColor': '#d9f2ff',
                        'fontWeight': 'bold',
                        'textAlign': 'center',
                        'color': '#2a4d69',
                        'fontFamily': '"Segoe UI", sans-serif'
                    },
                    style_cell={
                        'textAlign': 'center',
                        'padding': '8px',
                        'minWidth': '100px',
                        'maxWidth': '300px',
                        'whiteSpace': 'normal',
                        'fontFamily': '"Segoe UI", sans-serif'
                    },
                    style_data={
                        'backgroundColor': 'white',
                        'color': '#4f4f4f',
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f9f9f9'
                        }
                    ],
                    filter_action='none',
                    sort_action='none',
                    page_action='native'
                ),
                style={
                    'maxWidth': '1200px',
                    'margin': '0 auto',
                    'backgroundColor': 'white'
                }
            )
        ]),
        className="mb-4 shadow-sm rounded-4",
        style={
            'backgroundColor': 'white',
            'padding': '20px'
        }
    )
