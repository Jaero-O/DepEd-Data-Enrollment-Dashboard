from dash import html, dcc
from main.data_engineer.frontend.dashboard.content.graph.data_story_1 import (
    get_total_enrollment_kpi,
    plot_gender_ratio_donut
)
# Path to preprocessed file
cleaned_file = "enrollment_csv_file/preprocessed_data/total_enrollment.csv"

# Each selection maps to the filters you'd like to apply
# Mapping which filter fields are valid for each selection
filter_map = {
    'Region': ["Region"],
    'Division': ["Division"],
    'District': ["District"],
    'Province': ["Province"],
    'Municipality': ["Municipality"],
    'Legislative District': ["Legislative District"],
    'Barangay': ["Barangay"]
}

def dashboardContent(selection, filters):
    # Determine which filter keys to retain for the current selection
    valid_filter_keys = filter_map.get(selection, [])
    
    # Keep only the relevant filters
    filtered_filters = {
        k: v for k, v in filters.items() if k in valid_filter_keys
    }
    
    # Default to empty filters if no valid filters found
    if not filtered_filters:
        filtered_filters = {}

    # Generate the relevant figures for the current selection
    fig_total_enrollment= get_total_enrollment_kpi(cleaned_file, filtered_filters)
    fig_gender_ratio = plot_gender_ratio_donut(cleaned_file, filtered_filters)
    

    # Return the layout with relevant data for the selected tab
    return [
        html.P(f"Displaying data for {selection}", style={"fontWeight": "bold"}),
        dcc.Graph (fig_total_enrollment),
        dcc.Graph (fig_gender_ratio)
    ]
