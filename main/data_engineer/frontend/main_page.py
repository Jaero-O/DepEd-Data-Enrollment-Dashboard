import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
import requests
import pandas as pd
import base64
import io

# Import pages
from main.data_engineer.frontend.dashboard.district.district_page import districtPage
from main.data_engineer.frontend.dashboard.divisional.divisional_page import divisionalPage
from main.data_engineer.frontend.dashboard.regional.regional_page import regionalPage
from main.data_engineer.frontend.dashboard.national.national_page import nationalPage

# Import Flask Server
from main.data_engineer.backend.main_server import app as server

# Initialize the Dash app
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True
)

# Navigation Bar 
navBar = html.Div([
    html.Div([
        html.Img(src='./assets/images/deped_logo.png', className='depEd-logo'),
        html.Span('DepEd Learning Management System', className='title-page-text'),
    ], className='header-footer'),
    html.Div([
        html.Div([html.I(className="fa fa-area-chart hovered"), html.Span('My Dashboard', className='nav-bar-li hovered')], className='nav-bar-li-div-hovered'),
        html.Div([html.I(className="fa fa-home"), html.Span('Homepage', className='nav-bar-li')]),
        html.Div([html.I(className="fa fa-user"), html.Span('Account Profile', className='nav-bar-li')]),
        html.Div([html.I(className="fa fa-window-restore"), html.Span('Utilities', className='nav-bar-li')]),
        html.Div([html.I(className="fa fa-cog"), html.Span('Settings', className='nav-bar-li')]),
        html.Div([html.I(className="fa fa-sign-out log-out"), html.Span('Log Out', className='nav-bar-li log-out')]),
    ], className='nav-items'),
    html.Div([
        html.Div(dbc.Switch(id="theme-toggle-switch", label=None, value=False, className="toggle-switch-theme"), className="theme-toggle-container"),
        html.Span('All Rights Served 2025', className='title-page-text all-rights-served'),
    ], className='header-footer')
], className='nav-bar-div')

# Header
header = html.Div([
    html.Span('My Dashboard', className='My-Dashboard-title'),
    html.Div([
        dcc.Input(type="text", placeholder="Search...", className='search-bar'),
        html.I(className='fa fa-envelope'),
        html.I(className='fa fa-bell'),
        html.Div([html.I(className='fa fa-user-circle'), html.Span('Jane Doe')], className='header-username-div')
    ], className='header-icons-div')
], className='header-div')

# Content 
content = html.Div([
    dcc.Tabs(
        id="tabs",
        value="National",
        children=[
            dcc.Tab(label="National", value="National", className='tab', selected_className='tab-selected'),
            dcc.Tab(label="Regional", value="Regional", className='tab', selected_className='tab-selected'),
            dcc.Tab(label="Divisional", value="Divisional", className='tab', selected_className='tab-selected'),
            dcc.Tab(label="District", value="District", className='tab', selected_className='tab-selected'),
        ],
        className='tabs-dcc',
    ),
    html.Div(id="tab-content", className='content-page active-tab'),
    dcc.Upload(
        id="upload-data",
        children=html.Button("Upload File"),
        multiple=False,
    ),
    html.Div(id="output-data-upload")
], className='tab-div')

# Application Layout Initialization
app.layout = html.Div([
    dcc.Store(id="theme-store", data="light"),
    navBar,
    html.Div([
        header,
        content
    ])
], className='main-page', id="main-container")

# Callback to update content based on active tab
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def update_tab_content(selected_tab):
    if selected_tab == "National":
        response = requests.get("http://127.0.0.1:5000/api/uploaded-files")
        files = response.json()
        print(files)
        return nationalPage()
    elif selected_tab == "Regional":
        return regionalPage()
    elif selected_tab == "Divisional":
        return divisionalPage()
    elif selected_tab == "District":
        return districtPage()
    return nationalPage()

# Callback for changing the theme of the page
@app.callback(
    Output("main-container", "className"),
    Output("theme-store", "data"),
    Input("theme-toggle-switch", "value")
)
def toggle_theme(is_dark_mode):
    new_theme = "main-page dark-mode" if is_dark_mode else "main-page"
    return new_theme, new_theme

# Callback for uploading the file into the server
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

# if __name__ == '__main__':
#     app.run(debug=True, host="127.0.0.1", port=5000)
