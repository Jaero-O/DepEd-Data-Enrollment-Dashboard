from dash import Input, Output, State, MATCH, ALL, ctx, html, dcc
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from main.data_engineer.frontend.dashboard.content.content import dashboardContent, convert_filter_to_df
from main.data_engineer.frontend.dashboard.content.cards.card_filter import card_filter

data = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

column_rename_map = {
    'region': 'Region',
    'division': 'Division',
    'district': 'District',
    'beis_school_id': 'BEIS School ID',
    'school_name': 'School Name',
    'street_address': 'Street Address',
    'province': 'Province',
    'municipality': 'Municipality',
    'legislative_district': 'Legislative District',
    'barangay': 'Barangay',
    'sector': 'Sector',
    'school_subclassification': 'School Subclassification',
    'school_type': 'School Type',
    'modified_coc': 'Modified COC'
}

data.rename(columns=column_rename_map, inplace=True)

# Tab labels and options
labels_1 = ['Region', 'Division', 'District', 'Legislative District']
labels_2 = ['Province', 'Municipality', 'Barangay']
tab_labels = ['Region', 'Division', 'District', 'Province', 'Municipality', 'Legislative District', 'Barangay']

# Layout (content)
content_layout = html.Div([
    dcc.Store(id='current-filter-dict'),
    dcc.Store(id='selected-filters', storage_type='session'),
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
                html.Span('School Characteristics', className='lower-title'),
                html.Div([
                    html.Div([
                        html.Span('Sector', className='label-text'),
                        html.Div([
                            dbc.DropdownMenu(
                                id={'type': 'dropdown-label', 'index': 'Sector'},
                                label='All',
                                children=[
                                    dbc.Checklist(
                                        id={'type': 'chk', 'index': 'Sector'},
                                        options=[
                                            {'label': 'Public', 'value': 'Public'},
                                            {'label': 'Private', 'value': 'Private'},
                                            {'label': 'SUCs / LUCs', 'value': 'SUCsLUCs'},
                                            {'label': 'PSO', 'value': 'PSO'}
                                        ],
                                        value=[],
                                        className='checklist-menu px-3'
                                    )  
                                ],
                                className="dropdown-menu-class",
                                toggle_class_name='dropdown-menu-button',
                                direction="down",
                                size="sm"
                            ),
                            html.I(className='fa fa-trash', id={'type': 'delete', 'index': 'Sector'}, n_clicks=0),
                        ], className='dropdown-filtering-div3'),
                    ], className='dropdown-filtering-div2'),
                    html.Div([
                        html.Span('Subclassification', className='label-text'),
                        html.Div([
                            dbc.DropdownMenu(
                                id={'type': 'dropdown-label', 'index': 'School Subclassification'},
                                label='All',
                                children=[
                                    dbc.Checklist(
                                        id={'type': 'chk', 'index': 'School Subclassification'},
                                        options = [
                                            {'label': 'DepED Managed', 'value': 'DepED Managed'},
                                            {'label': 'DOST Managed', 'value': 'DOST Managed'},
                                            {'label': 'Local International School', 'value': 'Local International School'},
                                            {'label': 'LUC', 'value': 'LUC'},
                                            {'label': 'Non-Sectarian', 'value': 'Non-Sectarian '},
                                            {'label': 'Other GA Managed', 'value': 'Other GA Managed'},
                                            {'label': 'School Abroad', 'value': 'SCHOOL ABROAD'},
                                            {'label': 'Sectarian', 'value': 'Sectarian '},
                                            {'label': 'SUC Managed', 'value': 'SUC Managed'},
                                        ],
                                        value=[],
                                        className='checklist-menu px-3'
                                    ) 
                                ],
                                className="dropdown-menu-class",
                                toggle_class_name='dropdown-menu-button',
                                direction="down",
                                size="sm"
                            ),
                            html.I(className='fa fa-trash', id={'type': 'delete', 'index': 'School Subclassification'}, n_clicks=0),
                        ], className='dropdown-filtering-div3'),
                    ], className='dropdown-filtering-div2'),
                    html.Div([
                        html.Span('Type', className='label-text'),
                        html.Div([
                            dbc.DropdownMenu(
                                id={'type': 'dropdown-label', 'index': 'School Type'},
                                label='All',
                                children=[
                                    dbc.Checklist(
                                        id={'type': 'chk', 'index': 'School Type'},
                                        options = [
                                            {'label': 'Annex or Extension school(s)', 'value': 'Annex or Extension school(s)'},
                                            {'label': 'Mobile School(s)/Center(s)', 'value': 'Mobile School(s)/Center(s)'},
                                            {'label': 'Mother school', 'value': 'Mother school'},
                                            {'label': 'School with no Annexes', 'value': 'School with no Annexes'},
                                        ],
                                        value=[],
                                        className='checklist-menu px-3'
                                    ) 
                                ],
                                className="dropdown-menu-class",
                                toggle_class_name='dropdown-menu-button',
                                direction="down",
                                size="sm"
                            ), 
                            html.I(className='fa fa-trash', id={'type': 'delete', 'index': 'School Type'}, n_clicks=0),
                        ], className='dropdown-filtering-div3'),
                    ], className='dropdown-filtering-div2'),
                    html.Div([
                        html.Span('Level', className='label-text'),
                        html.Div([
                            dbc.DropdownMenu(
                                id={'type': 'dropdown-label', 'index': 'Modified COC'},
                                label='All',
                                children=[
                                    dbc.Checklist(
                                        id={'type': 'chk', 'index': 'Modified COC'},
                                        options = [
                                            {'label': 'Elementary School', 'value': 'Elementary School'},
                                            {'label': 'Junior High School', 'value': 'Junior High School'},
                                            {'label': 'Senior High School', 'value': 'Senior High School'},
                                        ],
                                        value=[],
                                        className='checklist-menu px-3'
                                    )
                                ],
                                className="dropdown-menu-class",
                                toggle_class_name='dropdown-menu-button',
                                direction="down",
                                size="sm"
                            ),
                            html.I(className='fa fa-trash',id={'type': 'delete', 'index':'Modified COC'}, n_clicks=0),
                        ], className='dropdown-filtering-div3'),
                    ], className='dropdown-filtering-div2'),
                ], className='dropdown-filtering-div12'),
            ], className='dropdown-filtering-div1'),
        ], className='dropdown-search-filtering-div'),
        html.Div(id='filter-table-output', className='filter-table-output')
    ], className='filtering-div', id='filter-container'),
    html.Div([
        card_filter(),
        html.Div(id="tab-dynamic-content")
    ], id="tab-content", className='content-page active-tab'),
    html.Div(id="output-data-upload")
], className='tab-div')





def content_layout_register_callbacks(app):

    # Callback to update content based on active tab
    @app.callback(
        Output("tab-dynamic-content", "children"),
        Input('current-filter-dict', 'data'),
        Input('selected-filters', 'data'),
    )
    def update_tab_content(data_dict,filter_dict):
        filter1 = filter_dict.get('filter1') if filter_dict else 'overall'  # or your default
        filter2 = filter_dict.get('filter2') if filter_dict else 'student'  # or your default
        print(filter_dict)
        print("Filter 1:", filter1)
        print("Filter 2:", filter2)
        return dashboardContent(convert_filter_to_df(data_dict), filter1, filter2)

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
            Output('current-filter-dict', 'data', allow_duplicate=True)
        ],
        Input({'type': 'chk', 'index': ALL}, 'value'),
        Input({'type': 'search', 'index': ALL}, 'value'),
        Input({'type': 'load-more', 'index': ALL}, 'n_clicks'),
        State({'type': 'chk', 'index': ALL}, 'options'),
        State({'type': 'chk', 'index': ALL}, 'id'),
        State('current-filter-dict', 'data'),
        prevent_initial_call='initial_duplicate'
    )
    def unified_checklist_callback(all_values, all_searches, all_clicks, all_options, all_ids, current_filter_dict):
        df = data.copy()
        triggered = ctx.triggered_id
        selections = {item['index']: val for item, val in zip(all_ids, all_values)}

        all_clicks = all_clicks or []
        all_searches = all_searches or []

        while len(all_clicks) < len(all_ids):
            all_clicks.append(0)
        while len(all_searches) < len(all_ids):
            all_searches.append('')

        new_options = []
        for item, current_opt, clicks, search_val in zip(all_ids, all_options, all_clicks, all_searches):
            col = item['index']

            # Fixed filters: Do not update their options dynamically
            fixed_fields = ['Sector', 'School Subclassification', 'School Type', 'Modified COC']
            if col in fixed_fields:
                new_options.append(current_opt)
                continue

            filtered_df = df.copy()

            for other_col, selected_vals in selections.items():
                if selected_vals and other_col != col:
                    filtered_df = filtered_df[filtered_df[other_col].isin(selected_vals)]

            values_in_col = filtered_df[col].dropna().astype(str).unique()
            selected_vals = selections.get(col, [])
            preserved_vals = df[df[col].isin(selected_vals)][col].dropna().astype(str).unique()

            combined_vals = list(set(values_in_col).union(set(preserved_vals)))
            combined_vals.sort()

            if search_val:
                combined_vals = [v for v in combined_vals if search_val.lower() in v.lower()]

            if triggered and triggered['type'] == 'load-more' and triggered['index'] == col:
                start_index = len(current_opt)
                next_vals = combined_vals[start_index:start_index + 10]
                options = current_opt + [
                    {'label': v, 'value': v} for v in next_vals if v not in [opt['value'] for opt in current_opt]
                ]
            else:
                options = [{'label': v, 'value': v} for v in combined_vals[:10]]

            new_options.append(options)


        # Dropdown label logic
        labels = []
        for val in all_values:
            if not val:
                labels.append("All")
            elif len(val) == 1:
                labels.append("Single Selected")
            else:
                labels.append("Multiple Selected")

        # Updating current_filter_dict
        updated_dict = current_filter_dict.copy() if current_filter_dict else {}
        for item, val in zip(all_ids, all_values):
            index = item['index']
            if index != 'Modified COC':  # don't update directly for 'Modified COC'
                updated_dict[index] = val if val else None

        # Add special logic for School Level → Modified COC (in filter dict only)
        level_vals = selections.get('Modified COC', [])
        level_all = ['Elementary School', 'Junior High School', 'Senior High School']
        selected_levels = level_vals if level_vals else level_all

        purely_map = {
            'Elementary School': 'Purely ES',
            'Junior High School': 'Purely JHS',
            'Senior High School': 'Purely SHS',
        }

        extra_value = ''
        if len(selected_levels) == 1:
            extra_value = purely_map.get(selected_levels[0], '')
        elif len(selected_levels) == 2:
            if set(selected_levels) == {'Elementary School', 'Junior High School'}:
                extra_value = ['Purely ES','Purely JHS','ES and JHS']
            elif set(selected_levels) == {'Junior High School', 'Senior High School'}:
                extra_value = ['Purely JHS','Purely SHS','JHS with SHS']
            elif set(selected_levels) == {'Elementary School', 'Senior High School'}:
                extra_value = ['Purely ES','Purely SHS']
        elif len(selected_levels) == 3:
            extra_value = ['Purely ES','Purely JHS','Purely SHS','ES and JHS','JHS with SHS','All Offering']

        updated_dict['Modified COC'] = extra_value if extra_value else None

        # Logic: If specific school filters are empty, treat as "All"
        fallback_values = {
            'Sector': None,
            'School Subclassification': None,
            'School Type': None,
            'Modified COC': None,
        }

        for key, all_vals in fallback_values.items():
            updated_dict[key] = updated_dict.get(key) or all_vals

        print("Updated Filter Dictionary:", updated_dict)
        print("Selected Values:", new_options)
        print("Selected Labels:", labels)
        print("Selected Values:", selections)


        return new_options, labels, updated_dict



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
        [
            State({'type': 'chk', 'index': ALL}, 'id'),
            State({'type': 'search', 'index': ALL}, 'id'),
        ],
        prevent_initial_call=True
    )
    def reset_checklist_or_all(reset_click, delete_clicks, chk_ids, search_ids):
        triggered = ctx.triggered_id

        if triggered == 'reset-button':
            return (
                [[] for _ in chk_ids],   # Reset all checklists
                ['' for _ in search_ids] # Reset all search inputs
            )

        elif isinstance(triggered, dict) and triggered.get('type') == 'delete':
            reset_chk = []
            reset_search = []

            for chk in chk_ids:
                if chk['index'] == triggered['index']:
                    reset_chk.append([])
                else:
                    reset_chk.append(dash.no_update)

            for search in search_ids:
                if search['index'] == triggered['index']:
                    reset_search.append('')
                else:
                    reset_search.append(dash.no_update)

            return reset_chk, reset_search

        return [dash.no_update] * len(chk_ids), [dash.no_update] * len(search_ids)


    
    # # Callback to update the filter table output
    # @app.callback(
    #     Output('filter-table-output', 'children'),
    #     Input('current-filter-dict', 'data')
    # )
    # def render_filter_table(input_dict):
    #     if not input_dict:
    #         return html.P("No filters selected.", className='no-data-msg')

    #     _, _, df = update_filter_dict_from_csv(input_dict)  # assuming this returns a DataFrame

    #     if df.empty:
    #         return html.P("No data matches the selected filters.", className='no-data-msg')

    #     # Build table header
    #     header = html.Tr([html.Th(col) for col in df.columns])

    #     # Build table rows
    #     body = []
    #     for _, row in df.iterrows():
    #         body.append(html.Tr([html.Td(row[col]) for col in df.columns]))

    #     # Return the table as an HTML Table element
    #     return html.Table([header] + body, className='filter-table')
