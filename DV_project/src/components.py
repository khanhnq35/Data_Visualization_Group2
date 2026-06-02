from __future__ import annotations

from dash import dcc, html

from src.theme import GRAPH_CONFIG


def page_header(title: str, eyebrow: str, description: str) -> html.Div:
    return html.Div(
        className="page-header",
        children=[
            html.Div(eyebrow, className="eyebrow"),
            html.H1(title),
            html.P(description),
        ],
    )


def kpi_card(label: str, value_id: str, helper_id: str | None = None) -> html.Div:
    helper = html.Div(id=helper_id, className="kpi-helper") if helper_id else None
    children = [
        html.Div(label, className="kpi-label"),
        html.Div(id=value_id, className="kpi-value"),
    ]
    if helper is not None:
        children.append(helper)
    return html.Div(className="kpi-card", children=children)


def graph_card(graph_id: str, class_name: str = "") -> html.Div:
    classes = "chart-card"
    if class_name:
        classes = f"{classes} {class_name}"
    return html.Div(
        className=classes,
        children=dcc.Graph(
            id=graph_id,
            config=GRAPH_CONFIG,
            responsive=True,
            className="chart-graph",
        ),
    )


def empty_state(title: str, body: str) -> html.Div:
    return html.Div(
        className="empty-state",
        children=[
            html.H2(title),
            html.P(body),
        ],
    )
