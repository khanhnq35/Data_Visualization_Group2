from __future__ import annotations

from dash import html

from src.components import empty_state, page_header


def layout() -> html.Div:
    return html.Div(
        className="page-stack",
        children=[
            page_header(
                "Tournament Detail",
                "Year template",
                "Single-tournament standings, goal profile, and top-four highlight cards.",
            ),
            empty_state(
                "Pending page merge",
                "Use this route for the tournament detail page. Component IDs should use the tournament- prefix.",
            ),
        ],
    )


def register_callbacks(app) -> None:
    return None
