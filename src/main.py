import dash

import requests

from layout import build_layout, error_layout

app = dash.Dash(__name__)

try:
    build_layout(app)
except Exception as e:
    error_layout(app, str(e))

if __name__ == "__main__":
    app.run_server(debug=True)
