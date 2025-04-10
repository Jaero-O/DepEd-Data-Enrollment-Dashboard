import pandas as pd
import plotly.express as px

def plot_gender_distribution(cleaned_file, filters=None):
    df = pd.read_csv(cleaned_file)
    df.columns = df.columns.str.strip()

    if filters:
        # Iterate over the filters dictionary to apply multiple filters
        for filter_column, filter_values in filters.items():
            if filter_column in df.columns:
                df = df[df[filter_column].isin(filter_values)]
            else:
                raise ValueError(f"Column '{filter_column}' not found in the dataset")

    male_columns = [col for col in df.columns if 'Male' in col]
    female_columns = [col for col in df.columns if 'Female' in col]

    gender_distribution = pd.DataFrame({
        'Gender': ['Male', 'Female'],
        'Enrollment Count': [
            df[male_columns].sum().sum(),
            df[female_columns].sum().sum()
        ]
    })

    fig = px.bar(
        gender_distribution,
        x='Gender',
        y='Enrollment Count',
        color='Gender',
        title="Gender Distribution of Student Enrollees"
    )
    fig.update_layout(
        barmode='stack',
        xaxis_title="Gender",
        yaxis_title="Enrollment Count",
        title_font=dict(size=20, color='black')
    )
    return fig

def plot_sector_distribution(cleaned_file, filters=None):
    df = pd.read_csv(cleaned_file)
    df.columns = df.columns.str.strip()

    if filters:
        # Iterate over the filters dictionary to apply multiple filters
        for filter_column, filter_values in filters.items():
            if filter_column in df.columns:
                df = df[df[filter_column].isin(filter_values)]
            else:
                raise ValueError(f"Column '{filter_column}' not found in the dataset")

    sector_distribution = df.groupby(
        ['Region', 'Sector', 'School Type', 'Modified COC']
    ).size().reset_index(name='School Count')

    fig = px.bar(
        sector_distribution,
        x='Region',
        y='School Count',
        color='Sector',
        hover_data=['School Type', 'Modified COC'],
        title="Distribution of Schools by Sector, School Type, and Modified COC"
    )
    fig.update_layout(
        barmode='stack',
        xaxis_title="Region",
        yaxis_title="School Count",
        title_font=dict(size=20, color='black')
    )
    return fig


def plot_enrollment_distribution(cleaned_file, filters=None):
    df = pd.read_csv(cleaned_file)
    df.columns = df.columns.str.strip()

    if filters:
        # Iterate over the filters dictionary to apply multiple filters
        for filter_column, filter_values in filters.items():
            if filter_column in df.columns:
                df = df[df[filter_column].isin(filter_values)]
            else:
                raise ValueError(f"Column '{filter_column}' not found in the dataset")

    enrollment_distribution = df.groupby(
        ['Region', 'Sector', 'School Type', 'Modified COC']
    )['Total Enrollment'].sum().reset_index()

    fig = px.bar(
        enrollment_distribution,
        x='Region',
        y='Total Enrollment',
        color='Sector',
        hover_data=['School Type', 'Modified COC'],
        title="Distribution of Student Enrollment by Sector, School Type, and Modified COC"
    )
    fig.update_layout(
        barmode='stack',
        xaxis_title="Region",
        yaxis_title="Total Enrollment",
        title_font=dict(size=20, color='black')
    )
    return fig


def plot_shs_track_distribution(cleaned_file, filters=None):
    df = pd.read_csv(cleaned_file)
    df.columns = df.columns.str.strip()

    if filters:
        # Iterate over the filters dictionary to apply multiple filters
        for filter_column, filter_values in filters.items():
            if filter_column in df.columns:
                df = df[df[filter_column].isin(filter_values)]
            else:
                raise ValueError(f"Column '{filter_column}' not found in the dataset")

    shs_columns = [col for col in df.columns if col.startswith('G11') or col.startswith('G12')]
    track_strand_cols = [col for col in shs_columns if any(x in col for x in ['ABM', 'HUMSS', 'STEM', 'GAS', 'TVL', 'SPORTS', 'ARTS', 'PBM'])]

    track_strand_totals = df[track_strand_cols].sum().reset_index()
    track_strand_totals.columns = ['Strand', 'Enrollment Count']
    track_strand_totals['Track/Strand'] = track_strand_totals['Strand'].apply(
        lambda x: x.replace('G11 ', '').replace('G12 ', '').replace('Male', '').replace('Female', '').strip()
    )

    summary = track_strand_totals.groupby('Track/Strand')['Enrollment Count'].sum().reset_index()

    fig = px.bar(summary,
                 x='Track/Strand',
                 y='Enrollment Count',
                 color='Track/Strand',
                 title='Distribution of Senior High School Enrollees by Track and Strand')

    fig.update_layout(
        title_font=dict(size=20, color='black'),
        barmode='stack',
        xaxis_title="Track/Strand",
        yaxis_title="Enrollment Count",
        showlegend=False
    )
    return fig

def plot_gender_distribution_shs_tracks(cleaned_file, filters=None):
    df = pd.read_csv(cleaned_file)
    df.columns = df.columns.str.strip()

    if filters:
        # Iterate over the filters dictionary to apply multiple filters
        for filter_column, filter_values in filters.items():
            if filter_column in df.columns:
                df = df[df[filter_column].isin(filter_values)]
            else:
                raise ValueError(f"Column '{filter_column}' not found in the dataset")

    # Identifying SHS columns (G11 and G12) and gender-specific columns (Male and Female)
    shs_columns = [col for col in df.columns if col.startswith('G11') or col.startswith('G12')]
    track_strand_cols = [col for col in shs_columns if any(x in col for x in ['ABM', 'HUMSS', 'STEM', 'GAS', 'TVL', 'SPORTS', 'ARTS', 'PBM'])]
    
    # Separate male and female columns for each track/strand
    male_columns = [col for col in track_strand_cols if 'Male' in col]
    female_columns = [col for col in track_strand_cols if 'Female' in col]
    
    # Summing the male and female enrollments per track/strand
    gender_distribution = pd.DataFrame({
        'Track/Strand': [col.replace('G11 ', '').replace('G12 ', '').replace('Male', '').replace('Female', '').strip() for col in male_columns],
        'Male Enrollment': [df[col].sum() for col in male_columns],
        'Female Enrollment': [df[col.replace('Male', 'Female')].sum() for col in male_columns]
    })

    # Plotting the gender distribution
    fig = px.bar(
        gender_distribution,
        x='Track/Strand',
        y=['Male Enrollment', 'Female Enrollment'],
        title="Gender Distribution Across Senior High School Tracks and Strands",
        labels={'Track/Strand': 'Track/Strand', 'value': 'Enrollment Count', 'variable': 'Gender'},
        color='variable',
        barmode='stack'
    )
    
    fig.update_layout(
        title_font=dict(size=20, color='black'),
        xaxis_title="Track/Strand",
        yaxis_title="Enrollment Count",
        showlegend=True
    )
    return fig
