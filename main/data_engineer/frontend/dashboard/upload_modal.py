import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash import Input, Output, State, MATCH, ALL, ctx
import requests
import base64
import io

upload_modal = html.Div([
    html.Div('School Enrollment Upload Data', className='header'),
    html.Div([
        html.Div([
            html.Div('File Upload:', className='upload-subtext'),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select File')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px 0'
                },
                multiple=False
            ),
            html.Div(id='uploaded-filename-display', className='uploaded-filename-display')
        ], className='upload-wrapper-file'),
        html.Div([
            html.Div('School Year: ', className='school-year--dropdown-subtext'),
            dcc.Dropdown(
                id='school-year-dropdown',
                options=[
                    {'label': f'{year}-{year + 1}', 'value': f'{year}-{year + 1}'}
                    for year in range(1980, 2026)
                ],
                placeholder='Select School Year',
                style={'width': '300px'},
                className='school-year-dropdown'
            ),
        ], className='school-year-dropdown-wrapper'),
    ],className='body'),
    html.Div([
        html.Button("Upload", id="upload-button", n_clicks=0),
        html.Button("Cancel", id="close-upload-wrapper", n_clicks=0)
    ],className='footer')
], id="upload-modal-wrapper", className='upload-wrapper')

ALLOWED_EXTENSIONS = ['.csv', '.xlsx']

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)

def upload_modal_register_callbacks(app):
    @app.callback(
        Output('stored-file', 'data'),
        Output('uploaded-filename-display', 'children'),  # ✅ show filename
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
    )
    def store_uploaded_file(contents, filename):
        if contents and filename:
            display_name = html.Div(f"Uploaded file: {filename}", style={"marginTop": "10px"})
            return {'contents': contents, 'filename': filename}, display_name
        return None, ""

    @app.callback(
        Output("output-data-upload", "children"),
        Input("upload-button", "n_clicks"),
        State("stored-file", "data"),
        State("school-year-dropdown", "value"),  # ✅ get selected year
        prevent_initial_call=True
    )
    def upload_file(n_clicks, file_data, selected_year):
        if not file_data:
            return html.Div([html.H5("No file selected")])

        contents = file_data['contents']
        original_filename = file_data['filename']

        if not allowed_file(original_filename):
            return html.Div([html.H5("Invalid file type. Please upload a CSV or Excel file.")])

        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        # ✅ Rename file using the first part of the selected school year
        if selected_year:
            year_start = selected_year.split('-')[0]
            extension = '.' + original_filename.split('.')[-1]
            final_filename = f"{year_start}{extension}"
        else:
            final_filename = original_filename

        files = {
            'file': (final_filename, io.BytesIO(decoded), 'application/octet-stream')
        }

        try:
            response = requests.post('http://127.0.0.1:5000/api/upload-file', files=files)
            if response.status_code == 200:
                return html.Div([html.H5(response.json().get('message'))])
            else:
                return html.Div([html.H5(f"Upload failed with status {response.status_code}")])
        except requests.exceptions.RequestException as e:
            return html.Div([html.H5(f"Error occurred: {str(e)}")])
