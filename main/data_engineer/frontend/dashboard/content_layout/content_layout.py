from dash import Input, Output, State, MATCH, ALL, ctx, html, dcc
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from main.data_engineer.frontend.dashboard.content.content import dashboard_content, convert_filter_to_df
from main.data_engineer.frontend.dashboard.content.cards.card_six_ni_lei import filter_location_dropdown
from main.data_analyst_scientist.data_pipeline.combine_datasets import aggregateDataset

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
    dcc.Store(id='selected-filters', data={
        'location': 'region',
        'hierarchy_order': 'desc'
    }),
    html.Div([
        html.Span("School Year Range", className='range-slider-title'),
        html.Div([
             dcc.RangeSlider(
                id='year-range',
                min=0,
                max=0,
                step=1,
                value=[1980, 2025],
                vertical=True,
                className='year-range-slider-true',
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            # Right side: year divs
            html.Div(
                id='year-list',
                className='year-list'
            )
        ], className='slider-container'),
    ],id='slider-filtering-div-id', className='slider-filtering-div'),
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
    html.Div(id="tab-dynamic-content",className='content-page active-tab' ),
    html.Div(id="output-data-upload")
], className='tab-div')





def content_layout_register_callbacks(app):
    
    @app.callback(
        [Output('year-range', 'min'),
        Output('year-range', 'max'),
        Output('year-range', 'marks'),
        Output('year-range', 'value', allow_duplicate=True)],
        Input('current-years', 'data'),
        prevent_initial_call='initial_duplicate'  # Input is the data in the store
    )
    def update_range(years):
        # Setting min and max values based on the years list
        min_year = min(years)
        max_year = max(years)

        # Creating marks for the years
        marks = {year: str(year) for year in years}

        # Setting the initial range to span from min to max year
        initial_range = [min_year, max_year]

        return min_year, max_year, marks, initial_range
    
    #dcc.Store: aggregated-years-df, 'current-year-df', 'previous-year-df'


    @app.callback(
        Output('aggregated-years-df', 'data'),
        Input('year-range', 'value'),
        State('current-years', 'data'),
        prevent_initial_call=True
    )
    def aggregated_years(year_range, current_years):
        ctx = dash.callback_context

        # Optimization: cache previous value
        if hasattr(aggregated_years, '_prev_range'):
            if aggregated_years._prev_range == year_range:
                raise dash.exceptions.PreventUpdate

        aggregated_years._prev_range = year_range

        print("Triggered by:", ctx.triggered)
        filtered_years = [y for y in current_years if year_range[0] <= y <= year_range[1]]
        aggregated_df = aggregateDataset(filtered_years).to_dict('records')
        return aggregated_df
    
    @app.callback(
        Output('current-year-df', 'data'),
        Output('previous-year-df', 'data'),
        Input('school-year-dropdown-select', 'value'),
        State('current-years', 'data'),
        State('year-range', 'value'),
        Input('aggregated-years-df', 'data'),
    )
    def current_and_previous_year_df(school_year, current_years, year_range, aggregated_years_df):
        ctx = dash.callback_context
        if ctx.triggered:
            prop_id = ctx.triggered[0]['prop_id']
            print("Function 2 triggered by:", prop_id) 
        selected_year = school_year if school_year == 'All School Years' else school_year.split('-')[0]

        filtered_years = [y for y in current_years if year_range[0] <= y <= year_range[1]]

        try:
            selected_year_int = int(selected_year)
            selected_index = filtered_years.index(selected_year_int)
            previous_year = filtered_years[selected_index - 1] if selected_index > 0 else selected_year_int
        except (ValueError, IndexError):
            previous_year = selected_year

        if selected_year == 'All School Years':
            return aggregated_years_df, aggregated_years_df
        else:
            # Load current year
            current_csv_path = f'enrollment_csv_file/cleaned_separate_datasets/{selected_year}.csv'
            current_df = pd.read_csv(current_csv_path)

            # Load previous year
            try:
                prev_csv_path = f'enrollment_csv_file/cleaned_separate_datasets/{previous_year}.csv'
                prev_df = pd.read_csv(prev_csv_path)
            except FileNotFoundError:
                prev_df = current_df.copy()  # fallback to current year data if missing

            return current_df.to_dict('records'), prev_df.to_dict('records')

    # Callback to update content based on active tab
    @app.callback(
        Output("tab-dynamic-content", "children"),
        Output('filter-location-dropdown-id', 'children'),
        Input('current-filter-dict', 'data'),
        Input('location-filter', 'value'),
        Input('selected-mode', 'data'),
        Input('tabs', 'value'),
        Input('current-year-df', 'data'),
        State('previous-year-df', 'data'),
        prevent_initial_call=True
    )
    def update_tab_content(filter_dict, location, mode, tab, current_year_df_dict, previous_year_df_dict):
        # Check if the DataFrames are empty
        ctx = dash.callback_context
        if ctx.triggered:
            prop_id = ctx.triggered[0]['prop_id']
            print("Function 3 triggered by:", prop_id) 
    
        location = location or 'region'

        # Convert dict back to DataFrame
        current_year_df = pd.DataFrame(current_year_df_dict)
        previous_year_df = pd.DataFrame(previous_year_df_dict)

        cleaned_current_year_df = convert_filter_to_df(filter_dict, current_year_df)
        cleaned_previous_year_df = convert_filter_to_df(filter_dict, previous_year_df)

        # Reverse column renaming for consistency
        reverse_column_map = {v: k for k, v in column_rename_map.items()}
        cleaned_current_year_df = cleaned_current_year_df.rename(columns=reverse_column_map)
        cleaned_previous_year_df = cleaned_previous_year_df.rename(columns=reverse_column_map)

        # Conditional UI component
        button = filter_location_dropdown if tab == 'geographic-based' else None

        # Generate content
        content = dashboard_content(cleaned_current_year_df, cleaned_previous_year_df, location, mode, tab)

        return content, button


        # # Generate content
        # content = dashboard_content(cleaned_current_year_df, cleaned_previous_year_df, location, mode, tab)
        # print(cleaned_current_year_df.columns)
        # print(cleaned_current_year_df)

        # return content, button

    # Callback to toggle filter visibility
    @app.callback(
        Output('filter-container', 'className'),
        Output('slider-filtering-div-id', 'className'),
        Output("upload-modal-background-drop","className", allow_duplicate=True),
        [Input('toggle-button-open', 'n_clicks'),
        Input('toggle-button-exit','n_clicks')],
        prevent_initial_call=True
    )
    def toggle_filters(n_clicks,n_clicks_exit):
        if n_clicks <= n_clicks_exit:
            return 'filtering-div close', 'slider-filtering-div close', "background-drop hidden"
        else:
            return 'filtering-div open', 'slider-filtering-div open', "background-drop show"
        
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
        State({'type': 'chk', 'index': ALL}, 'id'),
        State('current-filter-dict', 'data'),
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

        # Special logic for 'Modified COC'
        level_vals = selections.get('Modified COC', [])

        if level_vals:
            selected_levels = level_vals
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
                    extra_value = ['Purely ES', 'Purely JHS', 'ES and JHS']
                elif set(selected_levels) == {'Junior High School', 'Senior High School'}:
                    extra_value = ['Purely JHS', 'Purely SHS', 'JHS with SHS']
                elif set(selected_levels) == {'Elementary School', 'Senior High School'}:
                    extra_value = ['Purely ES', 'Purely SHS']
            elif len(selected_levels) == 3:
                extra_value = ['Purely ES', 'Purely JHS', 'Purely SHS', 'ES and JHS', 'JHS with SHS', 'All Offering']

            updated_dict['Modified COC'] = extra_value if extra_value else None
        else:
            updated_dict['Modified COC'] = None

        # Logic: If specific school filters are empty, treat as "All"
        fallback_values = {
            'Sector': None,
            'School Subclassification': None,
            'School Type': None,
            'Modified COC': None,
        }

        for key, all_vals in fallback_values.items():
            updated_dict[key] = updated_dict.get(key) or all_vals

        return new_options, labels, updated_dict




    # Callback to reset all dropdowns or specific dropdowns based on delete icon clicks
    @app.callback(
        [
            Output({'type': 'chk', 'index': ALL}, 'value'),
            Output({'type': 'search', 'index': ALL}, 'value'),
            Output('year-range', 'value', allow_duplicate=True)
        ],
        [
            Input('reset-button', 'n_clicks'),
            Input({'type': 'delete', 'index': ALL}, 'n_clicks'),
        ],
        [
            State({'type': 'chk', 'index': ALL}, 'id'),
            State({'type': 'search', 'index': ALL}, 'id'),
            State('current-years', 'data')
        ],
        prevent_initial_call=True
    )
    def reset_checklist_or_all(reset_click, delete_clicks, chk_ids, search_ids,range_list):
        triggered = ctx.triggered_id
        min_year = min(range_list)
        max_year = max(range_list)
        initial_range = [min_year, max_year]

        if triggered == 'reset-button':
            return (
                [[] for _ in chk_ids],   # Reset all checklists
                ['' for _ in search_ids],
                initial_range  # Reset all search inputs
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

            return reset_chk, reset_search, dash.no_update

        return [dash.no_update] * len(chk_ids), [dash.no_update] * len(search_ids), dash.no_update
    

    @app.callback(
        Output('year-list', 'children'),
        Input('year-range', 'value'),
        State('current-years', 'data'),
        prevent_initial_call = True
    )
    def update_year_list(selected_range, years_data):
        # Check if the selected values are in the current-years list
        selected_start = selected_range[0]
        selected_end = selected_range[1]

        # If the selected value is not in the years_data list, adjust to the nearest year
        if selected_start not in years_data:
            selected_start = min(years_data, key=lambda x: abs(x - selected_start))
        if selected_end not in years_data:
            selected_end = min(years_data, key=lambda x: abs(x - selected_end))

        children = []
        for year in reversed(years_data):  # Show top-down
            is_selected = selected_start <= year <= selected_end
            children.append(
                html.Div(
                    str(year),
                    className=f'year-label {"active" if is_selected else ""}',
                    id={'type': 'year-div', 'index': year},
                    n_clicks=0
                )
            )
        return children
    
    # @app.callback(
    #     Output('year-range', 'value'),
    #     Input({'type': 'year-div', 'index': dash.ALL}, 'n_clicks'),
    #     State({'type': 'year-div', 'index': dash.ALL}, 'id'),
    #     State('year-range', 'value'),
    #     State('current-years', 'data')  # Assuming this is your year list
    # )
    # def update_slider_on_year_click(n_clicks, ids, current_range, current_years):
    #     triggered = ctx.triggered_id
    #     if not triggered:
    #         return current_range

    #     clicked_year = triggered['index']
    #     if clicked_year not in current_years:
    #         return current_range

    #     min_val, max_val = current_range

    #     # Adjusting based on click location
    #     if clicked_year < min_val:
    #         return [clicked_year, max_val]
    #     elif clicked_year > max_val:
    #         return [min_val, clicked_year]
    #     else:
    #         # Snap to closest edge
    #         if abs(clicked_year - min_val) <= abs(clicked_year - max_val):
    #             return [clicked_year, max_val]
    #         else:
    #             return [min_val, clicked_year]
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
