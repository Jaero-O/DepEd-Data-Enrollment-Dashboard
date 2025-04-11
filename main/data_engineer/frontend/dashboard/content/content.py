from dash import html, dcc
from main.data_engineer.frontend.dashboard.content.graph.stacked_bar_graph import (
    plot_gender_distribution,
    plot_sector_distribution,
    plot_enrollment_distribution,
    plot_shs_track_distribution,
    plot_gender_distribution_by_shs_tracks
)

# Import the summary functions
from main.data_engineer.frontend.dashboard.content.graph.table1 import create_school_count_summary, create_student_enrollment_summary

cleaned_file = "enrollment_csv_file/preprocessed_data/total_enrollment.csv"

def dashboardContent(selection, filters):
    # Create graphs for gender, sector, enrollment, and SHS tracks
    fig_gender = plot_gender_distribution(cleaned_file, filters)
    fig_sector = plot_sector_distribution(cleaned_file, filters)
    fig_enrollment = plot_enrollment_distribution(cleaned_file, filters)
    fig_shs = plot_shs_track_distribution(cleaned_file, filters)
    fig_gender_track = plot_gender_distribution_by_shs_tracks(cleaned_file, filters)

    # Create the school count summary inside a styled box
    summary_schools = create_school_count_summary(cleaned_file, filters)
    
    # Create the student enrollment summary inside a styled box
    summary_students = create_student_enrollment_summary(cleaned_file, filters)

    # Return the layout including graphs and summaries
    return [
        html.P('Hi'),
        html.P('Hello'),
        dcc.Graph(figure=fig_gender),
        dcc.Graph(figure=fig_sector),
        dcc.Graph(figure=fig_enrollment),
        dcc.Graph(figure=fig_shs),
        dcc.Graph(figure=fig_gender_track),
        summary_schools,  # Show the school summary inside a box
        summary_students  # Show the student enrollment summary inside a box
    ]
