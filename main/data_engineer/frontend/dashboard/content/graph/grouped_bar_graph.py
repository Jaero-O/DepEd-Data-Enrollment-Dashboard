import pandas as pd
import plotly.express as px

def plot_grouped_non_graded_enrollment(cleaned_file, filters=None):
    # Read the preprocessed CSV file
    df = pd.read_csv(cleaned_file)
    df.columns = df.columns.str.strip()  # Strip any extra spaces from column names

    # Apply any filters if necessary
    if filters:
        for filter_column, filter_values in filters.items():
            if filter_column in df.columns:
                df = df[df[filter_column].isin(filter_values)]  # Apply filter for multiple values
            else:
                raise ValueError(f"Column '{filter_column}' not found in the dataset")

    # Create a DataFrame to summarize non-graded enrollments
    df_summary = pd.DataFrame({
        'Category': ['Elementary', 'Junior High School'],
        'Non-graded Enrollees': [
            df['Elem NG Male'].sum() + df['Elem NG Female'].sum(),  # Total non-graded for elementary
            df['JHS NG Male'].sum() + df['JHS NG Female'].sum()   # Total non-graded for junior high
        ]
    })

    # Create a grouped bar graph
    fig = px.bar(df_summary,
                 x='Category', 
                 y='Non-graded Enrollees', 
                 title="Total Non-Graded Enrollees in Elementary and Junior High School",
                 labels={'Non-graded Enrollees': 'Number of Non-Graded Enrollees'},
                 color='Category')

    fig.update_layout(
        yaxis_title="Number of Non-Graded Enrollees",
        title_x=0.5,
        height=400
    )

    return fig