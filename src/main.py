import dash
from layout import build_layout

app = dash.Dash(__name__)

build_layout(app)


if __name__ == "__main__":
    app.run_server(debug=True)
