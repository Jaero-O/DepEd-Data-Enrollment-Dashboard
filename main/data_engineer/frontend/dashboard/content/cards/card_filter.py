# from dash import html, dcc
# from dash.dependencies import Input, Output, State
# from dash import html, dcc

# def card_filter(option=None):
#     filter1_dropdown = dcc.Dropdown(
#         id='filter1',
#         options=[
#             {'label': 'Overall', 'value': 'overall'},
#             {'label': 'By Region', 'value': 'region'},
#             {'label': 'By Division', 'value': 'division'},
#             {'label': 'By District', 'value': 'district'},
#             {'label': 'By Legislative District', 'value': 'legislative_district'},
#             {'label': 'By Province', 'value': 'province'},
#             {'label': 'By Municipality', 'value': 'municipality'},
#             {'label': 'By Barangay', 'value': 'barangay'},
#         ],
#         value='overall',
#         clearable=False,
#         placeholder="Select Location Filter",
#         className='filter-dropdown'
#     )

#     # filter2_dropdown = dcc.Dropdown(
#     #     id='mode-filter',
#     #     options=[
#     #         {'label': 'Enrollment Data', 'value': 'student'},
#     #         {'label': 'School Data', 'value': 'school'},
#     #     ],
#     #     value='student',
#     #     clearable=False,
#     #     placeholder="Select Data Type",
#     #     className='filter-dropdown'
#     # )

#     order_radio = dcc.RadioItems(
#         id='card-six-order-toggle',
#         options=[
#             {'label': 'Highest', 'value': 'desc'},
#             {'label': 'Lowest', 'value': 'asc'}
#         ],
#         value='desc',
#         labelStyle={'display': 'inline-block', 'margin-right': '10px'},
#         inputStyle={'margin-right': '4px'},
#         className='order-toggle-radio'
#     )

#     if option == 'location dropdown':
#         return None


# # def card_filter_register_callbacks(app):
# #     from dash import Output, Input

# #     @app.callback(  # Correct ID reference
# #         Output('filter2', 'value'),  # Correct ID reference
# #         Input('filter2', 'value')
# #     )
# #     def update_filters(filter2_value):
# #         return filter2_value

# #     @app.callback(
# #         Output('selected-filters', 'data'),
# #         Input('filter2', 'value')
# #     )
# #     def update_selected_filters(filter2_value):
# #         selected_filters = {
# #             'filter2': filter2_value if filter2_value else 'student',
# #         }
# #         return selected_filters