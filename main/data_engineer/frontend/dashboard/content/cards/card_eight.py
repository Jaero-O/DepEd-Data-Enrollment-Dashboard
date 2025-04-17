import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
import dash_bootstrap_components as dbc

def card_eight(df, location, mode):
    if df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

    if mode not in ['student', 'school']:
        raise ValueError("Mode must be either 'student' or 'school'")

    # Filter by location if applicable
    if location != 'overall' and location in df.columns:
        df = df[df[location].notna()]

    # Define strand mappings
    strand_columns = {
        'ABM': {
            'male': ['g11_acad_-_abm_male', 'g12_acad_-_abm_male'],
            'female': ['g11_acad_-_abm_female', 'g12_acad_-_abm_female']
        },
        'HUMSS': {
            'male': ['g11_acad_-_humss_male', 'g12_acad_-_humss_male'],
            'female': ['g11_acad_-_humss_female', 'g12_acad_-_humss_female']
        },
        'STEM': {
            'male': ['g11_acad_stem_male', 'g12_acad_stem_male'],
            'female': ['g11_acad_stem_female', 'g12_acad_stem_female']
        },
        'GAS': {
            'male': ['g11_acad_gas_male', 'g12_acad_gas_male'],
            'female': ['g11_acad_gas_female', 'g12_acad_gas_female']
        },
        'PBM': {
            'male': ['g11_acad_pbm_male', 'g12_acad_pbm_male'],
            'female': ['g11_acad_pbm_female', 'g12_acad_pbm_female']
        },
        'TVL': {
            'male': ['g11_tvl_male', 'g12_tvl_male'],
            'female': ['g11_tvl_female', 'g12_tvl_female']
        },
        'Sports': {
            'male': ['g11_sports_male', 'g12_sports_male'],
            'female': ['g11_sports_female', 'g12_sports_female']
        },
        'Arts': {
            'male': ['g11_arts_male', 'g12_arts_male'],
            'female': ['g11_arts_female', 'g12_arts_female']
        }
    }

    # Aggregate male and female totals per strand
    strand_data = {
        'Strand': [],
        'Male': [],
        'Female': []
    }

    for strand, genders in strand_columns.items():
        male_cols = [col for col in genders['male'] if col in df.columns]
        female_cols = [col for col in genders['female'] if col in df.columns]

        strand_data['Strand'].append(strand)
        strand_data['Male'].append(df[male_cols].sum().sum())
        strand_data['Female'].append(df[female_cols].sum().sum())

    # Create DataFrame
    strand_df = pd.DataFrame(strand_data).sort_values(by=['Male', 'Female'], ascending=False)

    # Create stacked area chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=strand_df['Strand'],
        y=strand_df['Male'],
        name='Male',
        fill='tozeroy',
        mode='lines+markers',
        line=dict(color='blue'),
        marker=dict(size=6)
    ))

    fig.add_trace(go.Scatter(
        x=strand_df['Strand'],
        y=strand_df['Female'],
        name='Female',
        fill='tonexty',  # Stack on top of Male
        mode='lines+markers',
        line=dict(color='orange'),
        marker=dict(size=6)
    ))

    fig.update_layout(
    title=dict(
        text="SENIOR HIGH SCHOOL STRAND<br><sup>ENROLLED STUDENTS<sup>",
        x=0.05,
        font=dict(size=20, color='darkblue')
    ),
    margin=dict(l=40, r=20, t=60, b=60),
    height=450,
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(orientation='h', x=0.5, xanchor='center', y=-0.2),
    
    # Remove axis numbers
    xaxis=dict(showticklabels=True),  # Hide x-axis numbers
    yaxis=dict(showticklabels=False)   # Hide y-axis numbers
)


    # Return as dbc.Card
    return dbc.Card(
        dbc.CardBody([
            dcc.Graph(figure=fig, config={'displayModeBar': False})
        ]),
        className="card-eight-container"
    )




