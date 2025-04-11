from dash import html, dcc
from main.data_engineer.frontend.dashboard.content.graph.stacked_bar_graph import (
    plot_gender_distribution,
    plot_sector_distribution,
    plot_enrollment_distribution,
    plot_shs_track_distribution,
    plot_gender_distribution_by_shs_tracks
)
from main.data_engineer.frontend.dashboard.content.graph.bar_graph import plot_non_graded_enrollment_bar
from main.data_engineer.frontend.dashboard.content.graph.grouped_bar_graph import plot_grouped_non_graded_enrollment

# Path to preprocessed file
cleaned_file = "enrollment_csv_file/preprocessed_data/total_enrollment.csv"

def dashboardContent(selection, filters):
    fig_gender = plot_gender_distribution(cleaned_file, filters)
    fig_sector = plot_sector_distribution(cleaned_file, filters)
    fig_enrollment = plot_enrollment_distribution(cleaned_file, filters)
    fig_shs = plot_shs_track_distribution(cleaned_file, filters)
    fig_gender_track = plot_gender_distribution_by_shs_tracks(cleaned_file, filters)
    fig_non_graded = plot_non_graded_enrollment_bar(cleaned_file, filters)
    fig_ng_enrollees = plot_grouped_non_graded_enrollment(cleaned_file, filters)

    return [
            html.P('Hi'),
            html.P('Hello'),
            dcc.Graph(figure=fig_gender),
            dcc.Graph(figure=fig_sector),
            dcc.Graph(figure=fig_enrollment),
            dcc.Graph(figure=fig_shs),
            dcc.Graph(figure=fig_gender_track),
            dcc.Graph(figure=fig_non_graded),
            dcc.Graph(figure=fig_ng_enrollees)
        ]
    
