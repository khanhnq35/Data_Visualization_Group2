from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, dcc, html
from plotly.subplots import make_subplots

from src.components import graph_card, kpi_card, page_header
from src.data import load_world_cup_summary
from src.theme import COLORS, apply_chart_layout, empty_figure


def _options(values: pd.Series) -> list[dict[str, str]]:
    return [{"label": value, "value": value} for value in sorted(values.dropna().unique())]


def layout() -> html.Div:
    summary = load_world_cup_summary()
    years = summary["year"].astype(int)

    return html.Div(
        className="page-stack",
        children=[
            page_header(
                "Executive Overview",
                "FIFA World Cup",
                "Tournament scale, scoring trend, and champion history from 1930 to 2022.",
            ),
            html.Div(
                className="filter-panel overview-filter-panel",
                children=[
                    html.Div(
                        className="filter-block filter-wide",
                        children=[
                            html.Label("Year range: 1930 – 2022", id="overview-year-range-label", htmlFor="overview-year-range"),
                            dcc.RangeSlider(
                                id="overview-year-range",
                                min=int(years.min()),
                                max=int(years.max()),
                                value=[int(years.min()), int(years.max())],
                                marks={int(year): str(int(year)) for year in years[::3]},
                                step=None,
                                allowCross=False,
                                updatemode="mouseup",
                            ),
                        ],
                    ),
                    html.Div(
                        className="filter-block",
                        children=[
                            html.Label("Host", htmlFor="overview-host-filter"),
                            dcc.Dropdown(
                                id="overview-host-filter",
                                options=_options(summary["host"]),
                                multi=True,
                                placeholder="All hosts",
                            ),
                        ],
                    ),
                    html.Div(
                        className="filter-block",
                        children=[
                            html.Label("Champion", htmlFor="overview-champion-filter"),
                            dcc.Dropdown(
                                id="overview-champion-filter",
                                options=_options(summary["champion_norm"]),
                                multi=True,
                                placeholder="All champions",
                            ),
                        ],
                    ),
                    html.Div(
                        className="filter-block",
                        style={"justifyContent": "end", "height": "100%", "display": "flex", "flexDirection": "column"},
                        children=[
                            html.Button(
                                "Áp dụng bộ lọc",
                                id="overview-apply-btn",
                                style={
                                    "padding": "8px 16px",
                                    "background": "var(--accent)",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "6px",
                                    "cursor": "pointer",
                                    "fontSize": "13px",
                                    "fontWeight": "600",
                                    "height": "38px",
                                    "width": "100%",
                                    "minWidth": "110px"
                                },
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className="kpi-grid",
                children=[
                    kpi_card("Tournaments", "overview-kpi-tournaments"),
                    kpi_card("Team entries", "overview-kpi-teams"),
                    kpi_card("Matches", "overview-kpi-matches"),
                    kpi_card("Goals", "overview-kpi-goals"),
                    kpi_card("Champion nations", "overview-kpi-champions"),
                ],
            ),
            html.Div(
                className="chart-grid two-column",
                children=[
                    graph_card("overview-scale-chart", "chart-large", height="620px"),
                    graph_card("overview-avg-goals-chart", height="400px"),
                ],
            ),
            html.Div(
                className="chart-grid single-column",
                children=graph_card("overview-champion-timeline", "chart-wide", height="440px"),
            ),
        ],
    )


def _filter_summary(
    year_range: list[int] | None,
    hosts: list[str] | None,
    champions: list[str] | None,
) -> pd.DataFrame:
    df = load_world_cup_summary()
    if year_range and len(year_range) == 2:
        df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
    if hosts:
        df = df[df["host"].isin(hosts)]
    if champions:
        df = df[df["champion_norm"].isin(champions)]
    return df.sort_values("year")


def _format_int(value: int | float) -> str:
    if pd.isna(value):
        return "0"
    return f"{int(value):,}"


def _scale_figure(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return empty_figure("Tournament Scale by Year")

    df = df.copy()
    for col in ["teams", "matches_played", "goals_scored"]:
        pct = df[col].pct_change().multiply(100)
        df[f"{col}_pct"] = pct.apply(lambda val: f"+{val:.1f}%" if val > 0 else (f"{val:.1f}%" if val <= 0 else "—"))

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=("Số đội tham dự", "Số trận đấu", "Tổng bàn thắng"),
    )
    series = [
        ("teams", "Số đội", COLORS["accent"]),
        ("matches_played", "Số trận", COLORS["accent_2"]),
        ("goals_scored", "Bàn thắng", COLORS["success"]),
    ]
    for index, (column, label, color) in enumerate(series, start=1):
        marker_size = [12 if y == 1998 else 7 for y in df["year"]] if column == "teams" else 7
        fig.add_trace(
            go.Scatter(
                x=df["year"],
                y=df[column],
                mode="lines+markers",
                line={"width": 3, "color": color},
                marker={"size": marker_size},
                name=label,
                customdata=df[[f"{column}_pct"]].values,
                hovertemplate=f"Năm: %{{x}}<br>{label}: %{{y:,}}<br>Thay đổi: %{{customdata[0]}}<extra></extra>",
            ),
            row=index,
            col=1,
        )
        fig.update_yaxes(title_text=label, row=index, col=1)

    fig.update_layout(
        title="Quy mô World Cup theo năm (1930–2022)",
        showlegend=False,
    )
    fig.update_xaxes(title_text="Năm", row=3, col=1)

    return apply_chart_layout(fig, height=620)


def _avg_goals_figure(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return empty_figure("Average Goals per Game")

    mean_value = df["avg_goals_per_game"].mean()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["year"],
            y=df["avg_goals_per_game"],
            mode="lines+markers",
            line={"width": 3, "color": COLORS["accent"]},
            marker={"size": 8},
            hovertemplate="Year: %{x}<br>Avg goals/game: %{y:.2f}<extra></extra>",
            name="Avg goals/game",
        )
    )
    fig.add_hline(
        y=mean_value,
        line_dash="dot",
        line_color=COLORS["muted"],
        annotation_text=f"Trung bình: {mean_value:.2f}",
        annotation_position="bottom right",
    )

    fig.update_layout(title="Trung bình bàn thắng / trận")
    fig.update_xaxes(title="Năm")
    fig.update_yaxes(title="Bàn thắng/trận")
    return apply_chart_layout(fig, height=400)


def _champion_timeline_figure(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return empty_figure("Champion Timeline")

    customdata = df[["host", "champion", "runner_up", "teams", "matches_played", "goals_scored"]]

    # Tách 2 traces để có legend rõ ràng
    host_won_mask = df["host_won"].fillna(False)
    fig = go.Figure()

    for is_host_win, label, color, symbol in [
        (True,  "Chủ nhà vô địch", COLORS["success"], "star"),
        (False, "Đội khách vô địch", COLORS["accent"],  "circle"),
    ]:
        mask = host_won_mask == is_host_win
        sub = df[mask]
        if sub.empty:
            continue
        fig.add_trace(
            go.Scatter(
                x=sub["year"],
                y=sub["champion_norm"],
                mode="markers",
                marker={
                    "size": 12,
                    "color": color,
                    "symbol": symbol,
                    "line": {"width": 1, "color": COLORS["surface"]},
                    "opacity": 0.9,
                },
                customdata=sub[["host", "champion", "runner_up", "teams", "matches_played", "goals_scored"]].values,
                hovertemplate=(
                    "<b>%{y}</b> — %{x}<br>"
                    "Chủ nhà: %{customdata[0]}<br>"
                    "Á quân: %{customdata[2]}<br>"
                    "Số đội: %{customdata[3]:,} | Trận: %{customdata[4]:,} | Bàn: %{customdata[5]:,}"
                    "<extra></extra>"
                ),
                name=label,
            )
        )

    fig = apply_chart_layout(fig, height=440)
    fig.update_layout(
        title="Lịch sử nhà vô địch World Cup (1930–2022)",
        showlegend=True,
        margin={"l": 130, "r": 24, "t": 64, "b": 72},
    )
    fig.update_xaxes(title="Năm")
    fig.update_yaxes(
        title={
            "text": "Nhà vô địch",
            "standoff": 30
        },
        automargin=True
    )
    return fig


def register_callbacks(app) -> None:
    @app.callback(
        Output("overview-year-range-label", "children"),
        Input("overview-year-range", "value"),
    )
    def update_overview_label(year_range):
        y_min, y_max = (year_range[0], year_range[1]) if year_range and len(year_range) == 2 else (1930, 2022)
        return f"Year range: {y_min} – {y_max}"

    @app.callback(
        Output("overview-kpi-tournaments", "children"),
        Output("overview-kpi-teams", "children"),
        Output("overview-kpi-matches", "children"),
        Output("overview-kpi-goals", "children"),
        Output("overview-kpi-champions", "children"),
        Output("overview-scale-chart", "figure"),
        Output("overview-avg-goals-chart", "figure"),
        Output("overview-champion-timeline", "figure"),
        Input("overview-apply-btn", "n_clicks"),
        State("overview-year-range", "value"),
        State("overview-host-filter", "value"),
        State("overview-champion-filter", "value"),
    )
    def update_overview(n_clicks, year_range, hosts, champions):
        filtered = _filter_summary(year_range, hosts, champions)

        tournaments = len(filtered)
        team_entries = filtered["teams"].sum() if not filtered.empty else 0
        matches = filtered["matches_played"].sum() if not filtered.empty else 0
        goals = filtered["goals_scored"].sum() if not filtered.empty else 0
        champion_count = filtered["champion_norm"].nunique() if not filtered.empty else 0

        return (
            _format_int(tournaments),
            _format_int(team_entries),
            _format_int(matches),
            _format_int(goals),
            _format_int(champion_count),
            _scale_figure(filtered),
            _avg_goals_figure(filtered),
            _champion_timeline_figure(filtered),
        )
