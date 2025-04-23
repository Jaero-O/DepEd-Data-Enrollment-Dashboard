from dash import html, dcc
from dash import Input, Output, State, MATCH, ALL, ctx
from pathlib import Path
import os
import hashlib
import dash

from main.data_engineer.frontend.dashboard.content.cards.card_one import card_one_register_callbacks
from main.data_engineer.frontend.dashboard.content.cards.card_two import card_two_register_callbacks
from main.data_engineer.frontend.dashboard.content.cards.card_three import card_three_register_callbacks
from main.data_engineer.frontend.dashboard.content.cards.card_four import card_four_register_callbacks
from main.data_engineer.frontend.dashboard.content.cards.card_five import card_five_register_callbacks
from main.data_engineer.frontend.dashboard.content.cards.card_seven_es import card_seven_es_register_callbacks
from main.data_engineer.frontend.dashboard.content.cards.card_seven_jhs import card_seven_jhs_register_callbacks
from main.data_engineer.frontend.dashboard.content.cards.card_seven_shs import card_seven_shs_register_callbacks

from main.data_engineer.frontend.dashboard.content_layout.content_layout import content_layout, content_layout_register_callbacks
from main.data_engineer.frontend.dashboard.upload_modal import upload_modal, upload_modal_register_callbacks

def dash_callbacks(app):
    @app.callback(
        Output('tabs-wrapper', 'children'),
        Output('dashboard-main-title', 'children'),
        Input('selected-mode', 'data')
    )
    def render_tabs(mode):
        if mode == 'student':
            return dcc.Tabs(
                children=[
                    dcc.Tab(label='School-based', value='school-based', className='enrollment-tab', selected_className='enrollment-tab--selected'),
                    dcc.Tab(label='Level-based', value='level-based', className='enrollment-tab', selected_className='enrollment-tab--selected'),
                    dcc.Tab(label='Geographic-based', value='geographic-based', className='enrollment-tab', selected_className='enrollment-tab--selected'),
                    dcc.Tab(label='Yearly Analysis', value='yearly_analysis', className='enrollment-tab', selected_className='enrollment-tab--selected'),
                    dcc.Tab(label=None, value=None, style={'display':'None'}, className='enrollment-tab', selected_className='enrollment-tab--selected')
                ],
                id='tabs',
                value='school-based'
            ), "Enrollment Yearly Snapshot"
        elif mode == 'school':
            return dcc.Tabs(
                children=[
                    dcc.Tab(label='School-based', value='school-based', className='enrollment-tab', selected_className='enrollment-tab--selected'),
                    dcc.Tab(label='Geographic-based', value='geographic-based', className='enrollment-tab', selected_className='enrollment-tab--selected')
                ],
                id='tabs',
                value='school-based'
            ), "School Data"
        return None

    # card_filter_register_callbacks(app)
    # card_six_register_callbacks(app)
    # Callback for changing the theme of the page ------------------------------------------------------------------------------------------------

    @app.callback(
        Output('selected-mode', 'data'),
        Output('enrollment-data', 'className'),
        Output('school-data', 'className'),
        Input('enrollment-data', 'n_clicks'),
        Input('school-data', 'n_clicks'),
        prevent_initial_call=True
    )
    def update_selected_button(enrollment_clicks, school_clicks):
        triggered_id = ctx.triggered_id
        default_class = "submenu-item"
        active_class = "submenu-item active"
        
        if triggered_id == 'enrollment-data':
            return 'student', active_class, default_class
        elif triggered_id == 'school-data':
            return 'school', default_class, active_class
        
        return dash.no_update

    # Dropdown callback for picking school year options
    @app.callback(
        Output('school-year-dropdown-select', 'options'),
        [Input('year-range', 'value'),           # year_range is the selected range [start, end]
        Input('current-years', 'data')]        # current_years is the full list of years from dcc.Store
    )
    def populate_school_year_dropdown(year_range, current_years):
        print('current-years', current_years)
        if not year_range or not current_years:
            return []

        # Filter current_years to only include those within the selected range
        filtered_years = [y for y in current_years if year_range[0] <= y <= year_range[1]]
        filtered_years = sorted(set(y for y in filtered_years if isinstance(y, int)), reverse=True)

        # Build school year strings like "2015-2016"
        school_years = [f"{year}-{year + 1}" for year in filtered_years]

        # Construct dropdown options
        options = [{'label': 'All School Years', 'value': 'All School Years'}]
        options += [{'label': sy, 'value': sy} for sy in school_years]

        print('options:', options)

        return options

# @app.callback(
#     Output('some-output-id', 'children'),
#     Input('school-year-dropdown', 'value')
# )
# def use_selected_school_year(selected_value):
#     if selected_value == 'All School Years':
#         return "Showing all years"

#     # Extract the starting year as an integer
#     start_year = int(selected_value.split('-')[0])
#     return f"You selected the school year starting in {start_year}"


    @app.callback(
        Output("upload-modal-wrapper", "className"),
        Output("upload-modal-background-drop","className", allow_duplicate=True),
        Input("open-upload-wrapper", "n_clicks"),
        Input("close-upload-wrapper", "n_clicks"),
        Input("upload-button", "n_clicks"),
        prevent_initial_call=True
    )
    def toggle_upload_modal(open_clicks, close_clicks, close_clicks2):
        if open_clicks is None:
            open_clicks = 0
        if close_clicks is None:
            close_clicks = 0
        if close_clicks2 is None:
            close_clicks = 0

        if open_clicks > (close_clicks+close_clicks2):
            return "upload-wrapper show", "background-drop show"
        else:
            return "upload-wrapper hidden", "background-drop hidden"


    @app.callback(
        [Output('current-files', 'data'),
        Output('current-years', 'data'),
        Output('folder-hash', 'data')],
        [Input('file-check', 'n_intervals'),
        Input('folder-hash', 'data')]  # Input to detect changes in folder
    )
    def update_file_list(n, last_folder_hash):
        folder_path = Path('enrollment_database')
        filenames = [f.name for f in folder_path.iterdir() if f.is_file() and f.suffix == '.csv']
        
        # Calculate hash of the current folder contents (to detect changes)
        current_hash = hashlib.md5(''.join(filenames).encode('utf-8')).hexdigest()

        # If the folder hash is the same as the last stored hash, don't update
        if current_hash == last_folder_hash:
            return dash.no_update  # No change, return no_update
        
        # If the folder contents have changed, process the filenames
        years = []
        for f in filenames:
            name = f.replace('.csv', '')
            if name.isdigit():
                years.append(int(name))

        print(years)
        print(filenames)
        
        # Return new file list, years, and the updated folder hash
        return filenames, years, current_hash

    @app.callback(
        Output("main-container", "className"),
        Output("theme-store", "data"),
        Input("theme-toggle-switch", "value")
    )
    def toggle_theme(is_dark_mode):
        new_theme = "main-page dark-mode" if is_dark_mode else "main-page"
        return new_theme, new_theme

# Callback for updating the dropdown options based on the selected tab ------------------------------------------------------------------------------------------------

# @app.callback(
#     Output({'type': 'chk', 'index': ALL}, 'options'),
#     Input({'type': 'chk', 'index': ALL}, 'value'),
#     State('df-store', 'data'),
#     State({'type': 'chk', 'index': ALL}, 'id')
# )
# def update_all_checklists(all_values, data, all_ids):
#     df = pd.DataFrame(data)

#     # Build a dictionary of current selections
#     selections = {item['index']: val for item, val in zip(all_ids, all_values)}

#     # Filter DataFrame using current selections
#     for col, selected_vals in selections.items():
#         if selected_vals:  # Only filter if something is selected
#             df = df[df[col].isin(selected_vals)]

#     # Generate options for all checklists based on the filtered DataFrame
#     new_options = []
#     for item in all_ids:
#         col = item['index']
#         unique_vals = sorted(df[col].dropna().unique())
#         new_options.append([{'label': v, 'value': v} for v in unique_vals])

#     return new_options



# Callback for uploading the file into the server ------------------------------------------------------------------------------------------------

    ALLOWED_EXTENSIONS = ['.csv', '.xlsx']

    def allowed_file(filename):
        """Check if the file extension is allowed."""
        return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)


    # @app.callback(
    #     Output("output-data-upload", "children"),
    #     [Input("upload-data", "contents")],
    #     [State("upload-data", "filename")]
    # )
    # def upload_file(contents, filename):
    #     if contents is None:
    #         return "No file uploaded"
        
    #     if not allowed_file(filename):
    #         return html.Div([html.H5("Invalid file type. Please upload a CSV or Excel file.")])
        
    #     content_type, content_string = contents.split(',')
    #     decoded = base64.b64decode(content_string)

    #     # if "csv" not in content_type and "excel" not in content_type:
    #     #     return html.Div([html.H5("Invalid file format. Only CSV or Excel files are allowed.")])
        
    #     files = {
    #         'file': (filename, io.BytesIO(decoded), 'application/octet-stream')
    #     }
        
    #     try:
    #         response = requests.post('http://127.0.0.1:5000/api/upload-file', files=files)
    #         if response.status_code == 200:
    #             return html.Div([html.H5(response.json().get('message'))])
    #         else:
    #             return html.Div([html.H5(f"Upload failed with status {response.status_code}")])
    #     except requests.exceptions.RequestException as e:
    #         return html.Div([html.H5(f"Error occurred: {str(e)}")])
        


    content_layout_register_callbacks(app)
    upload_modal_register_callbacks(app)
    card_one_register_callbacks(app)
    card_two_register_callbacks(app)
    card_three_register_callbacks(app)
    card_four_register_callbacks(app)
    card_five_register_callbacks(app)
    # card_six_register_callbacks(app)
    card_seven_es_register_callbacks(app)
    card_seven_jhs_register_callbacks(app)
    card_seven_shs_register_callbacks(app)
