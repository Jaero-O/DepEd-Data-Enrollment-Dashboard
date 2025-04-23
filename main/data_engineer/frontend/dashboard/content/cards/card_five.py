import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re

def preserve_parentheses_title(text):
    text = text.lower()  # Normalize first

    def smart_title_case(s):
        if not s.strip():
            return ''
        exceptions = {'or', 'and', 'of', 'the', 'in', 'on', 'by', 'to', 'with'}
        words = s.split()
        result = [words[0].capitalize()]
        for word in words[1:]:
            if word.lower() in exceptions:
                result.append(word.lower())
            else:
                result.append(word.capitalize())
        return ' '.join(result)

    def sentence_case(s):
        if not s.strip():
            return ''
        return s[0].lower() + s[1:].lower()

    parts = re.split(r'(\(.*?\))', text)
    processed_parts = []
    for part in parts:
        if part.startswith('(') and part.endswith(')'):
            inner = part[1:-1]
            processed_parts.append(f'({inner})'.lower())
        else:
            titled = smart_title_case(part)
            # Apply slash rule only when `titled` is assigned
            titled = re.sub(r'/\s*([a-z])', lambda m: '/' + m.group(1).upper(), titled)
            processed_parts.append(titled)
    return ''.join(processed_parts)




def card_five(df, mode='student'):
    print(preserve_parentheses_title("Mobile School(S)/center(S)"))

    if df.empty:
        df = pd.read_csv("enrollment_csv_file/preprocessed_data/cleaned_enrollment_data.csv")

    if mode == 'school':
        df = df.groupby(['school_type']).size().reset_index(name='total')
        card_five_title = 'No. of Schools'

    elif mode == 'student':
        grade_cols = [col for col in df.columns if '_male' in col or '_female' in col]
        df = df[['school_type'] + grade_cols]
        df['total'] = df[grade_cols].sum(axis=1)
        card_five_title = 'Enrollment'

    # Group and sort
    grouped = df.groupby('school_type')[['total']].sum().sort_values(by='total', ascending=False)
    categories = [{"name": idx, "value": row["total"]} for idx, row in grouped.iterrows()]

    # Add some breathing room on the right for the labels
    x_max = grouped['total'].max() * 1.20

    # Create subplots
    subplots = make_subplots(
        rows=len(categories),
        cols=1,
        subplot_titles=[preserve_parentheses_title(x["name"]) for x in categories],
        shared_xaxes=True,
        vertical_spacing=(0.01 / len(categories)),
    )

    for k, x in enumerate(categories):
        # Background gray bar
        subplots.add_trace(go.Bar(
            orientation='h',
            y=[x["name"]],
            x=[x_max],  # full length background bar
            marker=dict(color="#e6e6e6"),  # light gray
            hoverinfo='skip',
        ), row=k + 1, col=1)

        subplots.add_trace(go.Bar(
            orientation='h',
            y=[x["name"]],
            x=[x["value"]],
            marker=dict(color="#21D7E4"),
            hoverinfo='text',
            text=[f'{round(x["value"]):,}'],
            textposition='none', 
            showlegend=False
        ), row=k + 1, col=1)

        buffer = x_max * 0.02  # 2% of full width, adjust if needed

    # Update layout
    print("Subplots:", subplots)
    for ann in subplots["layout"]["annotations"]:
        ann["x"] = 0
        ann["xanchor"] = "left"
        ann["align"] = "left"
        ann["font"] = dict(size=14, family="Inter", weight=600, color='#2a4d69')
        if len(categories) > 1:
            ann["yshift"] = -65 * (1/(len(categories)))
        else:
            ann["yshift"] = -45

    if len(categories) > 1:
            width_gap = max(0.40, min(0.9, 1.1 / (len(categories))))
    else:
        width_gap = 0.65
    
    layout_updates = {
        "barmode": "overlay",
        "showlegend": False,
        "width": 345,
        "height": min(350, 70 +  80* len(categories)),     
        "margin": dict(t=0, b=0, l=0, r=10),
        "template": "simple_white",
        "paper_bgcolor": 'rgba(0,0,0,0)',
        "plot_bgcolor": 'rgba(0,0,0,0)',
        "xaxis": {
            "range": [0, x_max],
            "showgrid": False,
            "zeroline": False,
            "visible": False,
        },
        "yaxis": {
            "showgrid": False,
            "zeroline": False,
            "visible": False,
        },
        "bargroupgap": width_gap,
        "font": dict(family="Inter", size=12, color="black"),
    }

    for i in range(1, len(categories) + 1):
        layout_updates[f'xaxis{i}'] = dict(visible=False, range=[0, x_max])
        layout_updates[f'yaxis{i}'] = dict(visible=False)

    subplots.update_layout(**layout_updates)

    return html.Div([
            html.Div([
                html.Div(
                f"Enrollment by School Type",
                className='card-title-main'),
            ],className='card-header-wrapper'),
            html.Div([
                dcc.Graph(figure=subplots, config={'displayModeBar': False}),
            ], 
            className='card-five-graph'),
        ], className='card card-five')

def card_five_register_callbacks(app):
    return None