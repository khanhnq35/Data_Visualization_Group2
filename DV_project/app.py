from __future__ import annotations

from dash import Dash, Input, Output, State, dcc, html

from pages import dominance, overview, tournament, upsets
from src.theme import register_plotly_template


PAGES = [
    {
        "label": "Overview",
        "path": "/",
        "module": overview,
        "icon": "📊",
    },
    {
        "label": "Dominance",
        "path": "/dominance",
        "module": dominance,
        "icon": "🏆",
    },
    {
        "label": "Upsets",
        "path": "/upsets",
        "module": upsets,
        "icon": "⚡",
    },
    {
        "label": "Tournament Detail",
        "path": "/tournament",
        "module": tournament,
        "icon": "📅",
    },
]


def _nav_links() -> list[dcc.Link]:
    return [
        dcc.Link(
            children=[
                html.Span(page["icon"], className="nav-icon"),
                html.Span(page["label"], className="nav-text"),
            ],
            href=page["path"],
            className="nav-link",
        )
        for page in PAGES
    ]


def create_app() -> Dash:
    register_plotly_template()
    app = Dash(
        __name__,
        suppress_callback_exceptions=True,
        title="World Cup Dashboard",
        assets_folder="assets",
    )

    app.layout = html.Div(
        id="app-shell",
        className="app-shell",
        children=[
            dcc.Store(id="sidebar-collapsed-store", storage_type="local", data=False),
            dcc.Location(id="url"),
            html.A("Skip to content", href="#page-content", className="skip-link"),
            html.Aside(
                id="sidebar",
                className="sidebar",
                children=[
                    html.Div(
                        className="brand",
                        children=[
                            html.Div("WC", className="brand-mark"),
                            html.Div(
                                className="brand-text",
                                children=[
                                    html.Div("World Cup", className="brand-title"),
                                    html.Div("Data Dashboard", className="brand-subtitle"),
                                ]
                            ),
                        ],
                    ),
                    html.Button(
                        "◀",
                        id="sidebar-toggle",
                        className="sidebar-toggle-btn",
                        n_clicks=0,
                    ),
                    html.Nav(_nav_links(), className="nav-list", **{"aria-label": "Dashboard pages"}),
                ],
            ),
            html.Main(id="page-content", className="content", tabIndex=-1),
        ],
    )

    for page in PAGES:
        page["module"].register_callbacks(app)

    @app.callback(Output("page-content", "children"), Input("url", "pathname"))
    def render_page(pathname: str | None):
        path = pathname or "/"
        for page in PAGES:
            if page["path"] == path:
                return page["module"].layout()
        return overview.layout()

    @app.callback(
        Output("app-shell", "style"),
        Output("sidebar", "className"),
        Output("sidebar-toggle", "children"),
        Output("sidebar-collapsed-store", "data"),
        Input("sidebar-toggle", "n_clicks"),
        State("sidebar-collapsed-store", "data"),
    )
    def toggle_sidebar(n_clicks, is_collapsed):
        collapsed = is_collapsed or False
        if n_clicks and n_clicks > 0:
            collapsed = not collapsed
        
        if collapsed:
            shell_style = {"gridTemplateColumns": "80px minmax(0, 1fr)"}
            sidebar_class = "sidebar collapsed"
            toggle_text = "▶"
        else:
            shell_style = {"gridTemplateColumns": "260px minmax(0, 1fr)"}
            sidebar_class = "sidebar"
            toggle_text = "◀"
            
        return shell_style, sidebar_class, toggle_text, collapsed

    return app


app = create_app()
server = app.server


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=False, port=port)
