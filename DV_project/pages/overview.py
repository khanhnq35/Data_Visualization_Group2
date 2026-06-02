from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, dcc, html
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
                className="filter-panel",
                children=[
                    html.Div(
                        className="filter-block filter-wide",
                        children=[
                            html.Label("Year range", htmlFor="overview-year-range"),
                            dcc.RangeSlider(
                                id="overview-year-range",
                                min=int(years.min()),
                                max=int(years.max()),
                                value=[int(years.min()), int(years.max())],
                                marks={int(year): str(int(year)) for year in years[::3]},
                                step=None,
                                allowCross=False,
                                tooltip={"placement": "bottom", "always_visible": False},
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
                    graph_card("overview-scale-chart", "chart-large"),
                    graph_card("overview-avg-goals-chart"),
                ],
            ),
            html.Div(
                className="chart-grid single-column",
                children=graph_card("overview-champion-timeline", "chart-wide"),
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

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=("Teams", "Matches", "Goals"),
    )
    series = [
        ("teams", "Teams", COLORS["accent"]),
        ("matches_played", "Matches", COLORS["accent_2"]),
        ("goals_scored", "Goals", COLORS["success"]),
    ]
    for index, (column, label, color) in enumerate(series, start=1):
        fig.add_trace(
            go.Scatter(
                x=df["year"],
                y=df[column],
                mode="lines+markers",
                line={"width": 3, "color": color},
                marker={"size": 7},
                name=label,
                hovertemplate=f"Year: %{{x}}<br>{label}: %{{y:,}}<extra></extra>",
            ),
            row=index,
            col=1,
        )
        fig.update_yaxes(title_text=label, row=index, col=1)

    fig.update_layout(title="Tournament Scale by Year", showlegend=False)
    fig.update_xaxes(title_text="Year", row=3, col=1)
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
            line={"width": 3, "color": COLORS["accent_3"]},
            marker={"size": 8},
            hovertemplate="Year: %{x}<br>Avg goals/game: %{y:.2f}<extra></extra>",
            name="Avg goals/game",
        )
    )
    fig.add_hline(
        y=mean_value,
        line_dash="dot",
        line_color=COLORS["muted"],
        annotation_text=f"Selected mean: {mean_value:.2f}",
        annotation_position="bottom right",
    )
    fig.update_layout(title="Average Goals per Game")
    fig.update_xaxes(title="Year")
    fig.update_yaxes(title="Goals per game")
    return apply_chart_layout(fig, height=400)


def _champion_timeline_figure(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return empty_figure("Champion Timeline")

    marker_colors = [
        COLORS["success"] if host_won else COLORS["accent"]
        for host_won in df["host_won"].fillna(False).tolist()
    ]
    marker_sizes = (df["teams"].fillna(0).clip(lower=12) * 0.75).tolist()
    customdata = df[["host", "champion", "runner_up", "teams", "matches_played", "goals_scored"]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["year"],
            y=df["champion_norm"],
            mode="markers",
            marker={
                "size": marker_sizes,
                "color": marker_colors,
                "line": {"width": 1, "color": COLORS["surface"]},
                "opacity": 0.9,
            },
            customdata=customdata,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Year: %{x}<br>"
                "Host: %{customdata[0]}<br>"
                "Champion in raw data: %{customdata[1]}<br>"
                "Runner-up: %{customdata[2]}<br>"
                "Teams: %{customdata[3]:,}<br>"
                "Matches: %{customdata[4]:,}<br>"
                "Goals: %{customdata[5]:,}<extra></extra>"
            ),
            name="Champion",
        )
    )
    fig.update_layout(title="Champion Timeline", showlegend=False)
    fig.update_xaxes(title="Year")
    fig.update_yaxes(title="Champion")
    return apply_chart_layout(fig, height=440)


def register_callbacks(app) -> None:
    @app.callback(
        Output("overview-kpi-tournaments", "children"),
        Output("overview-kpi-teams", "children"),
        Output("overview-kpi-matches", "children"),
        Output("overview-kpi-goals", "children"),
        Output("overview-kpi-champions", "children"),
        Output("overview-scale-chart", "figure"),
        Output("overview-avg-goals-chart", "figure"),
        Output("overview-champion-timeline", "figure"),
        Input("overview-year-range", "value"),
        Input("overview-host-filter", "value"),
        Input("overview-champion-filter", "value"),
    )
    def update_overview(year_range, hosts, champions):
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
