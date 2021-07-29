import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import time

import dash_table as table

import pandas as pd

from room_check import live_room_check

# https://databraineo.com/ki-training-resources/python/interaktive-dashboards-in-python-plotly-dash-tutorial/

df_room = live_room_check()

from api_access import *

# https://databraineo.com/ki-training-resources/python/interaktive-dashboards-in-python-plotly-dash-tutorial/

def consumption_balance():
    # @TODO Add coloring for hours that have negative balance?
    # @TODO Add balance target? Can't be zero during the night

    ts_end = int(time.time())
    ts_start = ts_end - (60 * 60 * 24)

    data = query_building(60, ts_start, ts_end)
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

def current_room_balance():
    data = query_live_data()

    return data['building']['totalPowerConsumption'] - data['building']['powerConsumptionDataCenter']

def build_layout(app):
    app.layout = html.Div(
        children=[
            html.H1(children="Codility Challenge 2021 - Group 6"),
            html.Div(
                children=[
                    dcc.Graph(
                        id="balance",
                        figure=consumption_balance()),
                    html.H2(children="Aktueller Verbrauch durch Büroräume"),
                    html.P(f"{current_room_balance():.2}"),                    
                    table.DataTable(
                        id='room_overview',
                        editable=False,
                        columns=[{"name": i, "id": i} for i in
                            ['Raum', 'Probleme']],
                        data=df_room,
                        style_cell={'textAlign': 'center'},
                        style_as_list_view=True,
                        style_data_conditional=[
                            {
                                'if': {
                                    'filter_query': '{In Ordnung} != true',
                                },
                                'backgroundColor': 'tomato',
                                'color': 'white'
                            },
                            {
                                'if': {
                                    'filter_query': '{In Ordnung} != false',
                                },
                                'backgroundColor': 'green',
                                'color': 'white'
                            }
                        ]
                    )
                ],
            ),            
        ]
    )