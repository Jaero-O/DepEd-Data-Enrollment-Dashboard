from dash import Input, Output, State, MATCH, ALL, ctx, html, dcc
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from main.data_engineer.frontend.dashboard.content.content import dashboardContent

data = pd.read_csv("enrollment_csv_file\\preprocessed_data\cleaned_enrollment_data.csv")

# Tab labels and options
labels_1 = ['Region', 'Division', 'District', 'Legislative District']
labels_2 = ['Province', 'Municipality', 'Barangay']
tab_labels = ['Region', 'Division', 'District', 'Province', 'Municipality', 'Legislative District', 'Barangay']

# Layout (content)
content_layout = html.Div([
    dcc.Store(id='current-filter-dict'),
    html.Div([
        html.Span('School Enrollment Dashboard', className='My-Dashboard-title'),
        html.Button(
            children=[
                html.I(className="fa fa-filter"), html.Span('Show Filter', className='hide-filter', id='filter-button-text')
            ],
            className='filter-button',
            id='toggle-button-open',
            n_clicks=0
        )
    ], className='header-tab'),

    html.Div([
        html.Div([
            html.Button(html.I(className='fa fa-times'),id='toggle-button-exit', n_clicks=0,className='exit-filter-menu'),
            html.Span('Filtering Menu', className='filter-menu-title'),
            html.Button(
                html.I(className='fa fa-refresh'), 
                id='reset-button', 
                n_clicks=0, 
                className='reset-button'
            )
        ], className='header-filter-menu'),
        html.Span("School Year Range", className='lower-title outside'),
        html.Div([
            dcc.RangeSlider(
                id='year-range-slider',
                className='year-slider',
                min=2010,
                max=2025,
                step=1,
                marks={str(year): str(year) for year in range(2000, 2026)},
                value=[2000, 2025],
                tooltip={"placement": "bottom", "always_visible": True}
            ),
        ], className='slider-filtering-div'),
        
        html.Div([
            html.Div([
                html.Span('Educational Divisions', className='lower-title'),
                html.Div([
                    html.Div([
                        html.Span(label, className='label-text'),
                        html.Div([
                            dbc.DropdownMenu(
                                id={'type': 'dropdown-label', 'index': label},
                                label='All',
                                children=[
                                    dcc.Input(
                                        id={'type': 'search', 'index': label},
                                        type="text",
                                        placeholder="Search...",
                                        debounce=True,
                                        className='search-input',
                                    ),
                                    dbc.Checklist(
                                        id={'type': 'chk', 'index': label},
                                        options=[],
                                        value=[],
                                        className='checklist-menu px-3',
                                    ),
                                    html.Button(
                                        html.I(className='fa fa-arrow-down'),
                                        id={'type': 'load-more', 'index': label},
                                        n_clicks=0,
                                        className='load-more-button',
                                        style={'marginTop': '10px'}
                                    )
                                ],
                                className="dropdown-menu-class",
                                toggle_class_name='dropdown-menu-button',
                                direction="down",
                                size="sm"
                            ),
                            html.I(className='fa fa-trash', id={'type': 'delete', 'index': label}, n_clicks=0),
                        ], className='dropdown-filtering-div3')
                    ], className='dropdown-filtering-div2') for label in labels_1
                ], className='dropdown-filtering-div12'),
                html.Span('Local Government Units', className='lower-title'),
                html.Div([
                    *[html.Div([
                        html.Span(label, className='label-text'),
                        html.Div([
                            dbc.DropdownMenu(
                                id={'type': 'dropdown-label', 'index': label},
                                label='All',
                                children=[
                                    dcc.Input(
                                        id={'type': 'search', 'index': label},
                                        type="text",
                                        placeholder="Search...",
                                        debounce=True,
                                        className='search-input',
                                    ),
                                    dbc.Checklist(
                                        id={'type': 'chk', 'index': label},
                                        options=[],
                                        value=[],
                                        className='checklist-menu px-3',
                                    ),
                                    html.Button(
                                        html.I(className='fa fa-arrow-down'),
                                        id={'type': 'load-more', 'index': label},
                                        n_clicks=0,
                                        className='load-more-button',
                                        style={'marginTop': '10px'}
                                    )
                                ],
                                className="dropdown-menu-class",
                                toggle_class_name='dropdown-menu-button',
                                direction="down",
                                size="sm"
                            ),
                            html.I(className='fa fa-trash', id={'type': 'delete', 'index': label}, n_clicks=0),
                        ], className='dropdown-filtering-div3')
                    ], className='dropdown-filtering-div2') for label in labels_2],
                ], className='dropdown-filtering-div12'),
            ], className='dropdown-filtering-div1'),
        ], className='dropdown-search-filtering-div'),
        html.Span("Filter Table Output", className='lower-title table'),
        html.Div(id='filter-table-output', className='filter-table-output')
    ], className='filtering-div', id='filter-container'),

    dcc.Tabs(
        id="tabs",
        value="Regional",
        children=[
            dcc.Tab(
                label=label,
                value=label,
                className='tab',
                selected_className='tab-selected'
            ) for label in tab_labels
        ],
        className='tabs-dcc',
    ),
    html.Div(id="tab-content", className='content-page active-tab'),
    html.Div(id="output-data-upload")
], className='tab-div')





def content_layout_register_callbacks(app):

    # Callback to update content based on active tab
    @app.callback(
        Output("tab-content", "children"),
        [
            Input("tabs", "value"),
            Input('current-filter-dict', 'data')
        ]
    )
    def update_tab_content(selected_tab, data_dict):
        return dashboardContent(selected_tab, data_dict)

    # Callback to toggle filter visibility
    @app.callback(
        Output('filter-container', 'className'),
        [Input('toggle-button-open', 'n_clicks'),
        Input('toggle-button-exit','n_clicks')],
        prevent_initial_call=True
    )
    def toggle_filters(n_clicks,n_clicks_exit):
        if n_clicks <= n_clicks_exit:
            return 'filtering-div close'
        else:
            return 'filtering-div open'
        
    # Callback to update checklist options based on selected values and search input
    @app.callback(
        [
            Output({'type': 'chk', 'index': ALL}, 'options'),
            Output({'type': 'dropdown-label', 'index': ALL}, 'label'),
            Output('current-filter-dict', 'data')
        ],
        Input({'type': 'chk', 'index': ALL}, 'value'),
        Input({'type': 'search', 'index': ALL}, 'value'),
        Input({'type': 'load-more', 'index': ALL}, 'n_clicks'),
        State({'type': 'chk', 'index': ALL}, 'options'),
        State({'type': 'chk', 'index': ALL}, 'id')
    )

    def unified_update_checklists(all_values, all_searches, all_clicks, all_options, all_ids):
        triggered = ctx.triggered_id
        df = data.copy()

        # Apply filtering based ONLY on other filters, not the current one
        selections = {item['index']: val for item, val in zip(all_ids, all_values)}
        
        new_options = []
        for item, current_opt, clicks, search_val in zip(all_ids, all_options, all_clicks, all_searches):
            col = item['index']
            filtered_df = df.copy()

            # Apply filters from other columns
            for other_col, selected_vals in selections.items():
                if selected_vals and other_col != col:
                    filtered_df = filtered_df[filtered_df[other_col].isin(selected_vals)]

            values_in_col = filtered_df[col].dropna().astype(str).unique()

            # Keep selected values even if they’re filtered out
            selected_vals = selections.get(col, [])
            preserved_vals = df[df[col].isin(selected_vals)][col].dropna().astype(str).unique()

            combined_vals = list(set(values_in_col).union(set(preserved_vals)))
            combined_vals.sort()

            # Apply search filtering
            if search_val:
                combined_vals = [v for v in combined_vals if search_val.lower() in v.lower()]

            # Apply "Load More" logic
            if triggered and triggered['type'] == 'load-more' and triggered['index'] == col:
                start_index = len(current_opt)
                next_vals = combined_vals[start_index:start_index + 10]
                options = current_opt + [{'label': v, 'value': v} for v in next_vals if v not in [opt['value'] for opt in current_opt]]
            else:
                # Initial display or search
                options = [{'label': v, 'value': v} for v in combined_vals[:10]]

            new_options.append(options)

        labels = []
        for val in all_values:
            if not val:
                labels.append("All")
            elif len(val) == 1:
                labels.append(val[0])
            else:
                labels.append("Multiple Selection")

        current_selection_dict = {
                item['index']: val for item, val in zip(all_ids, all_values) if val
        }
        print(current_selection_dict)

        return new_options, labels, current_selection_dict

    # Callback to reset all dropdowns or specific dropdowns based on delete icon clicks
    @app.callback(
        [
            Output({'type': 'chk', 'index': ALL}, 'value'),
            Output({'type': 'search', 'index': ALL}, 'value'),
        ],
        [
            Input('reset-button', 'n_clicks'),
            Input({'type': 'delete', 'index': ALL}, 'n_clicks'),
        ],
        State({'type': 'chk', 'index': ALL}, 'id'),
        prevent_initial_call=True
    )
    def reset_checklist_or_all(reset_click, delete_clicks, all_ids):
        triggered = ctx.triggered_id

        # Reset all dropdowns
        if triggered == 'reset-button':
            return [[] for _ in all_ids], ['' for _ in all_ids]

        # If a delete icon was clicked
        elif isinstance(triggered, dict) and triggered.get('type') == 'delete':
            reset_values = []
            for item in all_ids:
                if item['index'] == triggered['index']:
                    reset_values.append([])  # reset this one
                else:
                    reset_values.append(dash.no_update)  # leave others unchanged

            return reset_values, [dash.no_update] * len(all_ids)

        return [dash.no_update] * len(all_ids), [dash.no_update] * len(all_ids)
    
    # Callback to update the filter table output
    @app.callback(
        Output('filter-table-output', 'children'),
        Input('current-filter-dict', 'data')
    )
    def render_filter_table(data_dict):
        if not data_dict:
            return html.P("No filters selected.", className='no-data-msg')

        # Get the filter categories
        headers = list(data_dict.keys())

        # Find the max number of values among all keys to determine how many rows we need
        max_len = max(len(values) for values in data_dict.values())

        # Build table header row
        header_row = html.Tr([html.Th(key) for key in headers])

        # Build table rows for selected values (transpose values)
        rows = []
        for i in range(max_len):
            row = []
            for key in headers:
                values = data_dict[key]
                value = values[i] if i < len(values) else ""  # Handle uneven lists
                row.append(html.Td(value))
            rows.append(html.Tr(row))

        return html.Table(
            [header_row] + rows,
            className='filter-table'
        )

