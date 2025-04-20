import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash import Input, Output, State, MATCH, ALL, ctx
import requests
import pandas as pd
import base64
import io

# Import pages
from main.data_engineer.frontend.dashboard.content_layout.content_layout import content_layout, content_layout_register_callbacks

# Import Cards Callbacks
# from main.data_engineer.frontend.dashboard.content.cards.card_filter import card_filter_register_callbacks
from main.data_engineer.frontend.dashboard.content.cards.card_six import card_six_register_callbacks

# Import Flask Server
from main.data_engineer.backend.main_server import app as server


# Initialize the Dash app
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True
)

# website favicon and title
app.title = "DepEd Learning Management System"
# app._favicon = ("images\deped_logo.ico")
app.config.suppress_callback_exceptions = True

# Navigation Bar 
sidebar = html.Div([
    html.Img(src='./assets/images/deped_title.png', className='depEd-title'),
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
        html.Button('Admin Account', className='profile-role-btn')
    ], className='profile-card'),
], className='sidebar-wrapper')

# Header
navbar = html.Div([
    html.Div("Enrollment Data", className='navbar-title'),
    html.Div(id='tabs-wrapper', className='tabs-wrapper'),
    html.Div([
        html.Button(
            children=[
                html.I(className="fa fa-filter"), html.Span('Filter', className='hide-filter', id='filter-button-text')
            ],
            className='filter-button',
            id='toggle-button-open',
            n_clicks=0)
    ], className='filter-button-div-container'),
], className='header-div')

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

# Application Layout Initialization ------------------------------------------------------------------------------------------------

app.layout = html.Div([
    dcc.Store(id="theme-store", data="light"),
    dcc.Store(id='selected-mode', storage_type='session', data='student'),
    # dcc.Store(id='df-store', data=df.to_dict('records')),
    sidebar,
    html.Div([
        navbar,
        content_layout
    ], className='navbar-content-wrapper')
], className='main-page', id="main-container")

@app.callback(
    Output('tabs-wrapper', 'children'),
    Input('selected-mode', 'data')
)
def render_tabs(mode):
    if mode == 'student':
        return dcc.Tabs(
            children=[
                dcc.Tab(label='School-based', value='school-based', className='enrollment-tab', selected_className='enrollment-tab--selected'),
                dcc.Tab(label='Level-based', value='level-based', className='enrollment-tab', selected_className='enrollment-tab--selected'),
                dcc.Tab(label='Geographic-based', value='geographic-based', className='enrollment-tab', selected_className='enrollment-tab--selected')
            ],
            id='tabs',
            value='school-based'
        )
    elif mode == 'school':
        return dcc.Tabs(
            children=[
                dcc.Tab(label='School-based', value='school-based', className='enrollment-tab', selected_className='enrollment-tab--selected'),
                dcc.Tab(label='Geographic-based', value='geographic-based', className='enrollment-tab', selected_className='enrollment-tab--selected')
            ],
            id='tabs',
            value='school-based'
        )
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


@app.callback(
    Output("output-data-upload", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename")]
)
def upload_file(contents, filename):
    if contents is None:
        return "No file uploaded"
    
    if not allowed_file(filename):
        return html.Div([html.H5("Invalid file type. Please upload a CSV or Excel file.")])
    
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    # if "csv" not in content_type and "excel" not in content_type:
    #     return html.Div([html.H5("Invalid file format. Only CSV or Excel files are allowed.")])
    
    files = {
        'file': (filename, io.BytesIO(decoded), 'application/octet-stream')
    }
    
    try:
        response = requests.post('http://127.0.0.1:5000/api/upload-file', files=files)
        if response.status_code == 200:
            return html.Div([html.H5(response.json().get('message'))])
        else:
            return html.Div([html.H5(f"Upload failed with status {response.status_code}")])
    except requests.exceptions.RequestException as e:
        return html.Div([html.H5(f"Error occurred: {str(e)}")])
    


content_layout_register_callbacks(app)