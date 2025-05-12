import sqlite3
import pandas as pd
from dash import html, dcc
from main.data_engineer.frontend.dashboard.content.cards.card_one import card_one
from main.data_engineer.frontend.dashboard.content.cards.card_two import card_two
from main.data_engineer.frontend.dashboard.content.cards.card_three import card_three
from main.data_engineer.frontend.dashboard.content.cards.card_four import card_four
from main.data_engineer.frontend.dashboard.content.cards.card_five import card_five
from main.data_engineer.frontend.dashboard.content.cards.card_six_ni_lei import card_six
from main.data_engineer.frontend.dashboard.content.cards.card_seven import card_seven
from main.data_engineer.frontend.dashboard.content.cards.card_seven_jhs import card_seven_jhs
from main.data_engineer.frontend.dashboard.content.cards.card_seven_shs import card_seven_shs
from main.data_engineer.frontend.dashboard.content.cards.card_eight import card_eight
from main.data_engineer.frontend.dashboard.content.cards.card_table_school import card_tabular
from main.data_engineer.frontend.dashboard.content.cards.card_table_geography import card_regional_table
from main.data_engineer.frontend.dashboard.content.cards.card_nine import card_choropleth
from main.data_engineer.frontend.dashboard.content.cards.card_ten import card_ten
from main.data_analyst_scientist.data_pipeline.combine_datasets import aggregateDataset



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




def convert_filter_to_df(filter_dict, df):

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
    active_levels = [level for level in hierarchy_order if filter_dict.get(level)]

    if active_levels:
        deepest_level = active_levels[-1]
        filtered_df = filtered_df[filtered_df[deepest_level].isin(filter_dict[deepest_level])]
        
        # Filter upwards from the deepest level
        for level in hierarchy_order:
            if level == deepest_level:
                break
            if filter_dict.get(level):
                filtered_df = filtered_df[filtered_df[level].isin(filter_dict[level])]

    final_df = filtered_df.copy()

    # Step 2: Direct filtering (non-hierarchical fields)
    for field in direct_filters:
        values = filter_dict.get(field)
        if values:
            final_df = final_df[final_df[field].isin(values)]

    # Step 3: Reverse column names back
    reverse_column_map = {v: k for k, v in column_rename_map.items()}
    final_df.rename(columns=reverse_column_map, inplace=True)
    return final_df


# Load the dataset once to access filter options
def dashboardContent(final_df, location, mode, order):
    return [
        # html.Div("School-Based Enrollment", className='card-group-title'),
        # html.Div([
        #     html.Div([
        #         card_one(final_df, mode),
        #         *card_two(final_df, mode)
        #     ], className='card-one-two-wrapper'),
        #     html.Div([
        #         card_three(final_df, mode), 
        #         card_five(final_df, mode)
        #     ], className='card-three-five-wrapper')
        # ], className='card-one-two-three-five-wrapper'),
        # html.Div([card_four(final_df, mode)], className='card-four-wrapper'),
        # html.Div("Education Level Enrollment", className='card-group-title'),
        # html.Div([
        #     card_seven_es(final_df, mode),
        #     card_seven_jhs(final_df, mode),
        #     card_seven_shs(final_df, mode)
        # ],className='card-seven-wrapper'),
        # html.Div("Geographic-Based Enrollment", className='card-group-title'),
        # html.Div(
        #     [card_six(final_df, location, mode,order)],
        #     className='card-six-wrapper'
        # ),
        # card_four(final_df, location, mode),
        # card_three(final_df, mode),
        # card_five(final_df, location, mode),        
        # card_six(final_df, location, mode),
        # card_seven(final_df, mode),
        # card_eight(final_df, location, mode)
        # add here your cards after importing  
    ]

def dashboard_content(final_df, previous_year_df, location, mode, tab, current_sy, previous_sy):
    # return None
    print("=== dashboard_content inputs ===")
    print("Location:", location)
    print("Mode:", mode)
    print("Tab:", tab)
    print("Current SY:", current_sy)
    print("Previous SY:", previous_sy)
    print("================================")
    if tab == 'school-based':
        return[
            html.Div([
                html.Div([
                    card_one(final_df, mode),
                    *card_two(final_df, mode)
                ], className='card-one-two-wrapper'),
                html.Div([
                    card_three(final_df, mode),
                    card_four(final_df,mode),
                    card_five(final_df, mode)
                ], className='card-three-four-five-wrapper')
            ], className='school-based-wrapper'),
        ]
    
    elif tab == 'level-based':
        return[
            html.Div([
                html.Div([
                    html.Div([
                        card_tabular(final_df, mode)
                    ], className='card-level-table-wrapper'),
                    html.Div([
                        card_eight(final_df, previous_year_df,current_sy, previous_sy),
                    ], className='card-eight-wrapper'),
                ], className='card-eight-card-table-wrapper'),
                html.Div([
                    # html.Div([
                    #     card_seven_es(final_df, mode),
                    #     card_seven_jhs(final_df, mode),
                    # ], className='card-seven-es-jhs-wrapper'),
                    card_seven(final_df, mode, 'ES'),
                    card_seven(final_df, mode, 'JHS'),
                    card_seven(final_df, mode, 'SHS-Academic'),
                    card_seven(final_df, mode, 'SHS-Non-Academic'),
                ], className='card-seven-wrapper'),
                
            ], className='level-based-wrapper'),
        ]
    
    elif tab == 'geographic-based':
        return [
            html.Div([
                html.Div([
                    card_ten(final_df, mode),
                    html.Div([
                        html.Div(card_six(final_df,location,mode,'desc'), className='card-six-wrapper'),
                        html.Div(card_six(final_df,location,mode,'asc'), className='card-six-wrapper'),
                    ], className='card-six-outside-wrapper')
                ], className='card-six-ten-wrapper'),
                html.Div(card_choropleth(final_df,mode, location), className='card-nine-wrapper')
            ], className='geographic-based-wrapper'),
        ]



