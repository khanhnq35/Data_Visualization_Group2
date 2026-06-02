from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio


COLORS = {
    "background": "#f6f8fb",
    "surface": "#ffffff",
    "surface_alt": "#eef4f5",
    "text": "#172026",
    "muted": "#64727d",
    "border": "#d8e0e6",
    "accent": "#007c89",
    "accent_2": "#d98324",
    "accent_3": "#c44536",
    "success": "#2f855a",
    "warning": "#b7791f",
    "nav": "#101820",
}

CHART_COLORS = [
    COLORS["accent"],
    COLORS["accent_2"],
    COLORS["success"],
    COLORS["accent_3"],
    "#6f5f90",
    "#4a6f86",
    "#8a7a1f",
]

GRAPH_CONFIG = {
    "displaylogo": False,
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
    "responsive": True,
}


def register_plotly_template() -> None:
    pio.templates["worldcup"] = go.layout.Template(
        layout=go.Layout(
            font={"family": "Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif"},
            colorway=CHART_COLORS,
            paper_bgcolor=COLORS["surface"],
            plot_bgcolor=COLORS["surface"],
            title={"font": {"size": 18, "color": COLORS["text"]}},
            xaxis={
                "gridcolor": "#e8eef2",
                "linecolor": COLORS["border"],
                "zerolinecolor": COLORS["border"],
                "tickfont": {"color": COLORS["muted"]},
                "title": {"font": {"color": COLORS["muted"]}},
            },
            yaxis={
                "gridcolor": "#e8eef2",
                "linecolor": COLORS["border"],
                "zerolinecolor": COLORS["border"],
                "tickfont": {"color": COLORS["muted"]},
                "title": {"font": {"color": COLORS["muted"]}},
            },
            legend={
                "orientation": "h",
                "yanchor": "top",
                "y": -0.18,
                "xanchor": "center",
                "x": 0.5,
            },
            margin={"l": 48, "r": 24, "t": 64, "b": 72},
        )
    )
    pio.templates.default = "worldcup"


def ensure_plotly_template() -> None:
    if "worldcup" not in pio.templates:
        register_plotly_template()


def apply_chart_layout(fig: go.Figure, height: int = 380) -> go.Figure:
    ensure_plotly_template()
    fig.update_layout(
        template="worldcup",
        height=height,
        hovermode="closest",
        margin={"l": 48, "r": 24, "t": 64, "b": 72},
    )
    return fig


def empty_figure(title: str, message: str = "No data for the selected filters.") -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font={"size": 14, "color": COLORS["muted"]},
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(title=title)
    return apply_chart_layout(fig)
