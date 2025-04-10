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

# A dictionary to map selections to filter types
filter_map = {
    "Region": "region_filter",
    "Division": "division_filter",
    "District": "division_filter",
    "Province": "division_filter",
    "Municipality": "division_filter",
    "Legislative District": "division_filter",
    "Barangay": "division_filter"
}

def dashboardContent(selection, filters):
    # Get the corresponding filter type for the selected tab
    filter_type = filter_map.get(selection, None)

    # Generate figures based on the selection and filter type
    fig_gender = plot_gender_distribution(cleaned_file, filters, **{filter_type: True} if filter_type else {})
    fig_sector = plot_sector_distribution(cleaned_file, filters, **{filter_type: True} if filter_type else {})
    fig_enrollment = plot_enrollment_distribution(cleaned_file, filters, **{filter_type: True} if filter_type else {})
    fig_shs = plot_shs_track_distribution(cleaned_file, filters, **{filter_type: True} if filter_type else {})
    fig_gender_track = plot_gender_distribution_by_shs_tracks(cleaned_file, filters, **{filter_type: True} if filter_type else {})

    return [
        html.P(f"Displaying data for {selection}"),
        dcc.Graph(figure=fig_gender),
        dcc.Graph(figure=fig_sector),
        dcc.Graph(figure=fig_enrollment),
        dcc.Graph(figure=fig_shs),
        dcc.Graph(figure=fig_gender_track),
    ]
