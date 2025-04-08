import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
import requests
import pandas as pd
import base64
import io

# Import pages
from main.data_engineer.frontend.dashboard.baranggay.baranggay_page import baranggayPage
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
    html.Div([
        html.I(className='fa fa-search'),
        dcc.Input(type="text", placeholder="Search...", className='search-bar'),
    ], className='header-search-div'),
    html.Div([
        html.I(className='fa fa-envelope'),
        html.I(className='fa fa-bell'),
        html.Span('I', className='header-divider'),
        html.Div([
            html.I(className='fa fa-user-circle profile-pic'),
            html.Div([
                html.Span('Jane Doe', className='username-text'),
                html.Span('Admin', className='access-level-text')], className='user-info'),
        ], className='header-profile-div'),
        html.I(className='fa fa-ellipsis-v')
    ], className='header-icons-div')
], className='header-div')

# Content Part ----------------------------------------------------------------------------------------------------------------

labels = ['Region', 'Province', 'Division', 'District', 'Barangay']
tab_labels = ["National", "Regional", "Divisional", "District", "Baranggay"]
options = ["Option 1", "Option 2", "Option 3"]

content = html.Div([
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
    html.Div([  # Wrapper div for filters and dropdown
        html.Span('Filtering Menu', className='filter-menu-title'),
        html.Div([
            html.Span("Select range of school year:", className='label-text'),
                dcc.RangeSlider(
                id='year-range-slider',
                min=2000,
                max=2025,
                step=1,
                marks={str(year): str(year) for year in range(2000, 2026)},
                value=[2000, 2025],  # Default range (min: 2000, max: 2025)
                tooltip={"placement": "bottom", "always_visible": True}
            ),
        ], className='slider-filtering-div'),
        html.Div([  # Wrapper div for dropdown menus
            html.Div([
                html.Div([  # For each label, create a dropdown
                    html.Span(label, className='label-text'),  # Display each label
                    dbc.DropdownMenu(
                        label="Select Options",  # Default label text
                        children=[
                            dbc.Checklist(
                                id={'type': 'chk', 'index': label},
                                options=[{'label': opt, 'value': opt} for opt in options],
                                value=[],  # Default value (empty list means no selection)
                                inline=True,
                                className='checklist-menu'
                            )
                        ],
                        className="dropdown-menu-class",
                        toggle_class_name='dropdown-menu-button',
                        direction="down",
                        size="sm"
                    )
                ], className='dropdown-filtering-div2') for label in labels  # Loop through labels
            ], className='dropdown-filtering-div1'),
            html.Div([
                html.Label('School Finder Search Bar'),
                dcc.Input(type="text", placeholder="Search...", className='search-bar')
            ],className='search-filtering-div')
        ], className='dropdown-search-filtering-div')
    ],className='filtering-div open', id='filter-container'),

    # Tabs for navigation
    dcc.Tabs(
        id="tabs",
        value="National",
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
    
    # Content area for tab display
    html.Div(id="tab-content", className='content-page active-tab'),
    html.Div(id="output-data-upload")
], className='tab-div')


# Application Layout Initialization ------------------------------------------------------------------------------------------------

app.layout = html.Div([
    dcc.Store(id="theme-store", data="light"),
    navBar,
    html.Div([
        header,
        content
    ])
], className='main-page', id="main-container")



# Callback to update content based on active tab ------------------------------------------------------------------------------------------------

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
    elif selected_tab == "Baranggay":
        return baranggayPage()
    return nationalPage()



# Callback for changing the theme of the page ------------------------------------------------------------------------------------------------

@app.callback(
    Output("main-container", "className"),
    Output("theme-store", "data"),
    Input("theme-toggle-switch", "value")
)
def toggle_theme(is_dark_mode):
    new_theme = "main-page dark-mode" if is_dark_mode else "main-page"
    return new_theme, new_theme


# Callback for Showing/hiding filters

@app.callback(
    [Output('filter-container', 'className'),
     Output('filter-button-text', 'children')],
    Input('toggle-button', 'n_clicks'),
    prevent_initial_call=True
)
def toggle_filters(n_clicks):
    if n_clicks % 2 == 1:
        return 'filtering-div close', "Show Filters"
    elif n_clicks % 2 == 0:
        return 'filtering-div open', "Hide Filters"
    else:
        return 'filtering-div close', "Show Filters"



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