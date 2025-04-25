import json
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, Dash
from geojson_rewind import rewind

df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

def card_choropleth(df, mode='student', level='region'):
    if df is None or df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

    if level == 'region':
        geojson_path = r"main\data_engineer\frontend\assets\geojson\ph.json"
        with open(geojson_path, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
        featureidkey = "properties.name"

        region_mapping = {
            "Region I": "Ilocos", "Region II": "Cagayan Valley", "Region III": "Central Luzon",
            "Region IV-A": "Calabarzon", "Region V": "Bicol", "Region VI": "Western Visayas",
            "Region VII": "Central Visayas", "Region VIII": "Eastern Visayas", "Region IX": "Zamboanga Peninsula",
            "Region X": "Northern Mindanao", "Region XI": "Davao", "Region XII": "Soccsksargen",
            "CAR": "Cordillera Administrative Region", "CARAGA": "Caraga", "NCR": "National Capital Region",
            "MIMAROPA": "Mimaropa", "BARMM": "Autonomous Region in Muslim Mindanao", "PSO": None
        }

        df["geo_name"] = df["region"].map(region_mapping)
        df = df[df["geo_name"].notna()]

        if mode == 'school':
            df_count = df.groupby(['region']).size().reset_index(name='total')
            df_count["geo_name"] = df_count["region"].map(region_mapping)
            card_choropleth_title = 'Schools by Region'
        elif mode == 'student':
            grade_cols = [col for col in df.columns if '_male' in col or '_female' in col]
            df_count = df[['region'] + grade_cols]
            df_count['total'] = df_count[grade_cols].sum(axis=1)
            df_count = df_count.groupby(['region'])['total'].sum().reset_index()
            df_count["geo_name"] = df_count["region"].map(region_mapping)
            card_choropleth_title = 'Enrollment by Region'

    elif level == 'province':
        geojson_path = r"main\data_engineer\frontend\assets\geojson\combined-provincial-districts-updated.geojson"
        with open(geojson_path, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
        featureidkey = "properties.adm2_en"

        # Handle split of Maguindanao
        df_maguindanao = df[df['province'] == 'MAGUINDANAO'].copy()
        df_norte = df_maguindanao.copy()
        df_norte['province'] = 'MAGUINDANAO DEL NORTE'
        df_sur = df_maguindanao.copy()
        df_sur['province'] = 'MAGUINDANAO DEL SUR'
        df = df[df['province'] != 'MAGUINDANAO']
        df = pd.concat([df, df_norte, df_sur], ignore_index=True)

        province_mapping = {
            "ABRA": "Abra", "AGUSAN DEL NORTE": "Agusan del Norte", "AGUSAN DEL SUR": "Agusan del Sur",
            "AKLAN": "Aklan", "ALBAY": "Albay", "ANTIQUE": "Antique", "APAYAO": "Apayao",
            "AURORA": "Aurora", "BASILAN": "Basilan", "BATAAN": "Bataan", "BATANES": "Batanes",
            "BATANGAS": "Batangas", "BENGUET": "Benguet", "BILIRAN": "Biliran", "BOHOL": "Bohol",
            "BUKIDNON": "Bukidnon", "BULACAN": "Bulacan", "CAGAYAN": "Cagayan", "CAMARINES NORTE": "Camarines Norte",
            "CAMARINES SUR": "Camarines Sur", "CAMIGUIN": "Camiguin", "CAPIZ": "Capiz", "CATANDUANES": "Catanduanes",
            "CAVITE": "Cavite", "CEBU": "Cebu", "CITY OF COTABATO": "Cotabato City",
            "CITY OF ISABELA": "City of Isabela (Not a Province)", "COMPOSTELA VALLEY": "Davao de Oro",
            "DAVAO DEL NORTE": "Davao del Norte", "DAVAO DEL SUR": "Davao del Sur",
            "DAVAO OCCIDENTAL": "Davao Occidental", "DAVAO ORIENTAL": "Davao Oriental",
            "DINAGAT ISLANDS": "Dinagat Islands", "EASTERN SAMAR": "Eastern Samar", "GUIMARAS": "Guimaras",
            "IFUGAO": "Ifugao", "ILOCOS NORTE": "Ilocos Norte", "ILOCOS SUR": "Ilocos Sur", "ILOILO": "Iloilo",
            "ISABELA": "Isabela", "KALINGA": "Kalinga", "LA UNION": "La Union", "LAGUNA": "Laguna",
            "LANAO DEL NORTE": "Lanao del Norte", "LANAO DEL SUR": "Lanao del Sur", "LEYTE": "Leyte",
            "MAGUINDANAO DEL NORTE": "Maguindanao del Norte", "MAGUINDANAO DEL SUR": "Maguindanao del Sur",
            "MANILA, NCR,  FIRST DISTRICT": "NCR, City of Manila, First District (Not a Province)",
            "MARINDUQUE": "Marinduque", "MASBATE": "Masbate", "MISAMIS OCCIDENTAL": "Misamis Occidental",
            "MISAMIS ORIENTAL": "Misamis Oriental", "MOUNTAIN PROVINCE": "Mountain Province",
            "NCR   FOURTH DISTRICT": "NCR, Fourth District (Not a Province)", "NCR   SECOND DISTRICT": "NCR, Second District (Not a Province)",
            "NCR   THIRD DISTRICT": "NCR, Third District (Not a Province)", "NEGROS OCCIDENTAL": "Negros Occidental",
            "NEGROS ORIENTAL": "Negros Oriental", "NORTH COTABATO": "Cotabato", "NORTHERN SAMAR": "Northern Samar",
            "NUEVA ECIJA": "Nueva Ecija", "NUEVA VIZCAYA": "Nueva Vizcaya", "OCCIDENTAL MINDORO": "Occidental Mindoro",
            "ORIENTAL MINDORO": "Oriental Mindoro", "PALAWAN": "Palawan", "PAMPANGA": "Pampanga",
            "PANGASINAN": "Pangasinan", "QUEZON": "Quezon", "QUIRINO": "Quirino", "RIZAL": "Rizal",
            "ROMBLON": "Romblon", "SARANGANI": "Sarangani", "SIQUIJOR": "Siquijor", "SORSOGON": "Sorsogon",
            "SOUTH COTABATO": "South Cotabato", "SOUTHERN LEYTE": "Southern Leyte",
            "SULTAN KUDARAT": "Sultan Kudarat", "SULU": "Sulu", "SURIGAO DEL NORTE": "Surigao del Norte",
            "SURIGAO DEL SUR": "Surigao del Sur", "TARLAC": "Tarlac", "TAWI-TAWI": "Tawi-Tawi",
            "WESTERN SAMAR": "Samar", "ZAMBALES": "Zambales", "ZAMBOANGA DEL NORTE": "Zamboanga del Norte",
            "ZAMBOANGA DEL SUR": "Zamboanga del Sur", "ZAMBOANGA SIBUGAY": "Zamboanga Sibugay"
        }

        df["geo_name"] = df["province"].map(province_mapping)
        df = df[df["geo_name"].notna()]

        if mode == 'school':
            df_count = df.groupby(['province']).size().reset_index(name='total')
            df_count["geo_name"] = df_count["province"].map(province_mapping)
            card_choropleth_title = 'Schools by Province'
        elif mode == 'student':
            grade_cols = [col for col in df.columns if '_male' in col or '_female' in col]
            df_count = df[['province'] + grade_cols]
            df_count['total'] = df_count[grade_cols].sum(axis=1)
            df_count = df_count.groupby(['province'])['total'].sum().reset_index()
            df_count["geo_name"] = df_count["province"].map(province_mapping)
            card_choropleth_title = 'Enrollment by Province'

    geojson_data_rewind = rewind(geojson_data, rfc7946=False)

    fig = px.choropleth(
        df_count,
        geojson=geojson_data_rewind,
        featureidkey=featureidkey,
        locations="geo_name",
        color="total",
        color_continuous_scale=[
            "#000E19", "#001526", "#001C33", "#002440", "#002B4D", "#003259", "#003966",
            "#004073", "#004780", "#004E8C", "#005599", "#005CA6", "#0063B3", "#006BBF",
            "#0072CC", "#0079D9", "#0080E6", "#0087F2", "#0D94FF", "#1999FF", "#269FFF",
            "#33A5FF", "#40AAFF", "#4DB0FF", "#59B6FF", "#66BBFF", "#73C1FF", "#80C7FF",
            "#8CCCFF", "#99D2FF", "#A6D7FF", "#B3DDFF", "#BFE3FF", "#CCE8FF", "#D9EEFF",
            "#E6F4FF"
        ]

    )

    fig.update_traces(marker_line_color="black", marker_line_width=0)
    fig.update_geos(
        visible=False,
        projection_type="mercator",
        center={"lat": 12.8797, "lon": 121.7740},
        lonaxis=dict(range=[115, 128]),
        lataxis=dict(range=[4, 21]),
        bgcolor='rgba(0,0,0,0)'
    )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12, color="black"),
        coloraxis_colorbar=dict(
            orientation='h', yanchor='bottom', y=-0.1, xanchor='center',
            title=None, tickvals=[], x=0.5, len=0.70, thickness=18
        )
    )

    return dbc.Card(
        dbc.CardBody([
            html.Div(f"{card_choropleth_title}", style={
                "fontWeight": "bold", "fontFamily": "Inter", "fontSize": "16px", "color": "#2a4d69"
            }),
            html.Div([
                dcc.Graph(figure=fig, config={"displayModeBar": False}, style={"width": "100%", "height": "100%"})
            ], style={
                'marginTop': '0px', 'width': '100%', 'height': '95%',
                'overflow': 'hidden', 'fontFamily': 'Inter'
            }),
        ]),
        style={
            'background': 'linear-gradient(135deg, #9EFFF7, #ffffff)',  # updated line
            'borderRadius': '18px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'fontFamily': 'Inter',
            'padding': '5px',
            'width': '500px',
            'height': '700px'
        }
    )