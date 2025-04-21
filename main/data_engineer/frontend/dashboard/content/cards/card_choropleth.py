import json
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, Dash
from geojson_rewind import rewind



df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

def card_choropleth(df, mode='student'):
    if df is None or df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

    geojson_path = r"main\data_engineer\frontend\assets\geojson\ph.json"
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)
        geojson_data_rewind=rewind(geojson_data,rfc7946=False)


    region_mapping = {
        "Region I": "Ilocos",
        "Region II": "Cagayan Valley",
        "Region III": "Central Luzon",
        "Region IV-A": "Calabarzon",
        "Region V": "Bicol",
        "Region VI": "Western Visayas",
        "Region VII": "Central Visayas",
        "Region VIII": "Eastern Visayas",
        "Region IX": "Zamboanga Peninsula",
        "Region X": "Northern Mindanao",
        "Region XI": "Davao",
        "Region XII": "Soccsksargen",
        "CAR": "Cordillera Administrative Region",
        "CARAGA": "Caraga",
        "NCR": "National Capital Region",
        "MIMAROPA": "Mimaropa",
        "BARMM": "Autonomous Region in Muslim Mindanao",
        "PSO": None 
    }

    df["region_geo"] = df["region"].map(region_mapping)
    df = df[df["region_geo"].notna()]  

    if mode == 'school':
        df_count = df.groupby(['region']).size().reset_index(name='total')
        df_count['region_geo'] = df_count['region'].map(region_mapping)
    elif mode == 'student':
        grade_cols = [col for col in df.columns if '_male' in col or '_female' in col]
        print(grade_cols)
        df_count = df[['region'] + grade_cols]
        df_count['total'] = df_count[grade_cols].sum(axis=1)
        df_count = df_count.groupby(['region'])['total'].sum().reset_index()
        df_count['region_geo'] = df_count['region'].map(region_mapping)
        

    print(df_count.head())

    fig = px.choropleth(
        df_count,
        geojson=geojson_data_rewind,
        featureidkey="properties.name",
        locations="region_geo",
        color="total",
        color_continuous_scale=[
            "#74ff29",
            "#6aec24",
            "#61da1f",
            "#57c71a",
            "#4eb515",
            "#45a410",
            "#3c930a",
            "#338206",
            "#2a7102",
            "#226100"
        ]



,
        title="Enrollment by Region"
    )

    fig.update_traces(marker_line_color="black", marker_line_width=0.8)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12, color="black"),
    )

    return dbc.Card(
        dbc.CardBody([
            html.Div("CHOROPLETH", style={
                "fontWeight": "bold",
                "fontFamily": "Inter",
                "fontSize": "16px",
                "color": "#2a4d69"
            }),
            html.Div([
                dcc.Graph(figure=fig, config={"displayModeBar": False})
            ], style={
                'marginTop': '10px',
                'width': '1000px',
                'height': '500px',
                'overflow': 'hidden',
                'fontFamily': 'Inter'
            }),
        ]),
        style={
            'backgroundColor': '#f7f9f7',
            'borderRadius': '18px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'fontFamily': 'Inter',
            'padding': '10px',
        }
    )

def card_choropleth_region(df, mode='student'):
    if df is None or df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

    geojson_path = r"main\data_engineer\frontend\assets\geojson\combined-provincial-districts-updated.geojson"
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)
        geojson_data_rewind=rewind(geojson_data,rfc7946=False)

    df_maguindanao = df[df['province'] == 'MAGUINDANAO'].copy()

    df_norte = df_maguindanao.copy()
    df_norte['province'] = 'MAGUINDANAO DEL NORTE'

    df_sur = df_maguindanao.copy()
    df_sur['province'] = 'MAGUINDANAO DEL SUR'

    df = df[df['province'] != 'MAGUINDANAO']
    df = pd.concat([df, df_norte, df_sur], ignore_index=True)

    province_mapping = {
        "ABRA": "Abra",
        "AGUSAN DEL NORTE": "Agusan del Norte",
        "AGUSAN DEL SUR": "Agusan del Sur",
        "AKLAN": "Aklan",
        "ALBAY": "Albay",
        "ANTIQUE": "Antique",
        "APAYAO": "Apayao",
        "AURORA": "Aurora",
        "BASILAN": "Basilan",
        "BATAAN": "Bataan",
        "BATANES": "Batanes",
        "BATANGAS": "Batangas",
        "BENGUET": "Benguet",
        "BILIRAN": "Biliran",
        "BOHOL": "Bohol",
        "BUKIDNON": "Bukidnon",
        "BULACAN": "Bulacan",
        "CAGAYAN": "Cagayan",
        "CAMARINES NORTE": "Camarines Norte",
        "CAMARINES SUR": "Camarines Sur",
        "CAMIGUIN": "Camiguin",
        "CAPIZ": "Capiz",
        "CATANDUANES": "Catanduanes",
        "CAVITE": "Cavite",
        "CEBU": "Cebu",
        "CITY OF COTABATO": "Cotabato City",
        "CITY OF ISABELA": "City of Isabela (Not a Province)",
        "COMPOSTELA VALLEY": "Davao de Oro", 
        "DAVAO DEL NORTE": "Davao del Norte",
        "DAVAO DEL SUR": "Davao del Sur",
        "DAVAO OCCIDENTAL": "Davao Occidental",
        "DAVAO ORIENTAL": "Davao Oriental",
        "DINAGAT ISLANDS": "Dinagat Islands",
        "EASTERN SAMAR": "Eastern Samar",
        "GUIMARAS": "Guimaras",
        "IFUGAO": "Ifugao",
        "ILOCOS NORTE": "Ilocos Norte",
        "ILOCOS SUR": "Ilocos Sur",
        "ILOILO": "Iloilo",
        "ISABELA": "Isabela",
        "KALINGA": "Kalinga",
        "LA UNION": "La Union",
        "LAGUNA": "Laguna",
        "LANAO DEL NORTE": "Lanao del Norte",
        "LANAO DEL SUR": "Lanao del Sur",
        "LEYTE": "Leyte",
        "MAGUINDANAO": "Maguindanao",
        "MAGUINDANAO DEL NORTE": "Maguindanao del Norte",
        "MAGUINDANAO DEL SUR": "Maguindanao del Sur",
        "MANILA, NCR,  FIRST DISTRICT": "NCR, City of Manila, First District (Not a Province)",
        "MARINDUQUE": "Marinduque",
        "MASBATE": "Masbate",
        "MISAMIS OCCIDENTAL": "Misamis Occidental",
        "MISAMIS ORIENTAL": "Misamis Oriental",
        "MOUNTAIN PROVINCE": "Mountain Province",
        "NCR   FOURTH DISTRICT": "NCR, Fourth District (Not a Province)",
        "NCR   SECOND DISTRICT": "NCR, Second District (Not a Province)",
        "NCR   THIRD DISTRICT": "NCR, Third District (Not a Province)",
        "NEGROS OCCIDENTAL": "Negros Occidental",
        "NEGROS ORIENTAL": "Negros Oriental",
        "NORTH COTABATO": "Cotabato",
        "NORTHERN SAMAR": "Northern Samar",
        "NUEVA ECIJA": "Nueva Ecija",
        "NUEVA VIZCAYA": "Nueva Vizcaya",
        "OCCIDENTAL MINDORO": "Occidental Mindoro",
        "ORIENTAL MINDORO": "Oriental Mindoro",
        "Others": "Others",
        "PALAWAN": "Palawan",
        "PAMPANGA": "Pampanga",
        "PANGASINAN": "Pangasinan",
        "QUEZON": "Quezon",
        "QUIRINO": "Quirino",
        "RIZAL": "Rizal",
        "ROMBLON": "Romblon",
        "SARANGANI": "Sarangani",
        "SIQUIJOR": "Siquijor",
        "SORSOGON": "Sorsogon",
        "SOUTH COTABATO": "South Cotabato",
        "SOUTHERN LEYTE": "Southern Leyte",
        "SULTAN KUDARAT": "Sultan Kudarat",
        "SULU": "Sulu",
        "SURIGAO DEL NORTE": "Surigao del Norte",
        "SURIGAO DEL SUR": "Surigao del Sur",
        "TARLAC": "Tarlac",
        "TAWI-TAWI": "Tawi-Tawi",
        "WESTERN SAMAR": "Samar",
        "ZAMBALES": "Zambales",
        "ZAMBOANGA DEL NORTE": "Zamboanga del Norte",
        "ZAMBOANGA DEL SUR": "Zamboanga del Sur",
        "ZAMBOANGA SIBUGAY": "Zamboanga Sibugay"
    }

    df["province_geo"] = df["province"].map(province_mapping)
    print("Province Geo in DF:", sorted(df["province"].unique()))
    df = df[df["province_geo"].notna()]

    if mode == 'school':
        df_count = df.groupby(['province']).size().reset_index(name='total')
        df_count["province_geo"] = df_count["province"].map(province_mapping)
    elif mode == 'student':
        grade_cols = [col for col in df.columns if '_male' in col or '_female' in col]
        print(grade_cols)
        df_count = df[['province'] + grade_cols]
        df_count['total'] = df_count[grade_cols].sum(axis=1)
        df_count = df_count.groupby(['province'])['total'].sum().reset_index()
        df_count["province_geo"] = df_count["province"].map(province_mapping)
        

    print(df_count.head())

    fig = px.choropleth(
        df_count,
        geojson=geojson_data_rewind,
        featureidkey="properties.adm2_en",
        locations="province_geo",
        color="total",
        color_continuous_scale=[
            "#74ff29",
            "#6aec24",
            "#61da1f",
            "#57c71a",
            "#4eb515",
            "#45a410",
            "#3c930a",
            "#338206",
            "#2a7102",
            "#226100"
        ],
        title="Enrollment by Region"
    )

    fig.update_traces(marker_line_color="black", marker_line_width=0.8)
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12, color="black"),
    )

    print("Sample GeoJSON properties:", geojson_data["features"][0]["properties"].keys())

    for i, feature in enumerate(geojson_data["features"][:]):
        print(f"Feature {i} adm2_en:", feature["properties"].get("adm2_en"))

    print("Province Geo in DF:", sorted(df_count["province_geo"].unique()))
    
    return dbc.Card(
        dbc.CardBody([
            html.Div("CHOROPLETH", style={
                "fontWeight": "bold",
                "fontFamily": "Inter",
                "fontSize": "16px",
                "color": "#2a4d69"
            }),
            html.Div([
                dcc.Graph(figure=fig, config={"displayModeBar": False})
            ], style={
                'marginTop': '10px',
                'width': '1000px',
                'height': '500px',
                'overflow': 'hidden',
                'fontFamily': 'Inter'
            }),
        ]),
        style={
            'backgroundColor': '#f7f9f7',
            'borderRadius': '18px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'fontFamily': 'Inter',
            'padding': '10px',
        }
    )


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    card_choropleth(df, 'school'),
    card_choropleth(df, 'student'),
    card_choropleth_region(df, 'school'),
    card_choropleth_region(df, 'student'),
])

if __name__ == '__main__':
    app.run(debug=True)