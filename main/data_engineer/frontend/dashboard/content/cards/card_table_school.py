import pandas as pd
from dash import html, dash_table
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, callback

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
    'elem_ng_male': 'Elementary NG Male',
    'elem_ng_female': 'Elementary NG Female',
    'g7_male': 'Grade 7 Male',
    'g7_female': 'Grade 7 Female',
    'g8_male': 'Grade 8 Male',
    'g8_female': 'Grade 8 Female',
    'g9_male': 'Grade 9 Male',
    'g9_female': 'Grade 9 Female',
    'g10_male': 'Grade 10 Male',
    'g10_female': 'Grade 10 Female',
    'jhs_ng_male': 'Junior High NG Male',
    'jhs_ng_female': 'Junior High NG Female',
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

display_df = None

@callback(
    Output("student-data-table", "data"),
    Input("student-search-input", "value"),
    prevent_initial_call=True
)
def update_student_table(search_value):
    if not search_value:
        return display_df.to_dict("records")
    filtered_df = display_df[
        display_df['school_name'].str.contains(search_value, case=False, na=False) |
        display_df['beis_school_id'].astype(str).str.contains(search_value, case=False, na=False)
    ]
    return filtered_df.to_dict("records")


@callback(
    Output("school-data-table", "data"),
    Input("school-search-input", "value"),
    prevent_initial_call=True
)
def update_school_table(search_value):
    if not search_value:
        return display_df.to_dict("records")
    filtered_df = display_df[
        display_df['school_name'].str.contains(search_value, case=False, na=False) |
        display_df['beis_school_id'].astype(str).str.contains(search_value, case=False, na=False)
    ]
    return filtered_df.to_dict("records")

<<<<<<< HEAD
def card_tabular(df, mode):
    global display_df
=======

def card_tabular(df, mode):
>>>>>>> cf9d28a4dfbf380b81c067e6e0371f8670e8f3b1
    if df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

    if mode != 'student':
        raise ValueError("This view is only for student-level data summarization")

    def summarize_level(level_cols, ng_cols, labels_map):
        data = []
        total = df[level_cols + ng_cols].sum().sum()

        # Define the correct order of levels
        correct_order = ['k', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 
                        'g7', 'g8', 'g9', 'g10', 'g11', 'g12']

<<<<<<< HEAD
    return dbc.Card(
        dbc.CardBody([
            html.Div(
                f"{mode.upper()} DATA (Tabular Form)",
                className="tabular-title"
            ),
            html.Div(
                [
                    dcc.Input(
                        id=f"{mode}-search-input",
                        type="text",
                        placeholder="Search by School Name or School ID...",
                        className="search-input"
                    ),
                    dash_table.DataTable(
                        id=f"{mode}-data-table",
                        data=display_df.to_dict("records"),
                        columns=[
                            {"name": COLUMN_LABELS.get(col, col.replace("_", " ").title()), "id": col}
                            for col in display_df.columns
                        ],
                        page_size=10,
                        style_table={'overflowX': 'auto', 'overflowY': 'auto'},
                        page_action='native',
                        className="data-table"
                    )
                ],
                className="tabular-container"
            )
        ]),
        className="tabular-card"
    )
=======
        # Build unique group list based on the correct order
        groups = []
        seen = set()
        for grade in correct_order:
            for col in level_cols:
                if col.startswith(grade + '_'):
                    base = col.rsplit('_', 1)[0]
                    if base not in seen:
                        seen.add(base)
                        groups.append(base)

        for group in groups:
            male = f"{group}_male"
            female = f"{group}_female"
            if male in df and female in df:
                subtotal = df[[male, female]].sum().sum()
                percentage = (subtotal / total * 100) if total > 0 else 0
                label = labels_map.get(male, group.replace('_', ' ').title()).rsplit(' ', 1)[0]
                data.append({
                    "Grade / Strand": label,
                    "Total Enrollment": int(subtotal),
                    "% of Total": f"{percentage:.2f}%"
                })

        # Add NG total
        ng_total = df[ng_cols].sum().sum()
        if ng_total > 0:
            label = labels_map.get(ng_cols[0], "NG Group").rsplit(' ', 2)[0]
            percentage = (ng_total / total * 100) if total > 0 else 0
            data.append({
                "Grade / Strand": f"{label} NG",
                "Total Enrollment": int(ng_total),
                "% of Total": f"{percentage:.2f}%"
            })

        return pd.DataFrame(data)


    def create_table(title, data):
        return html.Div([
            html.Div([html.Div(title, className='card-title-main')], className='card-header-wrapper'),
            dash_table.DataTable(
                data=data.to_dict("records"),
                columns=[
                    {"name": "Grade / Strand", "id": "Grade / Strand"},
                    {"name": "Total Enrollment", "id": "Total Enrollment"},
                    {"name": "% of Total", "id": "% of Total"}
                ],
                style_table={'overflowX': 'auto', 'width': '100%'},
                style_header={
                    'backgroundColor': '#d9f2ff',
                    'fontWeight': 'bold',
                    'textAlign': 'center',
                    'color': '#2a4d69',
                    'fontSize': '12px',
                    'fontFamily': "Inter",
                    'borderBottom': '1px solid #ccc',
                },
                style_cell={
                    'textAlign': 'center',
                    'padding': '6px',
                    'fontFamily': "Inter-Medium",
                    'fontSize': '11px',
                    'color': '#4f4f4f',
                    'backgroundColor': 'white',
                    'border': 'none'
                },
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f9f9f9',
                    'border': 'none'
                }]
            )
        ], className="card card-level-table", style={"marginBottom": "30px"})

    # Define columns
    elementary_cols = [col for col in COLUMN_LABELS if col.startswith(('k_', 'g1_', 'g2_', 'g3_', 'g4_', 'g5_', 'g6_'))]
    elementary_ng_cols = ['elem_ng_male', 'elem_ng_female']

    jhs_cols = [col for col in COLUMN_LABELS if col.startswith(('g7_', 'g8_', 'g9_', 'g10_'))]
    jhs_ng_cols = ['jhs_ng_male', 'jhs_ng_female']

    g11_cols = [col for col in COLUMN_LABELS if col.startswith('g11_')]
    g12_cols = [col for col in COLUMN_LABELS if col.startswith('g12_')]

    # Generate summarized data
    elementary_df = summarize_level(elementary_cols, elementary_ng_cols, COLUMN_LABELS)
    jhs_df = summarize_level(jhs_cols, jhs_ng_cols, COLUMN_LABELS)
    g11_df = summarize_level(g11_cols, [], COLUMN_LABELS)
    g12_df = summarize_level(g12_cols, [], COLUMN_LABELS)

    # Return tables
    return html.Div([
        create_table("Elementary Level Enrollment", elementary_df),
        create_table("Junior High School Enrollment", jhs_df),
        create_table("Grade 11 Senior High School Enrollment", g11_df),
        create_table("Grade 12 Senior High School Enrollment", g12_df)
    ], style={
        "maxHeight": "360px",
        "overflowY": "auto",
        "paddingRight": "8px"
    })
>>>>>>> cf9d28a4dfbf380b81c067e6e0371f8670e8f3b1
