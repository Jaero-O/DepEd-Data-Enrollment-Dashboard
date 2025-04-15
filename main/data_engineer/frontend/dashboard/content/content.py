import pandas as pd
from dash import html, dcc
from main.data_engineer.frontend.dashboard.content.graph.stacked_bar_graph import (
    plot_gender_distribution,
    plot_sector_distribution,
    plot_enrollment_distribution,
    plot_shs_track_distribution,
    plot_gender_distribution_by_shs_tracks
)

# Path to preprocessed file
cleaned_file = "enrollment_csv_file/preprocessed_data/total_enrollment.csv"

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
    csv_path = "enrollment_csv_file/preprocessed_data/total_enrollment.csv"
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
# def dashboardContent(selection, updated_filter):

    # # Determine which filter keys to retain for the current selection
    # valid_filter_keys = filter_map.get(selection, [])

    # # Initialize a dictionary for effective filters
    # effective_filters = {}

    # for key in valid_filter_keys:
    #     if key in updated_filter and updated_filter[key]:
    #         effective_filters[key] = updated_filter[key]
    #     elif key in df.columns:
    #         # Use all unique values as default filter
    #         effective_filters[key] = df[key].dropna().unique().tolist()

    # print(f"Effective filters applied: {effective_filters}")
    # print(f"Selection: {selection}")

    # # Generate plots using the updated filters
    # fig_gender = plot_gender_distribution(cleaned_file, effective_filters)
    # fig_sector = plot_sector_distribution(cleaned_file, effective_filters)
    # fig_enrollment = plot_enrollment_distribution(cleaned_file, effective_filters)
    # fig_shs = plot_shs_track_distribution(cleaned_file, effective_filters)
    # fig_gender_track = plot_gender_distribution_by_shs_tracks(cleaned_file, effective_filters)

    # return [
    #     html.P(f"Displaying data for {selection}", style={"fontWeight": "bold"}),
    #     dcc.Graph(figure=fig_gender),
    #     dcc.Graph(figure=fig_sector),
    #     dcc.Graph(figure=fig_enrollment),
    #     dcc.Graph(figure=fig_shs),
    #     dcc.Graph(figure=fig_gender_track),
    # ]