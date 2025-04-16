import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Import the function to create the gender card
from card_one import create_gender_card  # Replace with the actual filename where the function is defined

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout for the dashboard
app.layout = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(
                    label="Dashboard",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(create_gender_card(), width=4)  # Add the gender card to this tab
                            ]
                        )
                    ]
                ),
                dbc.Tab(
                    label="Other Tab",
                    children=[
                        html.Div("Content for another tab")
                    ]
                ),
            ]
        )
    ]
)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
