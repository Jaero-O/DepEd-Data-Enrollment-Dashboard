import sys
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
from dashboard_page.district.district_page import districtPage
from dashboard_page.divisional.divisional_page import divisionalPage
from dashboard_page.regional.regional_page import regionalPage
from dashboard_page.national.national_page import nationalPage


# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

# Navigation Bar 
navBar = html.Div([
    html.Div([
        html.Img(src='/assets/images/deped_logo.png', className='depEd-logo'),
        html.Span('DepEd Learning Management System', className='title-page-text'),
    ],className='header-footer'),
    html.Div([
        html.Div([html.I(className="fa fa-area-chart hovered"), html.Span('My Dashboard', className='nav-bar-li hovered')], className='nav-bar-li-div-hovered'),
        html.Div([html.I(className="fa fa-home"), html.Span('Homepage', className='nav-bar-li')]),
        html.Div([html.I(className="fa fa-user"), html.Span('Account Profile', className='nav-bar-li')]),
        html.Div([html.I(className="fa fa-window-restore"), html.Span('Utilities', className='nav-bar-li')]),
        html.Div([html.I(className="fa fa-cog"), html.Span('Settings', className='nav-bar-li')]),
        html.Div([html.I(className="fa fa-sign-out log-out"), html.Span('Log Out', className='nav-bar-li log-out')]),
    ], className='nav-items'),
    html.Div([
        # html.Img(src='/assets/images/deped_title.png',className='depEd-title'),
        html.Span('All Rights Served 2025', className='title-page-text all-rights-served'),
    ],className='header-footer')
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
],className='header-div')

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
    html.Div(id="tab-content", className='content-page active-tab')
], className='tab-div')

# Application Layout Initialization
app.layout = html.Div([
    navBar,
    html.Div([
        header,
        content
    ])
],className='main-page')

# Callback to update content based on active tab
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def update_tab_content(selected_tab):
    if selected_tab == "National":
        return nationalPage()
    elif selected_tab == "Regional":
        return regionalPage()
    elif selected_tab == "Divisional":
        return divisionalPage()
    elif selected_tab == "District":
        return districtPage()
    return nationalPage


if __name__ == '__main__':
    app.run(debug=True)
