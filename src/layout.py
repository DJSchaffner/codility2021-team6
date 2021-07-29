import dash_html_components as html

# https://databraineo.com/ki-training-resources/python/interaktive-dashboards-in-python-plotly-dash-tutorial/


def build_layout(app):
    app.layout = html.Div(
        children=[
            html.H1(children="Codility Challenge 2021 - Group 6"),
            html.Div(
            ),
        ]
    )