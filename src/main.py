import dash

from layout import build_layout, error_layout

app = dash.Dash(__name__, eager_loading=True, title="ECO Dashboard")

try:
    build_layout(app)
except Exception as e:
    error_layout(app, str(e))

if __name__ == "__main__":
    app.run_server(debug=False)
