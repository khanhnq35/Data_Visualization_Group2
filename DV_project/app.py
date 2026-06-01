import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.SLATE],
)

app.layout = html.Div(
    style={"backgroundColor": "#0f172a", "minHeight": "100vh", "fontFamily": "Inter, sans-serif"},
    children=[
        # Simple top nav
        html.Nav(
            style={
                "backgroundColor": "#1e293b",
                "padding": "12px 24px",
                "display": "flex",
                "gap": "24px",
                "alignItems": "center",
                "borderBottom": "1px solid #334155",
            },
            children=[
                html.Span("⚽ FIFA World Cup Dashboard", style={"color": "#f1f5f9", "fontWeight": "700", "fontSize": "16px", "marginRight": "16px"}),
                dcc.Link("Overview",        href="/",                   style={"color": "#94a3b8", "textDecoration": "none", "fontSize": "14px"}),
                dcc.Link("Dominance",       href="/dominance",          style={"color": "#94a3b8", "textDecoration": "none", "fontSize": "14px"}),
                dcc.Link("Upsets",          href="/upsets",             style={"color": "#94a3b8", "textDecoration": "none", "fontSize": "14px"}),
                dcc.Link("Tournament Detail", href="/tournament-detail", style={"color": "#f1f5f9", "textDecoration": "none", "fontSize": "14px", "fontWeight": "600"}),
            ],
        ),
        dash.page_container,
    ],
)

if __name__ == "__main__":
    app.run(debug=True)
