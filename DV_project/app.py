from __future__ import annotations

from dash import Dash, Input, Output, dcc, html

from pages import dominance, overview, tournament, upsets
from src.theme import register_plotly_template


PAGES = [
    {
        "label": "Overview",
        "path": "/",
        "module": overview,
    },
    {
        "label": "Dominance",
        "path": "/dominance",
        "module": dominance,
    },
    {
        "label": "Upsets",
        "path": "/upsets",
        "module": upsets,
    },
    {
        "label": "Tournament Detail",
        "path": "/tournament",
        "module": tournament,
    },
]


def _nav_links() -> list[dcc.Link]:
    return [
        dcc.Link(page["label"], href=page["path"], className="nav-link")
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
        className="app-shell",
        children=[
            dcc.Location(id="url"),
            html.A("Skip to content", href="#page-content", className="skip-link"),
            html.Aside(
                className="sidebar",
                children=[
                    html.Div(
                        className="brand",
                        children=[
                            html.Div("WC", className="brand-mark"),
                            html.Div(
                                children=[
                                    html.Div("World Cup", className="brand-title"),
                                    html.Div("Data Dashboard", className="brand-subtitle"),
                                ]
                            ),
                        ],
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

    return app


app = create_app()
server = app.server


if __name__ == "__main__":
    app.run(debug=False)
