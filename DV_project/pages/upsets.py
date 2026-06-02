from __future__ import annotations

import pandas as pd
import plotly.express as px
from dash import Input, Output, ctx, dcc, html

from src.components import graph_card, page_header
from src.data import load_upsets_data
from src.theme import COLORS, apply_chart_layout, empty_figure


COLOR_UPSET = "#f97316"    # orange — CVD-safe thay vì đỏ
COLOR_NORMAL = "#94a3b8"  # grey
COLOR_HOME = "#1d4ed8"    # blue — CVD-safe
COLOR_AWAY = "#f97316"    # orange — CVD-safe thay vì đỏ
COLOR_DRAW = "#cbd5e1"    # grey nhạt


def _option_list(values: pd.Series) -> list[dict[str, str]]:
    return [{"label": value, "value": value} for value in sorted(values.dropna().unique())]


def _is_true(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["true", "yes", "1"])


def layout() -> html.Div:
    df = load_upsets_data()
    year_min = int(df["year"].min())
    year_max = int(df["year"].max())
    default_min = max(2000, year_min)

    return html.Div(
        className="page-stack",
        children=[
            page_header(
                "Upsets & Competitiveness",
                "International matches",
                "Rank gaps, score differences, neutral venues, and high-upset matches since 1993.",
            ),
            html.Div(
                className="filter-panel upsets-filter-panel",
                children=[
                    html.Div(
                        className="filter-block filter-wide",
                        children=[
                            html.Label("Year range", htmlFor="upsets-year-slider"),
                            dcc.RangeSlider(
                                id="upsets-year-slider",
                                min=year_min,
                                max=year_max,
                                step=1,
                                value=[default_min, year_max],
                                marks={year: str(year) for year in range(year_min, year_max + 1, 4)},
                                allowCross=False,
                                tooltip={"placement": "bottom", "always_visible": False},
                            ),
                        ],
                    ),
                    html.Div(
                        className="filter-block",
                        children=[
                            html.Label("Tournament", htmlFor="upsets-tournament-dropdown"),
                            dcc.Dropdown(
                                id="upsets-tournament-dropdown",
                                options=_option_list(df["tournament"]),
                                placeholder="All tournaments",
                            ),
                        ],
                    ),
                    html.Div(
                        className="filter-block",
                        children=[
                            html.Label("Team", htmlFor="upsets-team-dropdown"),
                            dcc.Dropdown(
                                id="upsets-team-dropdown",
                                options=_option_list(pd.concat([df["home_team"], df["away_team"]])),
                                placeholder="All teams",
                            ),
                        ],
                    ),
                    html.Div(
                        className="filter-block",
                        children=[
                            html.Label("Continent", htmlFor="upsets-continent-dropdown"),
                            dcc.Dropdown(
                                id="upsets-continent-dropdown",
                                options=_option_list(
                                    pd.concat([df["home_team_continent"], df["away_team_continent"]])
                                ),
                                placeholder="All continents",
                            ),
                        ],
                    ),
                    html.Div(
                        className="filter-block",
                        children=[
                            html.Label("Match type", htmlFor="upsets-match-type-dropdown"),
                            dcc.Dropdown(
                                id="upsets-match-type-dropdown",
                                options=[
                                    {"label": "All", "value": "All"},
                                    {"label": "Shoot-out", "value": "Shootout"},
                                    {"label": "Neutral location", "value": "Neutral"},
                                ],
                                value="All",
                                clearable=False,
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className="insight-card",
                children=[
                    "Dữ liệu ",
                    html.Strong("23,921 trận quốc tế"),
                    " cho thấy bóng đá phức tạp hơn bất kỳ công thức nào. "
                    "Đội được xếp hạng thấp hơn vẫn thắng thường xuyên hơn bạn nghĩ — "
                    "đây là bằng chứng rằng ",
                    html.Strong("bảng xếp hạng FIFA không quyết định tất cả"),
                    ".",
                ],
            ),
            html.Div(id="upsets-kpi-row", className="kpi-grid upsets-kpi-grid"),
            html.Div(
                className="chart-grid upsets-chart-grid",
                children=[
                    graph_card("upsets-scatter-plot", "chart-large"),
                    graph_card("upsets-bar-chart"),
                    graph_card("upsets-stacked-bar"),
                ],
            ),
            html.Div(id="upsets-detail-container", className="upsets-detail-panel"),
        ],
    )


def _filter_matches(
    year_range: list[int] | None,
    tournament: str | None,
    team: str | None,
    continent: str | None,
    match_type: str | None,
) -> pd.DataFrame:
    df = load_upsets_data()
    if year_range and len(year_range) == 2:
        df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
    if tournament:
        df = df[df["tournament"] == tournament]
    if team:
        df = df[(df["home_team"] == team) | (df["away_team"] == team)]
    if continent:
        df = df[
            (df["home_team_continent"] == continent)
            | (df["away_team_continent"] == continent)
        ]
    if match_type == "Shootout":
        df = df[_is_true(df["shoot_out"])]
    elif match_type == "Neutral":
        df = df[_is_true(df["neutral_location"])]
    return df.copy()


def _filtered_options(
    year_range: list[int] | None,
    tournament: str | None,
    team: str | None,
    continent: str | None,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    df = load_upsets_data()
    if year_range and len(year_range) == 2:
        df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

    tournament_df = df.copy()
    if team:
        tournament_df = tournament_df[
            (tournament_df["home_team"] == team) | (tournament_df["away_team"] == team)
        ]
    if continent:
        tournament_df = tournament_df[
            (tournament_df["home_team_continent"] == continent)
            | (tournament_df["away_team_continent"] == continent)
        ]

    team_df = df.copy()
    if tournament:
        team_df = team_df[team_df["tournament"] == tournament]
    if continent:
        team_df = team_df[
            (team_df["home_team_continent"] == continent)
            | (team_df["away_team_continent"] == continent)
        ]

    continent_df = df.copy()
    if tournament:
        continent_df = continent_df[continent_df["tournament"] == tournament]
    if team:
        continent_df = continent_df[
            (continent_df["home_team"] == team) | (continent_df["away_team"] == team)
        ]

    return (
        _option_list(tournament_df["tournament"]),
        _option_list(pd.concat([team_df["home_team"], team_df["away_team"]])),
        _option_list(
            pd.concat([continent_df["home_team_continent"], continent_df["away_team_continent"]])
        ),
    )


def _kpi_card(label: str, value: str, helper: str | None = None) -> html.Div:
    children = [
        html.Div(label, className="kpi-label"),
        html.Div(value, className="kpi-value"),
    ]
    if helper:
        children.append(html.Div(helper, className="kpi-helper"))
    return html.Div(className="kpi-card", children=children)


def _format_int(value: int | float) -> str:
    return f"{int(value):,}"


def _build_kpis(df: pd.DataFrame) -> list[html.Div]:
    total_matches = len(df)
    if total_matches == 0:
        return [
            _kpi_card("Matches", "0"),
            _kpi_card("Upsets", "0"),
            _kpi_card("Home win rate", "0%"),
            _kpi_card("Draw rate", "0%"),
            _kpi_card("Away win rate", "0%"),
            _kpi_card("Neutral matches", "0"),
        ]

    home_wins = int((df["home_team_score"] > df["away_team_score"]).sum())
    draws = int((df["home_team_score"] == df["away_team_score"]).sum())
    away_wins = total_matches - home_wins - draws
    upsets = int(df["is_upset"].sum())
    neutral_matches = int(_is_true(df["neutral_location"]).sum())
    shootout_matches = int(_is_true(df["shoot_out"]).sum())

    return [
        _kpi_card("Matches", _format_int(total_matches)),
        _kpi_card("Upsets", _format_int(upsets), f"{upsets / total_matches:.1%} of matches"),
        _kpi_card("Home win rate", f"{home_wins / total_matches:.1%}"),
        _kpi_card("Draw rate", f"{draws / total_matches:.1%}"),
        _kpi_card("Away win rate", f"{away_wins / total_matches:.1%}"),
        _kpi_card("Neutral matches", _format_int(neutral_matches), f"{shootout_matches:,} shoot-outs"),
    ]


def _custom_data_columns() -> list[str]:
    return [
        "date_str",
        "tournament",
        "home_team",
        "home_team_fifa_rank",
        "home_team_score",
        "away_team_score",
        "away_team_fifa_rank",
        "away_team",
        "upset_rank_gap",
    ]


def _scatter_figure(df: pd.DataFrame):
    if df.empty:
        return empty_figure("Rank Gap vs Goal Difference")

    fig = px.scatter(
        df,
        x="rank_gap",
        y="home_goal_diff",
        color="is_upset",
        color_discrete_map={True: COLOR_UPSET, False: COLOR_NORMAL},
        custom_data=_custom_data_columns(),
        labels={"rank_gap": "Chênh lệch hạng FIFA", "home_goal_diff": "Chênh lệch bàn thắng"},
        title="Hạng FIFA và kết quả trận đấu",
    )
    fig.update_traces(
        marker={"size": 6, "line": {"width": 0.5, "color": "white"}, "opacity": 0.6},
        hovertemplate=(
            "<b>%{customdata[0]} | %{customdata[1]}</b><br>"
            "%{customdata[2]} (Hạng %{customdata[3]}) "
            "<b>%{customdata[4]} - %{customdata[5]}</b> "
            "%{customdata[7]} (Hạng %{customdata[6]})<br>"
            "Chênh lệch hạng: %{x}<br>Chênh lệch bàn: %{y}<extra></extra>"
        ),
    )
    fig.for_each_trace(
        lambda trace: trace.update(
            name="Upset — Đội yếu thắng", opacity=0.9,
            marker={"size": 7, "line": {"width": 0.5, "color": "white"}},
        ) if trace.name == "True" else trace.update(
            name="Kết quả thông thường", opacity=0.3,
        )
    )
    fig.add_hline(y=0, line_dash="dash", line_color=COLORS["border"], opacity=0.8)
    fig.add_vline(x=0, line_dash="dash", line_color=COLORS["border"], opacity=0.8)

    # Annotation vùng quadrant
    if not df.empty:
        max_rg = float(df["rank_gap"].quantile(0.92))
        max_gd = float(df["home_goal_diff"].quantile(0.88))
        min_gd = float(df["home_goal_diff"].quantile(0.08))
        fig.add_annotation(
            x=max_rg * 0.65, y=max_gd * 0.7,
            text="Đội yếu hơn nhưng THẮNG<br>(upset!)",
            showarrow=False,
            font={"size": 9, "color": COLOR_UPSET},
            align="center",
        )
        fig.add_annotation(
            x=max_rg * 0.65, y=min_gd * 0.65,
            text="Đội yếu hơn, thua nhiều<br>(dự đoán được)",
            showarrow=False,
            font={"size": 9, "color": COLORS["muted"]},
            align="center",
        )

    return apply_chart_layout(fig, height=480)


def _top_upsets_figure(df: pd.DataFrame):
    upsets_df = df[df["is_upset"]].sort_values("upset_rank_gap", ascending=False).head(5)
    if upsets_df.empty:
        return empty_figure("Top 5 upset lớn nhất theo chênh lệch hạng", "Không có upset. Thử mở rộng bộ lọc.")

    fig = px.bar(
        upsets_df,
        x="upset_rank_gap",
        y="match_short_label",
        orientation="h",
        text="match_short_label",
        custom_data=_custom_data_columns(),
        color_discrete_sequence=[COLOR_UPSET],
        title="Top 5 upset lớn nhất theo chênh lệch hạng",
    )
    fig.update_traces(
        textposition="inside",
        insidetextanchor="start",
        textfont={"size": 12, "color": "white"},
        hovertemplate=(
            "<b>%{customdata[0]} | %{customdata[1]}</b><br>"
            "%{customdata[2]} (Hạng %{customdata[3]}) "
            "<b>%{customdata[4]} - %{customdata[5]}</b> "
            "%{customdata[7]} (Hạng %{customdata[6]})<br>"
            "Chênh lệch hạng: %{customdata[8]}<extra></extra>"
        ),
    )
    fig.update_yaxes(title="", categoryorder="total ascending", showticklabels=False)
    fig.update_xaxes(title="Chênh lệch hạng FIFA", showgrid=True, gridcolor="#e2e8f0")
    return apply_chart_layout(fig, height=360)


def _neutral_result_figure(df: pd.DataFrame):
    if df.empty:
        return empty_figure("Result by Neutral Location")

    df = df.copy()
    df["match_result"] = "Draw"
    df.loc[df["home_team_score"] > df["away_team_score"], "match_result"] = "Home Win"
    df.loc[df["home_team_score"] < df["away_team_score"], "match_result"] = "Away Win"
    df["neutral_label"] = _is_true(df["neutral_location"]).map(
        {False: "Home/Away", True: "Neutral Location"}
    )

    counts = df.groupby(["neutral_label", "match_result"]).size().reset_index(name="count")
    totals = counts.groupby("neutral_label")["count"].transform("sum")
    counts["percentage"] = (counts["count"] / totals) * 100
    counts["text_label"] = counts["percentage"].round(1).astype(str) + "%"

    fig = px.bar(
        counts,
        x="neutral_label",
        y="percentage",
        color="match_result",
        text="text_label",
        custom_data=["match_result", "count"],
        color_discrete_map={"Home Win": COLOR_HOME, "Away Win": COLOR_AWAY, "Draw": COLOR_DRAW},
        labels={"neutral_label": "", "percentage": "Tỷ lệ (%)", "match_result": "Kết quả"},
        title="Kết quả trận theo loại địa điểm thi đấu",
    )
    fig.update_traces(
        textfont={"color": "white"},
        hovertemplate=(
            "Địa điểm: %{x}<br>Kết quả: %{customdata[0]}<br>"
            "Tỷ lệ: %{y:.1f}%<br>Số trận: %{customdata[1]}<extra></extra>"
        ),
    )
    for _, row in counts.groupby("neutral_label", as_index=False)["count"].sum().iterrows():
        fig.add_annotation(
            x=row["neutral_label"],
            y=100,
            yshift=12,
            text=f"Tổng: {row['count']:,} trận",
            showarrow=False,
            font={"size": 11, "color": COLORS["muted"]},
        )
    fig.update_yaxes(title="", visible=False, range=[0, 110])
    return apply_chart_layout(fig, height=360)


def _default_detail() -> html.Div:
    return html.Div(
        children=[
            html.Div("Selected match details", className="upsets-detail-title"),
            html.Div("Click a match in the scatter plot or top upsets chart.", className="upsets-detail-body"),
        ]
    )


def register_callbacks(app) -> None:
    @app.callback(
        Output("upsets-tournament-dropdown", "options"),
        Output("upsets-team-dropdown", "options"),
        Output("upsets-continent-dropdown", "options"),
        Input("upsets-year-slider", "value"),
        Input("upsets-tournament-dropdown", "value"),
        Input("upsets-team-dropdown", "value"),
        Input("upsets-continent-dropdown", "value"),
    )
    def update_dropdown_options(year_range, tournament, team, continent):
        return _filtered_options(year_range, tournament, team, continent)

    @app.callback(
        Output("upsets-scatter-plot", "figure"),
        Output("upsets-bar-chart", "figure"),
        Output("upsets-stacked-bar", "figure"),
        Output("upsets-kpi-row", "children"),
        Input("upsets-year-slider", "value"),
        Input("upsets-tournament-dropdown", "value"),
        Input("upsets-team-dropdown", "value"),
        Input("upsets-continent-dropdown", "value"),
        Input("upsets-match-type-dropdown", "value"),
    )
    def update_graphs(year_range, tournament, team, continent, match_type):
        filtered = _filter_matches(year_range, tournament, team, continent, match_type)
        return (
            _scatter_figure(filtered),
            _top_upsets_figure(filtered),
            _neutral_result_figure(filtered),
            _build_kpis(filtered),
        )

    @app.callback(
        Output("upsets-detail-container", "children"),
        Input("upsets-scatter-plot", "clickData"),
        Input("upsets-bar-chart", "clickData"),
    )
    def display_click_data(scatter_click, bar_click):
        trigger_id = ctx.triggered_id
        click_data = scatter_click if trigger_id == "upsets-scatter-plot" else bar_click
        if not click_data:
            return _default_detail()

        date_str, tournament, home_team, home_rank, home_score, away_score, away_rank, away_team, _ = (
            click_data["points"][0]["customdata"]
        )
        return html.Div(
            children=[
                html.Div("Selected match details", className="upsets-detail-title"),
                html.Div(
                    [
                        html.Span(f"{tournament} ({date_str})", className="upsets-detail-meta"),
                        html.Span(f"{home_team} (Rank {home_rank})"),
                        html.Span(f" {home_score} - {away_score} ", className="upsets-detail-score"),
                        html.Span(f"{away_team} (Rank {away_rank})"),
                    ],
                    className="upsets-detail-body",
                ),
            ]
        )
