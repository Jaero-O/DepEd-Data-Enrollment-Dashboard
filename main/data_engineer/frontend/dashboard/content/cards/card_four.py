import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

def card_four(df, mode):
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

    # Remove the location filter logic, use the whole dataset directly
    filtered_df = df.copy()

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
                hole=.3
            )
        ]
    )
    pie_chart.update_layout(
        margin=dict(t=5, b=20, l=20, r=20),
        showlegend=False,
        autosize=True  # Added width to ensure proportional scaling
    )

    # Update the dcc.Graph container to allow the pie chart to expand
    dcc.Graph(
        figure=pie_chart,
        config={'displayModeBar': False}
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
                html.Span(
                    className='legend-dot',
                    style={'backgroundColor': color}
                ),
                html.Span(f"{percentage:.1f}%", className='legend-percentage', style={'color': color}),
                html.Span(sector_label.upper(), className='legend-label', style={'color': color})
            ], className='legend-item')
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
                html.Span(legend_items[i], className='sector-label'),
                html.Span(f"{int(total):,}", className='sector-value')
            ], className='sector-line')
        )

    return html.Div([
        html.Div([html.Div(["ENROLLMENT BY SECTOR"], className="card-title-main")], className='card-header-wrapper'),
        html.Div(dcc.Graph(
            figure=pie_chart,
            config={'displayModeBar': False},
            className='pie-chart',
            style={'height': '100%', 'width': '100%'}
        ), className='graph-wrapper'),
        html.Div(sector_lines, className='sector-lines-wrapper'),
    ], className='card card-four')

def card_four_register_callbacks(app):
    return None