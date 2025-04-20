import pandas as pd
from dash import html, dash_table
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, callback

from main.data_engineer.frontend.dashboard.content.cards.card_tabular import COLUMN_LABELS

# Mapping of numeric inputs to Roman numeral region names
REGION_MAP = {
    "1": "Region I",
    "2": "Region II",
    "3": "Region III",
    "4": "Region IV-A",
    "4A": "Region IV-A",
    "5": "Region V",
    "6": "Region VI",
    "7": "Region VII",
    "8": "Region VIII",
    "9": "Region IX",
    "10": "Region X",
    "11": "Region XI",
    "12": "Region XII",
}

# Reverse mapping from Roman numeral region names to numeric keys
ROMAN_TO_ARABIC = {v.upper(): k for k, v in REGION_MAP.items()}

@callback(
    Output("enrollment-data-table", "data"),
    Input("enrollment-search-input", "value"),
    prevent_initial_call=True
)
def update_regional_table(search_value):
    if not search_value:
        return display_df.to_dict("records")

    # Normalize search input: uppercase and remove spaces for matching
    search_value_norm = search_value.strip().upper().replace(" ", "")

    # Initialize region_match to None
    region_match = None

    # Check if the search input corresponds to a numeric region key
    if search_value_norm in REGION_MAP:
        region_match = REGION_MAP[search_value_norm]
    else:
        # Check if input starts with "REGION" and then numeric/alpha part
        if search_value_norm.startswith("REGION"):
            key = search_value_norm.replace("REGION", "")
            if key in REGION_MAP:
                region_match = REGION_MAP[key]
        # Check if input matches a Roman numeral region name exactly
        elif search_value_norm in ROMAN_TO_ARABIC:
            region_match = search_value.strip()  # Use original casing for search

    if 'Total Schools' in display_df.columns:
        # School mode: search by region, province, municipality
        if region_match:
            # Filter by matched region only
            filtered_df = display_df[
                display_df['region'].str.contains(region_match, case=False, na=False)
            ]
        else:
            # Otherwise, search by region, province, or municipality normally
            filtered_df = display_df[
                display_df['region'].str.contains(search_value, case=False, na=False) |
                display_df['province'].str.contains(search_value, case=False, na=False) |
                display_df['municipality'].str.contains(search_value, case=False, na=False)
            ]
    else:
        # Student mode: search by school_name or school_id
        filtered_df = display_df[
            display_df['school_name'].str.contains(search_value, case=False, na=False) |
            display_df['beis_school_id'].astype(str).str.contains(search_value, case=False, na=False)
        ]

    return filtered_df.to_dict("records")


def card_regional_table(df, mode):
    global display_df

    if df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

    if mode not in ['student', 'school']:
        raise ValueError("Mode must be either 'student' or 'school'")

    location_cols = [
        'region', 'division', 'district', 'street_address', 'province',
        'municipality', 'legislative_district', 'barangay', 'beis_school_id', 'school_name'
    ]

    if 'total_enrollment' not in df.columns:
        enrollment_cols = [
            col for col in df.columns if any(g in col for g in [
                'k_', 'g1_', 'g2_', 'g3_', 'g4_', 'g5_', 'g6_', 'elem_ng_',
                'g7_', 'g8_', 'g9_', 'g10_', 'jhs_ng_',
                'g11_', 'g12_'
            ]) and ('_male' in col or '_female' in col)
        ]
        df['total_enrollment'] = df[enrollment_cols].sum(axis=1)

    if mode == 'student':
        display_cols = location_cols + ['total_enrollment']
        display_df = df.loc[:, display_cols].copy()
        placeholder_text = "Search by School Name or School ID..."
    else:  # school mode
        grouped = (
            df.groupby(['region', 'province', 'municipality'], sort=False)
              .agg(total_schools=('beis_school_id', 'nunique'))
              .reset_index()
        )
        grouped.rename(columns={'total_schools': 'Total Schools'}, inplace=True)
        display_df = grouped[['region', 'province', 'municipality', 'Total Schools']].copy()
        placeholder_text = "Search by Region, Province or Municipality..."

    display_df.reset_index(drop=True, inplace=True)

    # Column label mapping
    column_labels = {
        'region': COLUMN_LABELS.get('region', 'Region'),
        'province': COLUMN_LABELS.get('province', 'Province'),
        'municipality': COLUMN_LABELS.get('municipality', 'Municipality'),
        'Total Schools': 'Total Schools',
        'total_enrollment': 'Total Enrollment',
        **{col: COLUMN_LABELS.get(col, col.replace("_", " ").title()) for col in location_cols}
    }

    return dbc.Card(
        dbc.CardBody([
            html.Div(
                "ENROLLMENT SUMMARY PER REGION",
                className="text-uppercase text-muted small fw-bold mb-3",
                style={'fontSize': '18px', 'color': '#2a4d69'}
            ),
            html.Div([
                dcc.Input(
                    id="enrollment-search-input",
                    type="text",
                    placeholder=placeholder_text,
                    style={
                        'width': '100%',
                        'height': '30px',
                        'padding': '10px',
                        'marginBottom': '10px',
                        'border': '1px solid #ccc',
                        'borderRadius': '5px',
                        'fontFamily': '"Segoe UI", sans-serif'
                    }
                ),
                dash_table.DataTable(
                    id="enrollment-data-table",
                    data=display_df.to_dict("records"),
                    columns=[
                        {"name": column_labels.get(col, col.replace("_", " ").title()), "id": col}
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
                    page_action='native'
                )
            ],
                style={
                    'maxWidth': '1200px',
                    'margin': '0 auto',
                    'backgroundColor': 'white'
                }
            )
        ]),
        className="mb-4 shadow-sm rounded-4",
        style={'backgroundColor': 'white', 'padding': '20px'}
    )
