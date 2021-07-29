import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import time

from api_access import *

# https://databraineo.com/ki-training-resources/python/interaktive-dashboards-in-python-plotly-dash-tutorial/

def consumption():
    ts_end = int(time.time())
    ts_start = ts_end - (60 * 60 * 24)

    data = query_building(60, ts_start, ts_end)
    x = []

    return {
        'data': [
            {'x': [1, 2, 3], 'type': 'bar', 'name': 'SF'}
        ],
        'layout': {
            'title': 'Stromverbrauch pro Stunde',
            'xaxis': { 'title': 'Stunde', 'autorange': False},
            'yaxis': { 'title': 'Verbrauch'}
        }
    }

def build_layout(app):
    app.layout = html.Div(
        children=[
            html.H1(children="Codility Challenge 2021 - Group 6"),
            html.Div(
                children=[
                    dcc.Graph(
                        id="consumption",
                        figure=consumption())
                ],
            ),
        ]
    )