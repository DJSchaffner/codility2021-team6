import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import time

from api_access import *

# https://databraineo.com/ki-training-resources/python/interaktive-dashboards-in-python-plotly-dash-tutorial/

def consumption_balance():
    # @TODO Add coloring for hours that have negative balance?
    # @TODO Add balance target? Can't be zero during the night

    ts_end = int(time.time())
    # There seems to be a bug in the api
    # @TODO increase interval to show last 24 hours
    ts_start = ts_end - (60 * 60)

    data = query_building(10, ts_start, ts_end)
    interval_balance = [e['building']['totalPowerConsumption'] - e['building']['solarPowerOutput'] for e in data]

    figure = {
        'data': [
            {'y': interval_balance, 'type': 'bar', 'name': 'SF'}
        ],
        'layout': {
            'title': 'Stromverbrauch pro Stunde',
            'autosize': True,
            'xaxis': { 'title': 'Stunde', 'autorange': False},
            'yaxis': { 'title': 'Verbrauch'}
        }
    }

    return figure

def build_layout(app):
    app.layout = html.Div(
        children=[
            html.H1(children="Codility Challenge 2021 - Group 6"),
            html.Div(
                children=[
                    dcc.Graph(
                        id="balance",
                        figure=consumption_balance())
                ],
            ),
        ]
    )