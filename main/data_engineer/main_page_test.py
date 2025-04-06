import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Sidebar layout
sidebar = html.Div(
    [
        html.Img(src='https://upload.wikimedia.org/wikipedia/en/thumb/9/9b/Department_of_Education_%28DepEd%29.png/200px-Department_of_Education_%28DepEd%29.png',
                 style={'width': '80%', 'margin': '20px'}),
        html.H4("DepEd Learning Management System", style={'textAlign': 'center', 'color': 'white'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("My Dashboard", href="#", active=True),
                dbc.NavLink("Homepage", href="#"),
                dbc.NavLink("Account Profile", href="#"),
                dbc.NavLink("Account Performance", href="#"),
                dbc.NavLink("Settings", href="#"),
                dbc.NavLink("Log Out", href="#", style={'color': 'red'}),
            ],
            vertical=True,
            pills=True,
        ),
        html.Footer("DepED - All Rights Reserved 2025", style={'textAlign': 'center', 'color': 'white', 'marginTop': '20px'})
    ],
    style={
        "position": "fixed", "width": "250px", "height": "100vh", "backgroundColor": "#1E2A38", "padding": "20px"
    }
)

# Main content layout
tabs = dbc.Tabs([
    dbc.Tab(label="National", tab_id="national"),
    dbc.Tab(label="Regional", tab_id="regional"),
    dbc.Tab(label="Provincial", tab_id="provincial"),
    dbc.Tab(label="District", tab_id="district"),
], id="tabs", active_tab="national", style={'marginBottom': '20px'})

content = html.Div(
    [
        html.H2("Hello, Jaerorette", style={'color': 'white'}),
        html.P("You've been gone away for 20 days.", style={'color': 'white'}),
        dcc.Input(type="text", placeholder="Search...", style={'marginBottom': '20px', 'width': '50%'}),
        tabs,
        dbc.Row([
            dbc.Col(html.Div(style={"height": "150px", "backgroundColor": "gray"}), width=3),
            dbc.Col(html.Div(style={"height": "150px", "backgroundColor": "gray"}), width=3),
            dbc.Col(html.Div(style={"height": "300px", "backgroundColor": "gray"}), width=6)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(html.Div(style={"height": "400px", "backgroundColor": "gray"}), width=12)
        ])
    ],
    style={"marginLeft": "270px", "padding": "20px", "backgroundColor": "#0B1622", "height": "100vh"}
)

# tabs = html.Div([
#     # Tabs Component
#     dcc.Tabs(
#         id="tabs",
#         value="National",  # Default active tab
#         children=[
#             dcc.Tab(label="National", value="National"),
#             dcc.Tab(label="Regional", value="Regional"),
#             dcc.Tab(label="Provincial", value="Provincial"),
#             dcc.Tab(label="District", value="District"),
#         ],
#         colors={"border": "#081434", "primary": "white", "background": "#1d2845"},
#     ),
    
#     # Div to display tab content
#     html.Div(id="tab-content", style={"margin-top": "20px", "color": "white"})
# ])

# # Callback to update content based on active tab
# @app.callback(
#     Output("tab-content", "children"),
#     Input("tabs", "value")
# )
# def update_tab_content(selected_tab):
#     if selected_tab == "National":
#         return html.P("Displaying National Data...")
#     elif selected_tab == "Regional":
#         return html.P("Displaying Regional Data...")
#     elif selected_tab == "Provincial":
#         return html.P("Displaying Provincial Data...")
#     elif selected_tab == "District":
#         return html.P("Displaying District Data...")
#     return html.P("Please select a tab.")

# App layout
app.layout = html.Div([sidebar, content])

# Run the app
if __name__ == "__main__":
    app.run(debug=False, threaded=True, processes=1)
