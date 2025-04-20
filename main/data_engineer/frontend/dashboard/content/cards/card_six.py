import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
from dash.dependencies import Input, Output

# --- UI Components --- #

from dash import html, dcc
import dash_bootstrap_components as dbc

filter1_dropdown = dbc.Select(
    id='location-filter',
    options=[
        {'label': 'By Region', 'value': 'region'},
        {'label': 'By Division', 'value': 'division'},
        {'label': 'By District', 'value': 'district'},
        {'label': 'By Legislative District', 'value': 'legislative_district'},
        {'label': 'By Province', 'value': 'province'},
        {'label': 'By Municipality', 'value': 'municipality'},
        {'label': 'By Barangay', 'value': 'barangay'},
    ],
    value='region',
    persistence=True,
    className='filter-dropdown-location w-50'
)

order_radio = dbc.RadioItems(
    id='card-six-order-toggle',
    options=[
        {'label': 'Highest', 'value': 'desc'},
        {'label': 'Lowest', 'value': 'asc'}
    ],
    value='asc',
    inline=True,
    persistence=True,
    className='order-toggle-radio w-50'
)


# --- Core Logic --- #

def get_total_by_mode(df, mode):
    if df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

    if mode == 'student':
        cols = [col for col in df.columns if any(g in col for g in [
            'k_', 'g1_', 'g2_', 'g3_', 'g4_', 'g5_', 'g6_', 'elem_ng_',
            'g7_', 'g8_', 'g9_', 'g10_', 'jhs_ng_', 'g11_', 'g12_'
        ]) and ('_male' in col or '_female' in col)]
        df['value'] = df[cols].sum(axis=1)
    else:
        df = df.drop_duplicates(subset='beis_school_id')
        df['value'] = 1  # Count schools

    return df

def generate_card_six_figure(df, group_col, order):
    grouped = df.groupby(group_col)['value'].sum().reset_index()
    grouped = grouped.sort_values(by='value', ascending=(order == 'asc')).tail(10)

    # Truncate long labels but keep full label for hover
    MAX_LABEL_LENGTH = 30
    grouped['short_label'] = grouped[group_col].apply(
        lambda x: x if len(x) <= MAX_LABEL_LENGTH else x[:MAX_LABEL_LENGTH] + '...'
    )
    grouped['hover_label'] = grouped[group_col]

    fig = go.Figure(go.Bar(
        x=grouped['value'],
        y=grouped['short_label'],  # Truncated label on y-axis
        orientation='h',
        marker=dict(color=grouped['value'], colorscale='Viridis'),
        hovertext=grouped['hover_label'],  # Full label on hover
        hoverinfo='text+x'
    ))

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        autosize=True,
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )
    fig.update_yaxes(autorange="reversed", ticksuffix='  ', tickfont=dict(size=11))

    return fig


# --- Card Layout --- #

def card_six(df, location, mode, hierarchy_order):
    df = get_total_by_mode(df, mode)
    group_col = location
    fig = generate_card_six_figure(df, group_col, hierarchy_order)

    return html.Div([
        html.Div([html.Div(f"ENROLLMENT BY {group_col.upper()}", className='card-title-main')], className='card-header-wrapper'),
        html.Div([
            html.Div("View:", className="highlight-label"),
            html.Div([order_radio,filter1_dropdown], className="filter-wrapper")
        ], className='card-filter-wrapper'),
        html.Div([dcc.Graph(id='card-six-graph', figure=fig, config={'displayModeBar': False})])
    ], id='card-six-id', className="card card-six")

# --- Callback Registration --- #

def card_six_register_callbacks(app):
    from main.data_engineer.frontend.dashboard.content.content import convert_filter_to_df

    @app.callback(
        Output('selected-filters', 'data'),
        Input('location-filter', 'value'),
        Input('card-six-order-toggle', 'value'),
        Input('mode-filter', 'value'),
        prevent_initial_call=True
    )
    def store_selected_filters(location, order, mode):
        print(f"Selected filters: {location}, {order}, {mode}")
        return {
            'location': location,
            'hierarchy_order': order,
            'mode': mode
        }

    @app.callback(
        Output('card-six-graph', 'figure'),
        [Input('selected-filters', 'data'),
         Input('current-filter-dict', 'data')]
    )
    def update_card_six(filter_dict, json_df):
        location = filter_dict.get('location', 'region')
        order = filter_dict.get('hierarchy_order', 'desc')
        mode = filter_dict.get('mode', 'student')
        df = convert_filter_to_df(json_df)
        df = get_total_by_mode(df, mode)
        group_col = location
        return generate_card_six_figure(df, group_col, order)