from dash import html, dcc
from dash.dependencies import Input, Output, State

def card_filter():
    filter1_options = [
        {'label': 'Overall', 'value': 'overall'},
        {'label': 'By Region', 'value': 'region'},
        {'label': 'By Division', 'value': 'division'},
        {'label': 'By District', 'value': 'district'},
        {'label': 'By Legislative District', 'value': 'legislative_district'},
        {'label': 'By Province', 'value': 'province'},
        {'label': 'By Municipality', 'value': 'municipality'},
        {'label': 'By Barangay', 'value': 'barangay'},
    ]

    filter2_options = [
        {'label': 'Enrollment Data', 'value': 'student'},
        {'label': 'School Data', 'value': 'school'},
    ]

    return html.Div([
        dcc.Dropdown(
            id={'type': 'dropdown', 'index': 'filter1'},
            options=filter1_options,
            value=None,
            clearable=False,
            placeholder="Select Location Filter",
            className='filter-dropdown'
        ),
        dcc.Dropdown(
            id={'type': 'dropdown', 'index': 'filter2'},
            options=filter2_options,
            value='student',
            clearable=False,
            placeholder="Select Data Type",
            className='filter-dropdown'
        ),
    ], className='card-filter')

def card_filter_register_callbacks(app):

    @app.callback(
        Output({'type': 'dropdown', 'index': 'filterLevel'}, 'value'),
        Output({'type': 'dropdown', 'index': 'filterType'}, 'value'),
        Input({'type': 'dropdown', 'index': 'filterLevel'}, 'value'),
        Input({'type': 'dropdown', 'index': 'filterType'}, 'value')
    )
    def update_filters(filter1_value, filter2_value):
        return filter1_value, filter2_value
    
    @app.callback(
        Output('selected-filters', 'data'),
        Input({'type': 'dropdown', 'index': 'filter1'}, 'value'),
        Input({'type': 'dropdown', 'index': 'filter2'}, 'value')
    )
    def update_selected_filters(filter1_value, filter2_value):
        selected_filters = {
            'filter1': filter1_value,
            'filter2': filter2_value
        }
        return selected_filters