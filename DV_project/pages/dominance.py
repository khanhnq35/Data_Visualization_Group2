from __future__ import annotations

from dash import html

from src.components import empty_state, page_header


def layout() -> html.Div:
    return html.Div(
        className="page-stack",
        children=[
            page_header(
                "Dominance",
                "World Cup success",
                "Titles, top finishes, and regional concentration across tournament history.",
            ),
            empty_state(
                "Pending page merge",
                "Use this route for the dominance page module. Component IDs should use the dominance- prefix.",
            ),
        ],
    )


def register_callbacks(app) -> None:
    return None
