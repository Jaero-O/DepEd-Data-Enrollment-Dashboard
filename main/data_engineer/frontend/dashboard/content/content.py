import pandas as pd
from dash import html, dcc
from main.data_engineer.frontend.dashboard.content.cards.card_one import card_one
from main.data_engineer.frontend.dashboard.content.cards.card_two import card_two
from main.data_engineer.frontend.dashboard.content.cards.card_three import card_three
from main.data_engineer.frontend.dashboard.content.cards.card_four import card_four
from main.data_engineer.frontend.dashboard.content.cards.card_five import card_five
from main.data_engineer.frontend.dashboard.content.cards.card_six import card_six
from main.data_engineer.frontend.dashboard.content.cards.card_seven import card_seven
from main.data_engineer.frontend.dashboard.content.cards.card_eight import card_eight


# Path to preprocessed file
cleaned_file = "enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv"

# Mapping which filter fields are valid for each selection
filter_map = {
    'Region': ["Region"],
    'Division': ["Division"],
    'District': ["District"],
    'Province': ["Province"],
    'Municipality': ["Municipality"],
    'Legislative District': ["Legislative District"],
    'Barangay': ["Barangay"],
    'Sector': ["Sector"],
    'School Subclassification': ["School Subclassification"],
    'School Type': ["School Type"],
    'Modified COC': ["Modified COC"]
}


# hierarchy order for filtering

hierarchy_order = [
    'Region',
    'Legislative District',
    'Province',
    'Division',
    'District',
    'Municipality',
    'Barangay',
]
# hierarchy order for filtering (non-hierarchical fields removed)
hierarchy_order = [
    'Region',
    'Legislative District',
    'Province',
    'Division',
    'District',
    'Municipality',
    'Barangay',
]

# non-hierarchical fields
direct_filters = ['Sector', 'School Subclassification', 'School Type', 'Modified COC']

def convert_filter_to_df(filter_dict):
    csv_path = "enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv"
    df = pd.read_csv(csv_path)

    # Check if data loaded properly
    print(df.head())  # Print first few rows for debugging

    # Rename columns to match filter keys
    column_rename_map = {
        'region': 'Region',
        'division': 'Division',
        'district': 'District',
        'beis_school_id': 'BEIS School ID',
        'school_name': 'School Name',
        'street_address': 'Street Address',
        'province': 'Province',
        'municipality': 'Municipality',
        'legislative_district': 'Legislative District',
        'barangay': 'Barangay',
        'sector': 'Sector',
        'school_subclassification': 'School Subclassification',
        'school_type': 'School Type',
        'modified_coc': 'Modified COC'
    }
    df.rename(columns=column_rename_map, inplace=True)

    # Handle if no filters are provided
    if filter_dict is None:
        final_df = df.drop_duplicates(subset='BEIS School ID')
        return final_df

    # Normalize filter values
    for key, value in filter_dict.items():
        if value is None:
            filter_dict[key] = []
        elif isinstance(value, str):
            filter_dict[key] = [value]

    # Step 1: Hierarchical filtering
    filtered_df = df.copy()
    for level in hierarchy_order[::-1]:
        if filter_dict.get(level):
            filtered_df = filtered_df[filtered_df[level].isin(filter_dict[level])]

    # Debugging: Show filtered dataframe after hierarchical filtering
    print(f"Filtered DataFrame after hierarchical filters: \n{filtered_df.head()}")

    updated_filter_dict = {
        level: sorted(filtered_df[level].dropna().unique().tolist())
        for level in hierarchy_order
    }

    # Step 2: Apply direct filters
    for field in direct_filters:
        values = filter_dict.get(field)
        if values:  # Only apply the filter if values exist and are not empty
            filtered_df = filtered_df[filtered_df[field].isin(values)]

    # Debugging: Show final filtered dataframe
    print(f"Final DataFrame after all filters: \n{filtered_df.head()}")

    # Ensure dataframe is not empty
    if filtered_df.empty:
        print("No data matches the selected filters.")
        return pd.DataFrame(columns=df.columns)

    # Return the filtered dataframe with original column names
    reverse_column_map = {v: k for k, v in column_rename_map.items()}
    filtered_df.rename(columns=reverse_column_map, inplace=True)
    
    return filtered_df


# Load the dataset once to access filter options
def dashboardContent(filtered_df, location, mode):
    return (
        card_one(filtered_df, location, mode),
        # card_two(final_df, location, mode),
        # card_three(final_df, location, mode),
        # card_four(final_df, location, mode),
        # card_five(final_df, location, mode),        
        # card_six(final_df, location, mode),
        # card_seven(final_df, location, mode),
        # card_eight(final_df, location, mode)
        # add here your cards after importing  
    )