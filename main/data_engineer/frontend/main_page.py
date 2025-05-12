import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash import Input, Output, State, MATCH, ALL, ctx
from pathlib import Path
import os
import hashlib
from dash import DiskcacheManager

from main.data_engineer.frontend.cache_file import cache

# Import pages
from main.data_engineer.frontend.dashboard.content_layout.content_layout import content_layout, content_layout_register_callbacks
from main.data_engineer.frontend.dashboard.upload_modal import upload_modal, upload_modal_register_callbacks

# Import Cards Callbacks
from main.data_engineer.frontend.dashboard.content.cards.card_six_ni_lei import filter_location_dropdown
from main.data_engineer.frontend.dashboard.content.cards.card_one import card_one_register_callbacks
from main.data_engineer.frontend.dashboard.content.cards.card_two import card_two_register_callbacks
from main.data_engineer.frontend.dashboard.content.cards.card_three import card_three_register_callbacks
from main.data_engineer.frontend.dashboard.content.cards.card_four import card_four_register_callbacks
from main.data_engineer.frontend.dashboard.content.cards.card_five import card_five_register_callbacks
from main.data_engineer.frontend.dashboard.content.cards.card_seven_es import card_seven_es_register_callbacks
from main.data_engineer.frontend.dashboard.content.cards.card_seven_jhs import card_seven_jhs_register_callbacks
from main.data_engineer.frontend.dashboard.content.cards.card_seven_shs import card_seven_shs_register_callbacks

# Import Flask Server
from main.data_engineer.backend.main_server import app as server


callback_manager = DiskcacheManager(cache)

# Initialize the Dash app
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    background_callback_manager=callback_manager
)

# website favicon and title
app.title = "DepEd Learning Management System"
# app._favicon = ("images\deped_logo.ico")
app.config.suppress_callback_exceptions = True

# Navigation Bar 
sidebar = html.Div([
    html.Div([
        # html.Img(src='./assets/images/deped_logo.png', className='depEd-logo'),
        html.Img(src='./assets/images/deped_title.png', className='depEd-title'),
    ], className='sidebar-header'),
    html.Div([
        html.Div([
            html.Div([html.I(className="fa fa-area-chart hovered"), html.Span('Dashboard', className='sidebar-li hovered'),html.I(className="fa fa-chevron-down")], className='sidebar-li-div-hovered items-wrapper'),
            html.Div([
                html.Button([
                    html.I(className="fa fa-graduation-cap"),
                    html.Span("Enrollment Data", className="submenu-link")
                ],id='enrollment-data', className="submenu-item active"),
                html.Button([
                    html.I(className="fa fa-building"),
                    html.Span("School Data", className="submenu-link")
                ],id='school-data', className="submenu-item"),
            ], className="submenu"),
        ]),
        html.Div([html.I(className="fa fa-envelope"), html.Span('Messages', className='sidebar-li')], className='items-wrapper'),
        html.Div([html.I(className="fa fa-calendar"), html.Span('Calendar', className='sidebar-li')], className='items-wrapper'),
        html.Div([html.I(className="fa fa-file"), html.Span('Legal Documents', className='sidebar-li')], className='items-wrapper'),
        html.Div([html.I(className="fa fa-database"), html.Span('Server Database', className='sidebar-li')], className='items-wrapper'),
        html.Div([html.I(className="fa fa-cog"), html.Span('Settings', className='sidebar-li')], className='items-wrapper'),
    ], className='sidebar-items'),
    html.Div([
        html.Img(src='/assets/images/kuruchan.png', className='profile-pic'),
        html.Div('Richard Villanueva', className='profile-name'),
        html.Div('richardkimv@deped.edu.ph', className='profile-email'),
        html.Div('ADMIN', className='profile-email admin'),
        html.Button(
            children=[
                html.I(className="fa fa-upload"), html.Span('Upload Data', className='hide-filter')
            ],
            className='profile-role-btn',
            id='open-upload-wrapper',
            n_clicks=0),
    ], className='profile-card'),
], className='sidebar-wrapper')

# Header
navbar1 = html.Div([
    html.Div("Enrollment Yearly Snapshot",id='dashboard-main-title', className='navbar-title'),
    html.Div([
        html.Div(id='filter-location-dropdown-id', children=[filter_location_dropdown]),
        dbc.Select(
            id='school-year-dropdown-select',
            value='2023-2024',
            options=[
                {'label': '2023-2024', 'value': '2023-2024'}
            ],
            className='school-year-dropdown-select',
        ),
        html.Div([
            upload_modal,
        ],id="upload-modal-background-drop", className="background-drop")
    ], className='filter-button-div-container'),
], className='header-div')

navbar2 = html.Div([
    html.Div([
        dcc.Tabs(
            children=[
                dcc.Tab(label='School-based', value='school-based', className='enrollment-tab', selected_className='enrollment-tab--selected'),
                dcc.Tab(label='Level-based', value='level-based', className='enrollment-tab', selected_className='enrollment-tab--selected'),
                dcc.Tab(label='Geographic-based', value='geographic-based', className='enrollment-tab', selected_className='enrollment-tab--selected'),
                dcc.Tab(label='Yearly Analysis', value='yearly_analysis', className='enrollment-tab', selected_className='enrollment-tab--selected'),
                dcc.Tab(label=None, value=None, style={'display':'None'}, className='enrollment-tab', selected_className='enrollment-tab--selected')
            ],
            id='tabs',
            value='school-based'
        )
    ],id='tabs-wrapper', className='tabs-wrapper'),
    html.Div([
        html.Button(
            children=[
                html.I(className="fa fa-filter"), html.Span('Filter', className='hide-filter')
            ],
            className='filter-button',
            id='toggle-button-open',
            n_clicks=0
        ),
    ], className='filter-button-div-container'),
],className='header-div')
# html.Div([
    #     html.I(className='fa fa-search'),
    #     dcc.Input(type="text", placeholder="Search...", className='search-bar'),
    # ], className='header-search-div'),
    # html.Div([
    #     html.I(className='fa fa-envelope'),
    #     html.I(className='fa fa-bell'),
    #     html.Span('I', className='header-divider'),
    #     html.Div([
    #         html.I(className='fa fa-user-circle profile-pic'),
    #         html.Div([
    #             html.Span('Jane Doe', className='username-text'),
    #             html.Span('Admin', className='access-level-text')], className='user-info'),
    #     ], className='header-profile-div'),
    #     html.I(className='fa fa-ellipsis-v')
    # ], className='header-icons-div')

app_temporary_storage=[
    dcc.Store(id="theme-store", data="light"),
    dcc.Store(id='selected-mode', data='student'),
    dcc.Store(id='stored-file'),
    dcc.Store(id='stored-year-range'),
    dcc.Store(id='current-files', storage_type='session'),
    dcc.Store(id='current-years', storage_type='session'),
    dcc.Store(id='folder-hash', data=''),
    dcc.Store(id='aggregated-years-df'),
    dcc.Store(id='current-year-df'),
    dcc.Store(id='previous-year-df'),
    dcc.Store(id='sy-labels', data=None),
    dcc.Store(id='latest-tab-change-id', data=0)
]

# Application Layout Initialization ------------------------------------------------------------------------------------------------

app.layout = html.Div([
    *app_temporary_storage,
    dcc.Interval(id='file-check', interval=3000, n_intervals=0),
    # dcc.Store(id='df-store', data=df.to_dict('records')),
    sidebar,
    html.Div([
        navbar1,
        navbar2,
        content_layout
    ], className='navbar-content-wrapper')
], className='main-page', id="main-container")







@app.callback(
    Output('tabs-wrapper', 'children'),
    Output('dashboard-main-title', 'children'),
    Input('selected-mode', 'data')
)
def render_tabs(mode):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]['prop_id']
        print("render_tabs triggered by:", prop_id) 
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
                dcc.Tab(label='Geographic-based', value='geographic-based', className='enrollment-tab', selected_className='enrollment-tab--selected'),
                dcc.Tab(label=None, value=None, style={'display':'None'}, className='enrollment-tab', selected_className='enrollment-tab--selected')
            ],
            id='tabs',
            value='school-based'
        ), "School Data"

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
    State('current-years', 'data')]        # current_years is the full list of years from dcc.Store
)
def populate_school_year_dropdown(year_range, current_years):
    if not year_range or not current_years:
        return []

    # Filter current_years to only include those within the selected range
    filtered_years = [y for y in current_years if year_range[0] <= y <= year_range[1]]
    filtered_years = sorted(set(y for y in filtered_years if isinstance(y, int)), reverse=True)

    # Build school year strings like "2015-2016"
    school_years = [f"{year}-{year + 1}" for year in filtered_years]

    # Construct dropdown options
    options = []
    options += [{'label': sy, 'value': sy} for sy in school_years]

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
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]['prop_id']
        print("toggle_upload_modal triggered by:", prop_id) 
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
     State('folder-hash', 'data')],
    prevent_initial_callback=True  # Input to detect changes in folder
)
def update_file_list(n, last_folder_hash):
    folder_path = Path('enrollment_database')
    filenames = [f.name for f in folder_path.iterdir() if f.is_file() and f.suffix == '.csv']
    
    # Calculate hash of the current folder contents (to detect changes)
    current_hash = hashlib.md5(''.join(filenames).encode('utf-8')).hexdigest()

    # If the folder hash is the same as the last stored hash, don't update
    if current_hash == last_folder_hash:
        return dash.no_update  # No change, return no_update
    
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]['prop_id']
        print("update_file_list triggered by:", prop_id) 
    # If the folder contents have changed, process the filenames
    years = []
    for f in filenames:
        name = f.replace('.csv', '')
        if name.isdigit():
            years.append(int(name))
    
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