import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
import dash_bootstrap_components as dbc

def card_four(df, location, mode):

    # Load backup data if df is empty
    if df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

    # Validate mode input
    if mode not in ['student', 'school']:
        raise ValueError("Mode must be either 'student' or 'school'")

    # Compute total enrollment if in student mode
    if mode == 'student':
        if 'total_enrollment' not in df.columns:
            enrollment_cols = [col for col in df.columns if any(g in col for g in [
                'k_', 'g1_', 'g2_', 'g3_', 'g4_', 'g5_', 'g6_', 'elem_ng_',
                'g7_', 'g8_', 'g9_', 'g10_', 'jhs_ng_',
                'g11_', 'g12_'
            ]) and ('_male' in col or '_female' in col)]
            df['total_enrollment'] = df[enrollment_cols].sum(axis=1)
        value_col = 'total_enrollment'
        title_suffix = "ENROLLMENTS"
    else:
        school_identifier = 'beis_school_id'
        df_unique = df.drop_duplicates(subset=[school_identifier])
        df_unique['total_school'] = 1
        df = df_unique
        value_col = 'total_school'
        title_suffix = "SCHOOLS"

    # Handle "overall" mode
    filtered_df = df.copy() if location == 'overall' else df[df[location].notna()]

    # Group strictly by sector column and apply display mapping
    if 'sector' in filtered_df.columns:
        sector_data = filtered_df.groupby('sector', as_index=False)[value_col].sum()

        # Mapping dataset sector names to display-friendly labels
        sector_display_map = {
            'Public': 'Public',
            'Private': 'Private',
            'SUCsLUCs': 'SUCs / LUCs',
            'PSO': 'PSO'
        }

        # Add display column for cleaner output
        sector_data['sector_display'] = sector_data['sector'].map(sector_display_map).fillna(sector_data['sector'])

        # Define desired display order
        desired_order = ['Public', 'Private', 'SUCs / LUCs', 'PSO']
        sector_data['sector_display'] = pd.Categorical(sector_data['sector_display'], categories=desired_order, ordered=True)
        sector_data = sector_data.sort_values('sector_display')
    else:
        raise ValueError("The 'sector' column is missing in the dataset.")

    # Define distinct colors for each sector
    color_map = {
        'Public': '#fbcc84',
        'Private': '#9575cd',
        'SUCs / LUCs': '#4db6ac',
        'PSO': '#447cab'
    }

    # Prepare colors list for pie chart
    pie_colors = [color_map.get(name, '#7f7f7f') for name in sector_data['sector_display']]

    # Create pie chart
    pie_chart = go.Figure(
        data=[
            go.Pie(
                labels=sector_data['sector_display'],
                values=sector_data[value_col],
                textinfo='none',
                marker=dict(colors=pie_colors),
            )
        ]
    )
    pie_chart.update_layout(
    margin=dict(t=5, b=20, l=20, r=20),
    showlegend=False,
    height=250,  # Increased height of the pie chart
    width=250,   # Added width to ensure proportional scaling
)

    # Update the dcc.Graph container to allow the pie chart to expand
    dcc.Graph(
        figure=pie_chart,
        config={'displayModeBar': False},
        style={
            'height': '300px',  # Match the height of the pie chart
            'width': '300px',   # Match the width of the pie chart
            'maxWidth': '100%', # Ensure responsiveness   
        }
    )

    # Create legend items in the same order
    legend_items = []
    total_value = sector_data[value_col].sum()
    for _, row in sector_data.iterrows():
        sector_label = row['sector_display']
        total = row[value_col]
        percentage = (total / total_value) * 100
        color = color_map.get(sector_label, '#7f7f7f')

        legend_items.append(
            html.Div([
                html.Span(style={
                    'width': '26px',
                    'height': '13px',
                    'backgroundColor': color,
                    'borderRadius': '8px',
                    'display': 'inline-block',
                    'marginRight': '8px'
                }),
                html.Span(f"{percentage:.1f}%", style={
                    'fontWeight': 'bold',
                    'color': color,  # Updated to match legend color
                    'fontSize': '18px',
                    'marginRight': '5px'
                }),
                html.Span(sector_label.upper(), style={
                    'fontWeight': 'bold',
                    'color': color,  # Updated to match legend color
                    'fontSize': '14px'
                })
            ], className='mb-2')
        )

    # Create text lines showing total count per sector
    sector_lines = []
    background_colors = ['#f9f9f9']  # Alternating background colors
    for i, row in enumerate(sector_data.iterrows()):
        _, row_data = row
        sector_label = row_data['sector_display']
        total = row_data[value_col]
        background_color = background_colors[i % len(background_colors)]  # Alternate colors

        sector_lines.append(
            html.Div([
                html.Span(sector_label, style={
                    'fontSize': '15px',
                    'fontWeight': 'bold',
                    'color': '#0a1f44',
                    'flex': '1',
                    'textAlign': 'left'
                }),
                html.Span(f"{int(total):,}", style={
                    'fontSize': '15px',
                    'fontWeight': 'bold',
                    'color': '#0a1f44',
                    'flex': '1',
                    'textAlign': 'right'
                })
            ], style={
                'display': 'flex',
                'justifyContent': 'space-between',
                'alignItems': 'center',
                'backgroundColor': background_color,
                'padding': '10px',
                'marginBottom': '5px',
                'borderRadius': '8px'
            })
        )

    return dbc.Card(
        dbc.CardBody([
            html.Div(
                "ENROLLMENT BY SECTOR",
                className="text-uppercase text-muted small fw-bold mb-1",
                style={
                    'fontSize': '19px',
                    'color': '#2a4d69',
                    'marginBottom': '-20px'  # <--- THIS is valid
                }
            ),
            html.H2(f"{sector_data[value_col].sum():,}", className="fw-bold", style={
                'color': '#000000',
                'fontSize': '40px',
                'marginBottom': '20px'
            }),
            html.Div(sector_lines, style={'marginBottom': '20px'}),
            html.Div([
                html.Div(legend_items, style={'flex': '1', 'padding': '20px'}),
                html.Div(dcc.Graph(
                    figure=pie_chart,
                    config={'displayModeBar': False},
                    style={'height': '100%', 'width': '100%'}
                ), style={
                    'flex': '1',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'height': 'auto'
                })
            ], style={
                'display': 'flex',
                'alignItems': 'center',
                'gap': '20px',
                'flexWrap': 'wrap'
            })
        ], style={
            'backgroundColor': 'white',
            'padding': '20px',
            'borderRadius': '12px'
        }),
        className="mb-4 shadow-sm rounded-4 p-3",
        style={
            'backgroundColor': '#adcbe3',
            'padding': '10px'
        }
    )
