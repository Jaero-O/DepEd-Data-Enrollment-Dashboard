from dash import Input, Output, State, MATCH, ALL, ctx, html, dcc
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
    html.Div([
        html.Span('School Enrollment Dashboard', className='My-Dashboard-title'),
        html.Button(
            children=[
                html.I(className="fa fa-filter"), html.Span('Hide Filter', className='hide-filter', id='filter-button-text')
            ],
            className='filter-button',
            id='toggle-button',
            n_clicks=0
        )
    ], className='header-tab'),

    html.Div([
        html.Span('Filtering Menu', className='filter-menu-title'),
        html.Div([
            html.Span("Select range of school year:", className='label-text'),
            dcc.RangeSlider(
                id='year-range-slider',
                min=2000,
                max=2025,
                step=1,
                marks={str(year): str(year) for year in range(2000, 2026)},
                value=[2000, 2025],
                tooltip={"placement": "bottom", "always_visible": True}
            ),
        ], className='slider-filtering-div'),
        
        html.Div([
            html.Div([
                html.Span('Educational Divisions', className='filter-menu-title'),
                html.Div([
                    html.Div([
                        # html.Span(label, className='label-text'),
                        html.Div([
                            dbc.DropdownMenu(
                                label=label,
                                children=[
                                    dcc.Input(
                                        id={'type': 'search', 'index': label},
                                        type="text",
                                        placeholder="Search...",
                                        debounce=True,
                                        style={"margin": "0.5rem", "width": "90%"}
                                    ),
                                    dbc.Checklist(
                                        id={'type': 'chk', 'index': label},
                                        options=[],
                                        value=[],
                                        className='checklist-menu px-3',
                                        style={'maxHeight': '200px', 'overflowY': 'auto'}
                                    ),
                                    html.Button(
                                        "Load More",
                                        id={'type': 'load-more', 'index': label},
                                        n_clicks=0,
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
                html.Span('Local Government Units', className='filter-menu-title units'),
                html.Div([
                    *[html.Div([
                        # html.Span(label, className='label-text'),
                        html.Div([
                            dbc.DropdownMenu(
                                label=label,
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
                    html.Button([html.I(className='fa fa-times'),'Reset All Dropdowns'], id='reset-button', n_clicks=0, className='dropdown-menu-button reset-button'),
                ], className='dropdown-filtering-div12'),
            ], className='dropdown-filtering-div1'),
        ], className='dropdown-search-filtering-div')
    ], className='filtering-div open', id='filter-container'),

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
        Input("tabs", "value")
    )
    def update_tab_content(selected_tab):
        return dashboardContent(selected_tab)

    # Callback to toggle filter visibility
    @app.callback(
        [Output('filter-container', 'className'),
         Output('filter-button-text', 'children')],
        Input('toggle-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def toggle_filters(n_clicks):
        if n_clicks % 2 == 1:
            return 'filtering-div close', "Show Filters"
        else:
            return 'filtering-div open', "Hide Filters"
        
    # Callback to update checklist options based on selected values and search input
    @app.callback(
        Output({'type': 'chk', 'index': ALL}, 'options'),
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

        return new_options



    # Reset checklist when the delete icon is clicked
    @app.callback(
        Output({'type': 'chk', 'index': MATCH}, 'value'),
        Input({'type': 'delete', 'index': MATCH}, 'n_clicks'),
        prevent_initial_call=True
    )
    def reset_checklist(n_clicks):
        return []