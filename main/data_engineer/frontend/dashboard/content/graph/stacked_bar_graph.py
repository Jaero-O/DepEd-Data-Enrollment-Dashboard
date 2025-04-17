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

    # If no filters are applied, the function will return the overall distribution
    male_columns = [col for col in df.columns if 'Male' in col]
    female_columns = [col for col in df.columns if 'Female' in col]

    # Calculate total male and female enrollment counts
    gender_distribution = pd.DataFrame({
        'Gender': ['Male', 'Female'],
        'Enrollment Count': [
            df[male_columns].sum().sum(),
            df[female_columns].sum().sum()
        ]
    })

    # Create the plot
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
        for filter_column, filter_values in filters.items():
            if filter_column in df.columns:
                df = df[df[filter_column].isin(filter_values)]
            else:
                raise ValueError(f"Column '{filter_column}' not found in the dataset")

    # Group by Region and Sector
    sector_distribution = df.groupby(
        ['Region', 'Sector']
    ).size().reset_index(name='School Count')

    # Create the bar plot
    fig = px.bar(
        sector_distribution,
        x='Region',
        y='School Count',
        color='Sector',
        title="Distribution of Schools by Sector"
    )
    fig.update_layout(
        barmode='stack',
        xaxis_title="Region",
        yaxis_title="School Count",
        title_font=dict(size=20, color='black')
    )

    return fig


def plot_school_type_distribution(cleaned_file, filters=None):
    df = pd.read_csv(cleaned_file)
    df.columns = df.columns.str.strip()

    if filters:
        for filter_column, filter_values in filters.items():
            if filter_column in df.columns:
                df = df[df[filter_column].isin(filter_values)]
            else:
                raise ValueError(f"Column '{filter_column}' not found in the dataset")

    # Group by Region and School Type
    school_type_distribution = df.groupby(
        ['Region', 'School Type']
    ).size().reset_index(name='School Count')

    # Create the bar plot
    fig = px.bar(
        school_type_distribution,
        x='Region',
        y='School Count',
        color='School Type',
        title="Distribution of Schools by School Type"
    )
    fig.update_layout(
        barmode='stack',
        xaxis_title="Region",
        yaxis_title="School Count",
        title_font=dict(size=20, color='black')
    )

    return fig


def plot_modified_coc_distribution(cleaned_file, filters=None):
    df = pd.read_csv(cleaned_file)
    df.columns = df.columns.str.strip()

    if filters:
        for filter_column, filter_values in filters.items():
            if filter_column in df.columns:
                df = df[df[filter_column].isin(filter_values)]
            else:
                raise ValueError(f"Column '{filter_column}' not found in the dataset")

    # Group by Region and Modified COC
    modified_coc_distribution = df.groupby(
        ['Region', 'Modified COC']
    ).size().reset_index(name='School Count')

    # Create the bar plot
    fig = px.bar(
        modified_coc_distribution,
        x='Region',
        y='School Count',
        color='Modified COC',
        title="Distribution of Schools by Modified COC"
    )
    fig.update_layout(
        barmode='stack',
        xaxis_title="Region",
        yaxis_title="School Count",
        title_font=dict(size=20, color='black')
    )

    return fig


def plot_enrollment_distribution_by_sector(cleaned_file, filters=None):
    df = pd.read_csv(cleaned_file)
    df.columns = df.columns.str.strip()

    if filters:
        # Apply filters to the dataset
        for filter_column, filter_values in filters.items():
            if filter_column in df.columns:
                df = df[df[filter_column].isin(filter_values)]
            else:
                raise ValueError(f"Column '{filter_column}' not found in the dataset")

    # Grouping the data by Sector and summing the Total Enrollment
    enrollment_by_sector = df.groupby(['Sector'])['Total Enrollment'].sum().reset_index()

    # Create the bar plot
    fig = px.bar(
        enrollment_by_sector,
        x='Sector',
        y='Total Enrollment',
        title="Enrollment Distribution by Sector",
        labels={'Total Enrollment': 'Total Enrollment'},
    )
    fig.update_layout(
        xaxis_title="Sector",
        yaxis_title="Total Enrollment",
        title_font=dict(size=20, color='black')
    )
    return fig


# Function to plot enrollment distribution by School Type
def plot_enrollment_distribution_by_school_type(cleaned_file, filters=None):
    df = pd.read_csv(cleaned_file)
    df.columns = df.columns.str.strip()

    if filters:
        # Apply filters to the dataset
        for filter_column, filter_values in filters.items():
            if filter_column in df.columns:
                df = df[df[filter_column].isin(filter_values)]
            else:
                raise ValueError(f"Column '{filter_column}' not found in the dataset")

    # Grouping the data by School Type and summing the Total Enrollment
    enrollment_by_school_type = df.groupby(['School Type'])['Total Enrollment'].sum().reset_index()

    # Create the bar plot
    fig = px.bar(
        enrollment_by_school_type,
        x='School Type',
        y='Total Enrollment',
        title="Enrollment Distribution by School Type",
        labels={'Total Enrollment': 'Total Enrollment'},
    )
    fig.update_layout(
        xaxis_title="School Type",
        yaxis_title="Total Enrollment",
        title_font=dict(size=20, color='black')
    )
    return fig


# Function to plot enrollment distribution by Modified COC
def plot_enrollment_distribution_by_modified_coc(cleaned_file, filters=None):
    df = pd.read_csv(cleaned_file)
    df.columns = df.columns.str.strip()

    if filters:
        # Apply filters to the dataset
        for filter_column, filter_values in filters.items():
            if filter_column in df.columns:
                df = df[df[filter_column].isin(filter_values)]
            else:
                raise ValueError(f"Column '{filter_column}' not found in the dataset")

    # Grouping the data by Modified COC and summing the Total Enrollment
    enrollment_by_modified_coc = df.groupby(['Modified COC'])['Total Enrollment'].sum().reset_index()

    # Create the bar plot
    fig = px.bar(
        enrollment_by_modified_coc,
        x='Modified COC',
        y='Total Enrollment',
        title="Enrollment Distribution by Modified COC",
        labels={'Total Enrollment': 'Total Enrollment'},
    )
    fig.update_layout(
        xaxis_title="Modified COC",
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

    # Identify SHS columns for G11 and G12, then narrow down to track/strand columns
    shs_columns = [col for col in df.columns if col.startswith('G11') or col.startswith('G12')]
    track_strand_cols = [col for col in shs_columns if any(x in col for x in ['ABM', 'HUMSS', 'STEM', 'GAS', 'TVL', 'SPORTS', 'ARTS', 'PBM'])]

    # Sum the enrollment counts for each track/strand column
    track_strand_totals = df[track_strand_cols].sum().reset_index()
    track_strand_totals.columns = ['Strand', 'Enrollment Count']

    # Clean up the 'Strand' column names to represent track/strand names
    track_strand_totals['Track/Strand'] = track_strand_totals['Strand'].apply(
        lambda x: x.replace('G11 ', '').replace('G12 ', '').replace('Male', '').replace('Female', '').strip()
    )

    # Group by 'Track/Strand' and sum enrollment counts
    summary = track_strand_totals.groupby('Track/Strand')['Enrollment Count'].sum().reset_index()

    # Create the bar plot
    fig = px.bar(summary,
                 x='Track/Strand',
                 y='Enrollment Count',
                 color='Track/Strand',
                 title='Distribution of Senior High School Enrollees by Track and Strand')

    # Update the plot layout for better appearance
    fig.update_layout(
        title_font=dict(size=20, color='black'),
        barmode='stack',
        xaxis_title="Track/Strand",
        yaxis_title="Enrollment Count",
        showlegend=False
    )

    return fig


def plot_gender_distribution_by_shs_tracks(cleaned_file, filters=None):
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
