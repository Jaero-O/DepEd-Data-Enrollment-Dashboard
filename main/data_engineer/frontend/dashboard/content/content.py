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
    fig_non_graded = plot_non_graded_enrollment_bar(cleaned_file, filters)
    fig_ng_enrollees = plot_grouped_non_graded_enrollment(cleaned_file, filters)

    # Create the school count summary inside a styled box
    summary_schools = create_school_count_summary(cleaned_file, filters)
    
    # Create the student enrollment summary inside a styled box
    summary_students = create_student_enrollment_summary(cleaned_file, filters)

    # Return the layout including graphs and summaries
    return [
        html.Div([html.P('Hi'), html.P('Hello')]),
        html.Div(dcc.Graph(figure=fig_gender), style={'marginBottom': '30px'}),
        html.Div(dcc.Graph(figure=fig_sector), style={'marginBottom': '30px'}),
        html.Div(dcc.Graph(figure=fig_enrollment), style={'marginBottom': '30px'}),
        html.Div(dcc.Graph(figure=fig_shs), style={'marginBottom': '30px'}),
        html.Div(dcc.Graph(figure=fig_gender_track), style={'marginBottom': '30px'}),
        html.Div(dcc.Graph(figure=fig_non_graded), style={'marginBottom': '30px'}),
        html.Div(dcc.Graph(figure=fig_ng_enrollees), style={'marginBottom': '30px'}),
        html.Div([
            html.Div(summary_schools, style={'marginBottom': '30px'}),
            html.Div(summary_students, style={'marginBottom': '30px'})
        ], style={'display': 'flex', 'flexWrap': 'wrap'})
    ]
