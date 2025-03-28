import dash
from dash import html, dcc
from dash.dependencies import Input, Output

app = dash.Dash()

app.layout = html.Div([
    html.Div(
        html.H1('My Dashboard')
    ),
    dcc.Tabs(id='tabs', value='Tab1', children=[
        dcc.Tab(label='Tab 1', id='tab1', value='Tab1', children =[
        ]),
        dcc.Tab(label='Tab 2', id='tab2', value='Tab2', children=[
        ])
    ])
])

@app.callback(Output('tab1', 'children'),
              [Input('tabs', 'value')])
def update_tabs(value):
    if value == 'Tab1':
        return dcc.Tabs(id="subtabs1", value='Subtab1', children=[
            dcc.Tab(label='Subtab 1', id='subtab1', value='Subtab1'),
            dcc.Tab(label='Subtab 2', id='subtab2', value='Subtab2'),
        ]),

@app.callback(Output('tab2', 'children'),
              [Input('tabs', 'value')])
def update_tabs(value):
    if value == 'Tab2':
        return dcc.Tabs(id="subtabs2", value='Subtab4', children=[
            dcc.Tab(label='Subtab 4', id='subtab4', value='Subtab4'),
            dcc.Tab(label='Subtab 5', id='subtab5', value='Subtab5')
        ]),

if __name__ == '__main__':
    app.run(debug=True)