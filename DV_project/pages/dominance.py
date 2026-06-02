from __future__ import annotations

import glob
import os
import pandas as pd
from dash import dcc, html, dash_table, Input, Output

from src.components import graph_card, kpi_card, page_header
from src.theme import COLORS, apply_chart_layout, empty_figure


# ── Data Loading & Processing ──────────────────────────────────────────────────

# Path setups (matches the structure of the repository)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "Data")
ARCHIVE_DIR = os.path.join(DATA_DIR, "archive")
SUMMARY_PATH = os.path.join(ARCHIVE_DIR, "FIFA - World Cup Summary.csv")
MATCHES_PATH = os.path.join(DATA_DIR, "international_matches.csv")

SUMMARY_DF = pd.read_csv(SUMMARY_PATH)
SUMMARY_DF.columns = [c.strip() for c in SUMMARY_DF.columns]
SUMMARY_DF["YEAR"] = pd.to_numeric(SUMMARY_DF["YEAR"], errors="coerce").astype(int)

AVAILABLE_FILES = sorted(glob.glob(os.path.join(ARCHIVE_DIR, "FIFA - [0-9]*.csv")))
AVAILABLE_YEARS = sorted(
    [
        int(os.path.basename(path).replace("FIFA - ", "").replace(".csv", ""))
        for path in AVAILABLE_FILES
    ]
)

YEAR_SLIDER_MARKS = {
    year: {
        "label": str(year),
        "style": {"color": "#64727d", "fontSize": "11px", "whiteSpace": "nowrap"},
    }
    for year in AVAILABLE_YEARS
    if year == min(AVAILABLE_YEARS)
    or year == max(AVAILABLE_YEARS)
    or year % 20 == 0 or year == 2022
}

FALLBACK_TEAM_CONTINENT = {
    "Bulgaria**": "Europe",
    "Czechoslovakia": "Europe",
    "Dutch East Indies": "Asia",
    "East Germany": "Europe",
    "FR Yugoslavia": "Europe",
    "Iran": "Asia",
    "Israel*": "Asia",
    "Ivory Coast": "Africa",
    "North Korea": "Asia",
    "Serbia and Montenegro": "Europe",
    "South Korea": "Asia",
    "Soviet Union": "Europe",
    "United States": "North America",
    "West Germany": "Europe",
    "Yugoslavia": "Europe",
    "Zaire": "Africa",
}


def _pos_group(position):
    if pd.isna(position):
        return "Other"
    if position == 1:
        return "Champion"
    if position <= 4:
        return "Top 4"
    if position <= 8:
        return "Top 8"
    return "Other"


def _load_team_continent_mapping():
    if not os.path.exists(MATCHES_PATH):
        return {}

    matches = pd.read_csv(MATCHES_PATH)
    matches.columns = [c.strip() for c in matches.columns]
    teams = []
    if "home_team" in matches.columns and "home_team_continent" in matches.columns:
        teams.append(matches[["home_team", "home_team_continent"]].rename(columns={"home_team": "team", "home_team_continent": "continent"}))
    if "away_team" in matches.columns and "away_team_continent" in matches.columns:
        teams.append(matches[["away_team", "away_team_continent"]].rename(columns={"away_team": "team", "away_team_continent": "continent"}))
    if not teams:
        return {}

    team_continent = pd.concat(teams, ignore_index=True)
    team_continent = team_continent.dropna(subset=["team", "continent"])
    result = {}
    for team, group in team_continent.groupby("team"):
        counts = group["continent"].value_counts()
        result[team] = counts.index[0]

    for team, continent in FALLBACK_TEAM_CONTINENT.items():
        if team not in result:
            result[team] = continent

    return result


TEAM_CONTINENT = _load_team_continent_mapping()


def _load_all_standings():
    archive_frames = []
    for file_path in AVAILABLE_FILES:
        year = int(os.path.basename(file_path).replace("FIFA - ", "").replace(".csv", ""))
        df = pd.read_csv(file_path)
        df.columns = [c.strip() for c in df.columns]
        df["Year"] = year
        df["Position"] = pd.to_numeric(df.get("Position", pd.Series()), errors="coerce")
        df["Goals For"] = pd.to_numeric(df.get("Goals For", pd.Series()), errors="coerce")
        df["Points"] = pd.to_numeric(df.get("Points", pd.Series()), errors="coerce")
        df["position_group"] = df["Position"].apply(_pos_group)
        df["continent"] = df["Team"].map(TEAM_CONTINENT).fillna("Unknown")
        archive_frames.append(df)
    return pd.concat(archive_frames, ignore_index=True)


ALL_STANDINGS = _load_all_standings()
ALL_STANDINGS = ALL_STANDINGS.sort_values(["Year", "Position"])

TEAM_OPTIONS = sorted(ALL_STANDINGS["Team"].dropna().unique())
CONTINENT_OPTIONS = sorted(ALL_STANDINGS["continent"].dropna().unique())
POSITION_OPTIONS = ["Champion", "Top 4", "Top 8", "Other"]


# ── Page Layout ────────────────────────────────────────────────────────────────

def layout() -> html.Div:
    return html.Div(
        className="page-stack",
        children=[
            page_header(
                "Dominance",
                "World Cup success",
                "Explore historical World Cup dominance patterns by teams and continents.",
            ),
            html.Div(
                className="filter-panel",
                style={"gridTemplateColumns": "minmax(280px, 1.4fr) repeat(3, minmax(160px, 0.7fr))"},
                children=[
                    html.Div(
                        className="filter-block",
                        children=[
                            html.Label("Year range", htmlFor="dominance-year-range"),
                            dcc.RangeSlider(
                                id="dominance-year-range",
                                min=min(AVAILABLE_YEARS),
                                max=max(AVAILABLE_YEARS),
                                step=4,
                                marks=YEAR_SLIDER_MARKS,
                                value=[min(AVAILABLE_YEARS), max(AVAILABLE_YEARS)],
                                allowCross=False,
                                tooltip={"placement": "bottom", "always_visible": False},
                            ),
                        ],
                    ),
                    html.Div(
                        className="filter-block",
                        children=[
                            html.Label("Team filter", htmlFor="dominance-team-filter"),
                            dcc.Dropdown(
                                id="dominance-team-filter",
                                options=[{"label": team, "value": team} for team in TEAM_OPTIONS],
                                value=[],
                                multi=True,
                                placeholder="All teams",
                            ),
                        ],
                    ),
                    html.Div(
                        className="filter-block",
                        children=[
                            html.Label("Continent filter", htmlFor="dominance-continent-filter"),
                            dcc.Dropdown(
                                id="dominance-continent-filter",
                                options=[{"label": cont, "value": cont} for cont in CONTINENT_OPTIONS],
                                value=CONTINENT_OPTIONS,
                                multi=True,
                                placeholder="All continents",
                            ),
                        ],
                    ),
                    html.Div(
                        className="filter-block",
                        children=[
                            html.Label("Position group", htmlFor="dominance-position-filter"),
                            dcc.Dropdown(
                                id="dominance-position-filter",
                                options=[{"label": group, "value": group} for group in POSITION_OPTIONS],
                                value=POSITION_OPTIONS,
                                multi=True,
                                placeholder="All groups",
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className="kpi-grid",
                style={"gridTemplateColumns": "repeat(4, minmax(140px, 1fr))"},
                children=[
                    kpi_card("Tournaments", "dominance-kpi-tournaments"),
                    kpi_card("Teams", "dominance-kpi-teams"),
                    kpi_card("Titles", "dominance-kpi-titles"),
                    kpi_card("Top 4 Finishes", "dominance-kpi-top4"),
                ],
            ),
            html.Div(
                className="chart-grid two-column",
                children=[
                    graph_card("dominance-champion-bar"),
                    graph_card("dominance-top4-by-continent"),
                ],
            ),
            html.Div(
                className="chart-grid single-column",
                children=[
                    graph_card("dominance-goals-for-chart", "chart-wide"),
                ],
            ),
            html.Div(
                className="chart-card",
                style={"padding": "24px"},
                children=[
                    html.H3("Team Dominance Summary", style={"margin": "0 0 16px 0", "fontSize": "16px", "color": COLORS["text"]}),
                    dash_table.DataTable(
                        id="dominance-summary-table",
                        columns=[
                            {"name": label, "id": key}
                            for label, key in [
                                ("Team", "Team"),
                                ("Continent", "continent"),
                                ("Appearances", "appearances"),
                                ("Championships", "championship_count"),
                                ("Top 4", "top4_count"),
                                ("Best Position", "best_position"),
                                ("Goals For", "total_goals_for"),
                                ("Points", "total_points"),
                            ]
                        ],
                        sort_action="native",
                        page_size=15,
                        style_table={"overflowX": "auto"},
                        style_header={
                            "backgroundColor": "#f6f8fb",
                            "color": "#172026",
                            "fontWeight": "600",
                            "fontSize": "13px",
                            "border": "1px solid #d8e0e6",
                            "textTransform": "uppercase",
                            "letterSpacing": "0.03em",
                        },
                        style_data={
                            "backgroundColor": "#ffffff",
                            "color": "#172026",
                            "fontSize": "13px",
                            "border": "1px solid #d8e0e6",
                        },
                        style_data_conditional=[
                            {"if": {"row_index": "odd"}, "backgroundColor": "#f8fafc"},
                            {"if": {"filter_query": "{best_position} = 1"}, "color": COLORS["accent_2"], "fontWeight": "700"},
                        ],
                    )
                ],
            ),
        ],
    )


# ── Callbacks Registration ─────────────────────────────────────────────────────

def register_callbacks(app) -> None:
    @app.callback(
        Output("dominance-kpi-tournaments", "children"),
        Output("dominance-kpi-teams", "children"),
        Output("dominance-kpi-titles", "children"),
        Output("dominance-kpi-top4", "children"),
        Output("dominance-champion-bar", "figure"),
        Output("dominance-top4-by-continent", "figure"),
        Output("dominance-goals-for-chart", "figure"),
        Output("dominance-summary-table", "data"),
        Input("dominance-year-range", "value"),
        Input("dominance-team-filter", "value"),
        Input("dominance-continent-filter", "value"),
        Input("dominance-position-filter", "value"),
    )
    def update_dominance(year_range, selected_teams, selected_continents, selected_positions):
        if not selected_continents:
            selected_continents = CONTINENT_OPTIONS
        if not selected_positions:
            selected_positions = POSITION_OPTIONS

        year_min, year_max = year_range
        filtered = ALL_STANDINGS[
            (ALL_STANDINGS["Year"] >= year_min)
            & (ALL_STANDINGS["Year"] <= year_max)
            & (ALL_STANDINGS["continent"].isin(selected_continents))
            & (ALL_STANDINGS["position_group"].isin(selected_positions))
        ]

        if selected_teams:
            filtered = filtered[filtered["Team"].isin(selected_teams)]

        tournaments = sorted(filtered["Year"].unique())
        team_count = filtered["Team"].nunique()
        title_count = int((filtered["Position"] == 1).sum())
        top4_count = int((filtered["Position"] <= 4).sum())

        team_summary = filtered.groupby("Team").agg(
            appearances=("Year", "nunique"),
            championship_count=("Position", lambda s: int((s == 1).sum())),
            top4_count=("Position", lambda s: int((s <= 4).sum())),
            best_position=("Position", lambda s: int(s.min() if len(s.dropna()) else 999)),
            total_goals_for=("Goals For", "sum"),
            total_points=("Points", "sum"),
            continent=("continent", "first"),
        ).reset_index()
        team_summary = team_summary.sort_values(["championship_count", "appearances", "total_goals_for"], ascending=[False, False, False])

        champion_counts = filtered[filtered["Position"] == 1].groupby("Team").size().reset_index(name="titles")
        champion_counts = champion_counts.sort_values("titles", ascending=True)  # True for clean horizontal bar ordering

        if champion_counts.empty:
            champion_fig = empty_figure("Championship Count by Team", "No title winners in selection")
        else:
            champion_fig = px.bar(
                champion_counts.tail(20),
                x="titles",
                y="Team",
                orientation="h",
                title="Championship Count by Team",
                labels={"titles": "Titles", "Team": "Team"},
                color_discrete_sequence=[COLORS["accent"]],
            )
            apply_chart_layout(champion_fig, height=380)
            max_titles = int(champion_counts["titles"].max()) if not champion_counts.empty else 0
            champion_fig.update_layout(
                yaxis={"automargin": True, "title": None},
                xaxis={"dtick": 1, "tick0": 0, "title": "Number of Titles"},
            )

        top4_by_continent = (
            filtered[filtered["Position"] <= 4]
            .groupby(["Year", "continent"])
            .size()
            .reset_index(name="top4_count")
        )

        if top4_by_continent.empty:
            top4_fig = empty_figure("Top 4 Finishes by Continent", "No top 4 teams in selection")
        else:
            top4_fig = px.bar(
                top4_by_continent,
                x="Year",
                y="top4_count",
                color="continent",
                title="Top 4 Finishes by Continent",
                labels={"top4_count": "Count", "continent": "Continent"},
            )
            apply_chart_layout(top4_fig, height=380)
            top4_fig.update_layout(
                yaxis={"dtick": 1, "tick0": 0, "title": "Top 4 Finishes"},
                xaxis={"title": "World Cup Edition"},
            )

        goals_by_team = (
            filtered.groupby("Team")
            .agg(total_goals_for=("Goals For", "sum"), appearances=("Year", "nunique"))
            .reset_index()
            .sort_values("total_goals_for", ascending=True)  # True for clean horizontal bar ordering
        )

        if goals_by_team.empty:
            goals_fig = empty_figure("Goals Scored by Team (Top 20)", "No data in selection")
        else:
            goals_fig = px.bar(
                goals_by_team.tail(20),
                x="total_goals_for",
                y="Team",
                orientation="h",
                title="Total Goals Scored by Team (Top 20)",
                labels={"total_goals_for": "Goals For", "Team": "Team"},
                color_discrete_sequence=[COLORS["accent_2"]],
            )
            apply_chart_layout(goals_fig, height=450)
            goals_fig.update_layout(
                yaxis={"automargin": True, "title": None},
                xaxis={"title": "Goals For"},
            )

        table_data = [] if filtered.empty else team_summary.to_dict("records")

        return (
            str(len(tournaments)),
            str(team_count),
            str(title_count),
            str(top4_count),
            champion_fig,
            top4_fig,
            goals_fig,
            table_data,
        )
