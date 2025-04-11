import pandas as pd
import dash_html_components as html

def styled_summary_box(count, label):
    return html.Div([
        html.Div(str(count), style={
            'fontSize': '24px',
            'fontWeight': 'bold',
            'color': '#2c3e50'
        }),
        html.Div(label, style={
            'fontSize': '14px',
            'color': '#7f8c8d'
        })
    ], style={
        'marginBottom': '15px',
        'textAlign': 'center',
        'padding': '10px',
        'borderRadius': '10px',
        'backgroundColor': '#f9f9f9',
        'boxShadow': '0px 2px 4px rgba(0, 0, 0, 0.05)'
    })


def create_school_count_summary(cleaned_file, filters=None):
    df = pd.read_csv(cleaned_file)
    df.columns = df.columns.str.strip()
    summary_items = []

    if not filters or all(len(v) == 0 for v in filters.values()):
        for region in df['Region'].unique():
            region_df = df[df['Region'] == region]
            count = region_df.shape[0]
            summary_items.append(styled_summary_box(count, f"Region ({region})"))
    else:
        matched_regions = {}

        for filter_column, filter_values in filters.items():
            if filter_column in df.columns and filter_values:
                for value in filter_values:
                    filtered = df[df[filter_column] == value]
                    for region in filtered['Region'].unique():
                        region_total = df[df['Region'] == region].shape[0]
                        if region not in matched_regions:
                            matched_regions[region] = {
                                'total': region_total,
                                'details': []
                            }
                        matched_count = filtered.shape[0]
                        if filter_column == "Region" and value == region:
                            continue
                        matched_regions[region]['details'].append({
                            'label': f"{filter_column} ({value})",
                            'count': matched_count
                        })

        for region, data in matched_regions.items():
            summary_items.append(styled_summary_box(data['total'], f"Region ({region})"))
            sorted_details = sorted(data['details'], key=lambda x: x['count'], reverse=True)
            for d in sorted_details:
                summary_items.append(styled_summary_box(d['count'], f"↳ {d['label']}"))

    return html.Div([
        html.H3("School Count Summary", style={'marginBottom': '20px'}),
        html.Div(summary_items)
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',
        'lineHeight': '1.8'
    })


def create_student_enrollment_summary(cleaned_file, filters=None):
    df = pd.read_csv(cleaned_file)
    df.columns = df.columns.str.strip()

    enrollment_columns = [
        'K Male', 'K Female', 'G1 Male', 'G1 Female', 'G2 Male', 'G2 Female',
        'G3 Male', 'G3 Female', 'G4 Male', 'G4 Female', 'G5 Male', 'G5 Female',
        'G6 Male', 'G6 Female', 'Elem NG Male', 'Elem NG Female', 'G7 Male',
        'G7 Female', 'G8 Male', 'G8 Female', 'G9 Male', 'G9 Female', 'G10 Male',
        'G10 Female', 'JHS NG Male', 'JHS NG Female', 'G11 ACAD - ABM Male',
        'G11 ACAD - ABM Female', 'G11 ACAD - HUMSS Male', 'G11 ACAD - HUMSS Female',
        'G11 ACAD STEM Male', 'G11 ACAD STEM Female', 'G11 ACAD GAS Male',
        'G11 ACAD GAS Female', 'G11 ACAD PBM Male', 'G11 ACAD PBM Female',
        'G11 TVL Male', 'G11 TVL Female', 'G11 SPORTS Male', 'G11 SPORTS Female',
        'G11 ARTS Male', 'G11 ARTS Female', 'G12 ACAD - ABM Male', 'G12 ACAD - ABM Female',
        'G12 ACAD - HUMSS Male', 'G12 ACAD - HUMSS Female', 'G12 ACAD STEM Male',
        'G12 ACAD STEM Female', 'G12 ACAD GAS Male', 'G12 ACAD GAS Female',
        'G12 ACAD PBM Male', 'G12 ACAD PBM Female', 'G12 TVL Male', 'G12 TVL Female',
        'G12 SPORTS Male', 'G12 SPORTS Female', 'G12 ARTS Male', 'G12 ARTS Female'
    ]

    df['Enrollment'] = df[enrollment_columns].sum(axis=1)
    summary_items = []

    if not filters or all(len(v) == 0 for v in filters.values()):
        for region in df['Region'].unique():
            region_df = df[df['Region'] == region]
            total = int(region_df['Enrollment'].sum())
            summary_items.append(styled_summary_box(total, f"Region ({region})"))
    else:
        matched_regions = {}

        for filter_column, filter_values in filters.items():
            if filter_column in df.columns and filter_values:
                for value in filter_values:
                    filtered = df[df[filter_column] == value]
                    for region in filtered['Region'].unique():
                        region_total = int(df[df['Region'] == region]['Enrollment'].sum())
                        if region not in matched_regions:
                            matched_regions[region] = {
                                'total': region_total,
                                'details': []
                            }
                        matched_total = int(filtered['Enrollment'].sum())
                        if filter_column == "Region" and value == region:
                            continue
                        matched_regions[region]['details'].append({
                            'label': f"{filter_column} ({value})",
                            'count': matched_total
                        })

        for region, data in matched_regions.items():
            summary_items.append(styled_summary_box(data['total'], f"Region ({region})"))
            sorted_details = sorted(data['details'], key=lambda x: x['count'], reverse=True)
            for d in sorted_details:
                summary_items.append(styled_summary_box(d['count'], f"↳ {d['label']}"))

    return html.Div([
        html.H3("Student Enrollment Summary", style={'marginBottom': '20px'}),
        html.Div(summary_items)
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',
        'lineHeight': '1.8'
    })