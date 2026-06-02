# -*- coding: utf-8 -*-
import glob
import os
from collections import Counter

import pandas as pd
import dash
from dash import dcc, html, dash_table, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__, path="/dominance", name="Dominance")

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
        "style": {"color": "#cbd5e1", "fontSize": "12px", "whiteSpace": "nowrap"},
    }
    for year in AVAILABLE_YEARS
    if year == min(AVAILABLE_YEARS)
    or year == max(AVAILABLE_YEARS)
    or year % 20 == 10
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

TEAM_CONTINENT = {}


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


def _build_status_card(label: str, value: str, description: str) -> html.Div:
    return html.Div(
        style={
            "backgroundColor": "#1e293b",
            "borderRadius": "16px",
            "padding": "18px",
            "flex": "1",
            "minWidth": "180px",
            "border": "1px solid #334155",
        },
        children=[
            html.Div(label, style={"color": "#94a3b8", "fontSize": "12px", "fontWeight": "700", "textTransform": "uppercase", "marginBottom": "8px"}),
            html.Div(value, style={"color": "#f1f5f9", "fontSize": "24px", "fontWeight": "700"}),
            html.Div(description, style={"color": "#cbd5e1", "fontSize": "13px", "marginTop": "6px"}),
        ],
    )


def _empty_figure(message: str):
    fig = go.Figure()
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font_color="#f1f5f9",
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[
            {
                "text": message,
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 16, "color": "#cbd5e1"},
                "x": 0.5,
                "y": 0.5,
                "xanchor": "center",
                "yanchor": "middle",
            }
        ],
    )
    return fig


layout = html.Div(
    id="dominance-page-root",
    style={"fontFamily": "Inter, sans-serif", "padding": "24px", "backgroundColor": "#0f172a", "minHeight": "100vh", "color": "#f1f5f9"},
    children=[
        html.Div(
            style={"marginBottom": "24px"},
            children=[
                html.H1("Dominance", style={"fontSize": "28px", "fontWeight": "700", "color": "#f1f5f9", "margin": "0 0 4px 0"}),
                html.P("Explore World Cup domination patterns by teams and continents.", style={"color": "#94a3b8", "margin": 0}),
            ],
        ),
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(240px, 1fr))", "gap": "16px", "marginBottom": "24px"},
            children=[
                html.Div(
                    style={"backgroundColor": "#1e293b", "padding": "20px", "borderRadius": "16px", "border": "1px solid #334155"},
                    children=[
                        html.Div("Year range", style={"color": "#94a3b8", "fontSize": "13px", "fontWeight": "700", "marginBottom": "12px"}),
                        dcc.RangeSlider(
                            id="dominance-year-range",
                            className="dash-range-slider",
                            min=min(AVAILABLE_YEARS),
                            max=max(AVAILABLE_YEARS),
                            step=4,
                            marks=YEAR_SLIDER_MARKS,
                            value=[min(AVAILABLE_YEARS), max(AVAILABLE_YEARS)],
                            tooltip={"placement": "bottom", "always_visible": False},
                        ),
                    ],
                ),
                html.Div(
                    style={"backgroundColor": "#1e293b", "padding": "20px", "borderRadius": "16px", "border": "1px solid #334155"},
                    children=[
                        html.Div("Team filter", style={"color": "#94a3b8", "fontSize": "13px", "fontWeight": "700", "marginBottom": "12px"}),
                        dcc.Dropdown(
                            id="dominance-team-filter",
                            options=[{"label": team, "value": team} for team in TEAM_OPTIONS],
                            value=[],
                            multi=True,
                            placeholder="All teams",
                            style={"color": "#0f172a", "backgroundColor": "#f8fafc"},
                        ),
                    ],
                ),
                html.Div(
                    style={"backgroundColor": "#1e293b", "padding": "20px", "borderRadius": "16px", "border": "1px solid #334155"},
                    children=[
                        html.Div("Continent filter", style={"color": "#94a3b8", "fontSize": "13px", "fontWeight": "700", "marginBottom": "12px"}),
                        dcc.Dropdown(
                            id="dominance-continent-filter",
                            options=[{"label": cont, "value": cont} for cont in CONTINENT_OPTIONS],
                            value=CONTINENT_OPTIONS,
                            multi=True,
                            placeholder="All continents",
                            style={"color": "#0f172a", "backgroundColor": "#f8fafc"},
                        ),
                    ],
                ),
                html.Div(
                    style={"backgroundColor": "#1e293b", "padding": "20px", "borderRadius": "16px", "border": "1px solid #334155"},
                    children=[
                        html.Div("Position group", style={"color": "#94a3b8", "fontSize": "13px", "fontWeight": "700", "marginBottom": "12px"}),
                        dcc.Dropdown(
                            id="dominance-position-filter",
                            options=[{"label": group, "value": group} for group in POSITION_OPTIONS],
                            value=POSITION_OPTIONS,
                            multi=True,
                            placeholder="All groups",
                            style={"color": "#0f172a", "backgroundColor": "#f8fafc"},
                        ),
                    ],
                ),
            ],
        ),
        html.Div(id="dominance-cards-row", style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(220px, 1fr))", "gap": "16px", "marginBottom": "24px"}),
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px", "marginBottom": "24px"},
            children=[
                html.Div(
                    style={"backgroundColor": "#1e293b", "borderRadius": "16px", "padding": "16px"},
                    children=[dcc.Graph(id="dominance-champion-bar", config={"displayModeBar": False})],
                ),
                html.Div(
                    style={"backgroundColor": "#1e293b", "borderRadius": "16px", "padding": "16px"},
                    children=[dcc.Graph(id="dominance-top4-by-continent", config={"displayModeBar": False})],
                ),
            ],
        ),
        html.Div(
            style={"backgroundColor": "#1e293b", "borderRadius": "16px", "padding": "16px", "marginBottom": "24px"},
            children=[dcc.Graph(id="dominance-goals-for-chart", config={"displayModeBar": False})],
        ),
        html.Div(
            style={"backgroundColor": "#1e293b", "borderRadius": "16px", "padding": "16px"},
            children=[
                html.H3("Team dominance summary", style={"margin": "0 0 12px 0", "fontSize": "18px", "color": "#f1f5f9"}),
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
                            ("Best position", "best_position"),
                            ("Goals For", "total_goals_for"),
                            ("Points", "total_points"),
                        ]
                    ],
                    sort_action="native",
                    page_size=20,
                    style_table={"overflowX": "auto"},
                    style_header={
                        "backgroundColor": "#0f172a",
                        "color": "#94a3b8",
                        "fontWeight": "600",
                        "fontSize": "12px",
                        "border": "1px solid #334155",
                        "textTransform": "uppercase",
                    },
                    style_data={
                        "backgroundColor": "#1e293b",
                        "color": "#f1f5f9",
                        "fontSize": "13px",
                        "border": "1px solid #334155",
                    },
                    style_data_conditional=[
                        {"if": {"row_index": "odd"}, "backgroundColor": "#243044"},
                        {"if": {"filter_query": "{Championships} > 0"}, "color": "#facc15", "fontWeight": "700"},
                    ],
                )
            ],
        ),
    ],
)


@callback(
    Output("dominance-cards-row", "children"),
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

    card_children = [
        _build_status_card("Tournaments", str(len(tournaments)), "World Cup editions in range"),
        _build_status_card("Teams", str(team_count), "Unique teams included"),
        _build_status_card("Titles", str(title_count), "Champion finishes in selection"),
        _build_status_card("Top 4 finishes", str(top4_count), "Teams reaching top 4"),
    ]

    champion_counts = filtered[filtered["Position"] == 1].groupby("Team").size().reset_index(name="titles")
    champion_counts = champion_counts.sort_values("titles", ascending=False)
    if champion_counts.empty:
        champion_fig = _empty_figure("No champion data for current filters")
    else:
        champion_fig = px.bar(
            champion_counts.head(20),
            x="titles",
            y="Team",
            orientation="h",
            title="Championship count by team",
            labels={"titles": "Titles", "Team": "Team"},
            color="titles",
            color_continuous_scale="teal",
        )
        max_titles = int(champion_counts["titles"].max()) if not champion_counts.empty else 0
        tick_values = list(range(0, max_titles + 1))
        champion_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font_color="#f1f5f9",
            margin=dict(l=110, r=10, t=40, b=20),
            yaxis=dict(automargin=True),
            xaxis=dict(dtick=1, tick0=0),
        )
        champion_fig.update_traces(
            marker=dict(
                colorbar=dict(
                    tickmode="array",
                    tickvals=tick_values,
                    ticktext=[str(val) for val in tick_values],
                    tickformat="d",
                )
            )
        )

    top4_by_continent = (
        filtered[filtered["Position"] <= 4]
        .groupby(["Year", "continent"])
        .size()
        .reset_index(name="top4_count")
    )
    if top4_by_continent.empty:
        top4_fig = _empty_figure("No top-4 finishes for current filters")
    else:
        top4_fig = px.bar(
            top4_by_continent,
            x="Year",
            y="top4_count",
            color="continent",
            title="Top 4 finishes by continent",
            labels={"top4_count": "Top 4 count", "continent": "Continent"},
        )
        top4_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font_color="#f1f5f9",
            margin=dict(l=40, r=10, t=40, b=40),
            yaxis=dict(dtick=1, tick0=0),
        )

    goals_by_team = (
        filtered.groupby("Team")
        .agg(total_goals_for=("Goals For", "sum"), appearances=("Year", "nunique"))
        .reset_index()
        .sort_values("total_goals_for", ascending=False)
    )
    if goals_by_team.empty:
        goals_fig = _empty_figure("No team goal data for current filters")
    else:
        goals_fig = px.bar(
            goals_by_team.head(20),
            x="total_goals_for",
            y="Team",
            orientation="h",
            title="Goals scored by team",
            labels={"total_goals_for": "Goals For", "Team": "Team"},
            color="total_goals_for",
            color_continuous_scale="teal",
        )
        goals_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font_color="#f1f5f9",
            margin=dict(l=110, r=10, t=40, b=20),
            yaxis=dict(automargin=True),
        )

    if filtered.empty:
        table_data = []
    else:
        table_data = team_summary.to_dict("records")

    return card_children, champion_fig, top4_fig, goals_fig, table_data
