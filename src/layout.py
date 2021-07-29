import time

import dash_table as table
import dash_html_components as html
import dash_core_components as dcc

from room_check import live_room_check

from api_access import *


# https://databraineo.com/ki-training-resources/python/interaktive-dashboards-in-python-plotly-dash-tutorial/

def consumption_balance():
    """Generates a figure for the power consumption balance to display.

    Returns:
        Figure: The Figure containing the calculated data.
    """
    # @TODO Add coloring for hours that have negative balance?
    # @TODO Add balance target? Can't be zero during the night

    ts_end = int(time.time())
    ts_start = ts_end - (60 * 60 * 24)

    data = query_building(60, ts_start, ts_end)
    interval_dates = [
        time.strftime('%H:%M', time.gmtime(ts_end - (e * 60 * 60))) for e in
        range(24)]
    interval_balance = [e['building']['totalPowerConsumption'] - e['building'][
        'solarPowerOutput'] for e in data]
    # @TODO get colors to display
    # colors = ['green' if e < 0 else 'tomato' for e in interval_balance]

    figure = {
        'data': [
            {'x': interval_dates, 'y': interval_balance, 'type': 'bar'}
        ],
        'layout': {
            'title': 'Strombilanz der letzten 24 Stunden',
            'autosize': True,
            'xaxis': {'type': 'category'},
            'yaxis': {'title': 'Verbrauch (kw/h)'}
        }
    }

    return figure


def current_room_balance():
    """Calculates the current power consumption for all office rooms

    Returns:
        float: The current power consumption
    """
    data = query_live_data()

    return data['building']['totalPowerConsumption'] - data['building'][
        'powerConsumptionDataCenter']


def current_water_consumption():
    """Calculates the water consumption for the building from the last 10 minutes.

    Returns:
        float: The current water consumption in liters.
    """
    ts_end = int(time.time())
    ts_start = ts_end - (60 * 10)

    data = query_building(10, ts_start, ts_end)

    return data[0]['building']['waterConsumption']


def last_water_consumption():
    """Calculates the water consumption for the building from the 10 minutes before the last 10 minutes.

    Returns:
        float: The last water consumption in liters.
    """
    ts_end = int(time.time()) - (60 * 10)
    ts_start = ts_end - (60 * 10)

    data = query_building(10, ts_start, ts_end)

    return data[0]['building']['waterConsumption']


def build_layout(app):
    app.layout = html.Div(
        children=[
            html.H1(children="Codility Challenge 2021 - Group 6"),
            html.H1(children="Building Eco Dashboard"),
            html.Div(
                children=[
                    dcc.Graph(
                        id="power_balance",
                        figure=consumption_balance()),
                    html.H2(
                        children="Aktueller Stromverbrauch durch Büroräume"),
                    html.P(f"{current_room_balance():.2f} kw/h"),
                    html.H2(children="Aktueller Wasserverbrauch (10 min)"),
                    html.P(
                        f"{current_water_consumption():.2f} L ({('fallend', 'steigend')[current_water_consumption() > last_water_consumption()]})"),
                    html.H2(children="Raumübersicht"),
                    table.DataTable(
                        id='room_overview',
                        editable=False,
                        columns=[{"name": i, "id": i} for i in
                                 ['Raum', 'Problem(e)']],
                        data=live_room_check(),
                        style_cell={'textAlign': 'center'},
                        style_as_list_view=True,
                        style_data_conditional=[
                            {
                                'if': {
                                    'filter_query': '{Problem(e)} != "-"',
                                },
                                'backgroundColor': 'tomato',
                                'color': 'white'
                            },
                            {
                                'if': {
                                    'filter_query': '{Problem(e)} = "-"',
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


def error_layout(app, error_text):
    app.layout = html.Div(
        children=[
            html.H1(children="Codility Challenge 2021 - Group 6"),
            html.H1(children="Building Eco Dashboard"),
            html.P(children="Ein Fehler ist aufgetreten."),
            html.P(children=error_text)
        ]
    )
