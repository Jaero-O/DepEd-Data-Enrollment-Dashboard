import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
from card_one import card_one  # Import the card_one function

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load your dataset here
# Assuming you have a CSV or DataFrame `df`
# For this example, you might need to load your actual data in the following way:
df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

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
                                dbc.Col(card_one(df, mode='student', location='Region'), width=4)  # Use card_one here
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
