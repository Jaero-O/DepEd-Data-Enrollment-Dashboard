import pandas as pd
import plotly.express as px

def plot_non_graded_enrollment_bar(cleaned_file, filters=None):
    df = pd.read_csv(cleaned_file)
    df.fillna(0, inplace=True)

    if filters:
        # Iterate over the filters dictionary to apply multiple filters
        for filter_column, filter_values in filters.items():
            if filter_column in df.columns:
                df = df[df[filter_column].isin(filter_values)]
            else:
                raise ValueError(f"Column '{filter_column}' not found in the dataset")

    # Calculate total NG enrollees
    df['Total NG'] = (
        df['Elem NG Male'] + df['Elem NG Female'] +
        df['JHS NG Male'] + df['JHS NG Female']
    )

    # Filter to schools with NG enrollees
    ng_schools = df[df['Total NG'] > 0]

    # Group and count
    ng_by_region = ng_schools.groupby('Region')['School Name'].nunique().reset_index()
    ng_by_region.columns = ['Region', 'Schools with NG Enrollees']

    # Plot
    fig = px.bar(
        ng_by_region,
        x='Region',
        y='Schools with NG Enrollees',
        title='Number of Schools with Non-Graded Enrollees',
        labels={'Schools with NG Enrollees': 'Number of Schools'},
        text='Schools with NG Enrollees'
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_tickangle=-45)

    return fig