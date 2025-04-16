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
# Each selection maps to the filters you'd like to apply
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

    # Rename columns
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

    updated_filter_dict = {
        level: sorted(filtered_df[level].dropna().unique().tolist())
        for level in hierarchy_order
    }

    top_level = hierarchy_order[0]
    beis_school_ids = []
    matched_rows_list = []

    for top_value in filter_dict.get(top_level, []):
        subset_df = df[df[top_level] == top_value]

        for level in hierarchy_order[::-1]:
            if level in filter_dict and level in df.columns:
                valid_values = set(filter_dict[level])
                matched_values = set(subset_df[level].dropna().unique())
                intersection = valid_values & matched_values
                if intersection:
                    matched_rows = subset_df[subset_df[level].isin(intersection)]
                    beis_school_ids.extend(matched_rows['BEIS School ID'].dropna().tolist())
                    matched_rows_list.append(matched_rows)
                    break

    # Combine matched rows
    if matched_rows_list:
        final_df = pd.concat(matched_rows_list, ignore_index=True)
        final_df = final_df.drop_duplicates(subset='BEIS School ID')
    else:
        final_df = pd.DataFrame(columns=df.columns)

    for field in direct_filters:
        values = filter_dict.get(field)
        if values:  # Only apply the filter if values exist and are not empty
            final_df = final_df[final_df[field].isin(values)]

    print("\n📊 Matched DataFrame based on filters:")
    print(final_df)

    # Reverse column names back
    reverse_column_map = {v: k for k, v in column_rename_map.items()}
    final_df.rename(columns=reverse_column_map, inplace=True)

    return final_df


# Load the dataset once to access filter options
def dashboardContent(final_df, location, mode):
    return (
        card_one(final_df, location, mode),
        card_two(final_df, location, mode),
        card_three(final_df, location, mode),
        card_four(final_df, location, mode),
        card_five(final_df, location, mode),        
        card_six(final_df, location, mode),
        card_seven(final_df, location, mode),
        card_eight(final_df, location, mode)
        # add here your cards after importing  
    )


