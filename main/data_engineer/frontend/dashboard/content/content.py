from dash import html, dcc
from main.data_engineer.frontend.dashboard.content.graph.stacked_bar_graph import (
    plot_gender_distribution,
    plot_sector_distribution,
    plot_enrollment_distribution_by_sector,
    plot_enrollment_distribution_by_school_type,
    plot_enrollment_distribution_by_modified_coc,
    plot_shs_track_distribution,
    plot_gender_distribution_by_shs_tracks,
    plot_school_type_distribution,
    plot_modified_coc_distribution
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
    fig_gender = plot_gender_distribution(cleaned_file, filtered_filters)
    fig_sector = plot_sector_distribution(cleaned_file, filtered_filters)
    fig_school_type = plot_school_type_distribution(cleaned_file, filtered_filters)
    fig_modified_coc = plot_modified_coc_distribution(cleaned_file, filtered_filters)
    
    # Updated: Separate graphs for enrollment distribution by sector, school type, and modified COC
    fig_enrollment_by_sector = plot_enrollment_distribution_by_sector(cleaned_file, filtered_filters)
    fig_enrollment_by_school_type = plot_enrollment_distribution_by_school_type(cleaned_file, filtered_filters)
    fig_enrollment_by_modified_coc = plot_enrollment_distribution_by_modified_coc(cleaned_file, filtered_filters)
    
    fig_shs = plot_shs_track_distribution(cleaned_file, filtered_filters)
    fig_gender_track = plot_gender_distribution_by_shs_tracks(cleaned_file, filtered_filters)

    # Return the layout with relevant data for the selected tab
    return [
        html.P(f"Displaying data for {selection}", style={"fontWeight": "bold"}),
        dcc.Graph(figure=fig_gender),
        dcc.Graph(figure=fig_sector),
        dcc.Graph(figure=fig_school_type),
        dcc.Graph(figure=fig_modified_coc),
        dcc.Graph(figure=fig_enrollment_by_sector),
        dcc.Graph(figure=fig_enrollment_by_school_type),
        dcc.Graph(figure=fig_enrollment_by_modified_coc),
        dcc.Graph(figure=fig_shs),
        dcc.Graph(figure=fig_gender_track)
    ]
