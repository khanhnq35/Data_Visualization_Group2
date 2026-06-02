from __future__ import annotations

import glob
import os
import pandas as pd
import plotly.express as px
from dash import dcc, html, dash_table, Input, Output

from src.components import graph_card, kpi_card, page_header
from src.theme import COLORS, apply_chart_layout, empty_figure


# ── Data Loading & Processing ──────────────────────────────────────────────────

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "Data", "archive")

SUMMARY_PATH = os.path.join(DATA_DIR, "FIFA - World Cup Summary.csv")
summary_df = pd.read_csv(SUMMARY_PATH)
summary_df.columns = [c.strip() for c in summary_df.columns]
summary_df["YEAR"] = summary_df["YEAR"].astype(int)

AVAILABLE_YEARS = sorted(
    [
        int(os.path.basename(f).replace("FIFA - ", "").replace(".csv", ""))
        for f in glob.glob(os.path.join(DATA_DIR, "FIFA - [0-9]*.csv"))
    ]
)

_cache: dict = {}


def load_year(year: int) -> pd.DataFrame:
    if year in _cache:
        return _cache[year]
    path = os.path.join(DATA_DIR, f"FIFA - {year}.csv")
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    df["Year"] = year
    df["Goal Difference"] = pd.to_numeric(
        df["Goal Difference"].astype(str).str.replace("−", "-"), errors="coerce"
    )
    df["Position"] = pd.to_numeric(df["Position"], errors="coerce")
    df["position_group"] = df["Position"].apply(_pos_group)
    _cache[year] = df
    return df


def _pos_group(pos):
    if pd.isna(pos):
        return "Other"
    if pos == 1:
        return "Champion"
    if pos <= 4:
        return "Top 4"
    if pos <= 8:
        return "Top 8"
    return "Other"


# Colour map shared across charts
POS_COLORS = {
    "Champion": "#facc15",  # Tailwind yellow-400 (corresponds to gold)
    "Top 4": "#94a3b8",     # Tailwind slate-400 (corresponds to silver)
    "Top 8": "#d97706",     # Tailwind amber-600 (corresponds to bronze)
    "Other": "#cbd5e1",     # Light gray
}

CHART_LAYOUT = dict(
    hovermode="closest",
)


# ── Page Layout ────────────────────────────────────────────────────────────────

def layout() -> html.Div:
    return html.Div(
        className="page-stack",
        children=[
            page_header(
                "Tournament Detail",
                "FIFA World Cup",
                "Explore team performance, standing tables, and goal profiles for any World Cup edition.",
            ),
            html.Div(
                className="filter-panel",
                style={"gridTemplateColumns": "180px", "justifyContent": "start"},
                children=[
                    html.Div(
                        className="filter-block",
                        children=[
                            html.Label("Select World Cup Year", htmlFor="tournament-year-dropdown"),
                            dcc.Dropdown(
                                id="tournament-year-dropdown",
                                options=[{"label": str(y), "value": y} for y in AVAILABLE_YEARS],
                                value=2022,
                                clearable=False,
                            ),
                        ],
                    ),
                ],
            ),
            # Top-4 highlight cards (populated via callback)
            html.Div(
                id="tournament-top4-cards",
                className="kpi-grid",
                style={"gridTemplateColumns": "repeat(4, minmax(140px, 1fr))"},
            ),
            # Tournament metadata summary (populated via callback)
            html.Div(
                className="kpi-grid",
                style={"gridTemplateColumns": "repeat(5, minmax(120px, 1fr))"},
                children=[
                    kpi_card("Host Country", "tournament-meta-host"),
                    kpi_card("Teams Entered", "tournament-meta-teams"),
                    kpi_card("Matches Played", "tournament-meta-matches"),
                    kpi_card("Total Goals", "tournament-meta-goals"),
                    kpi_card("Avg Goals / Match", "tournament-meta-avg-goals"),
                ],
            ),
            # Goals charts row
            html.Div(
                className="chart-grid two-column",
                children=[
                    graph_card("tournament-goals-for-chart"),
                    graph_card("tournament-goals-against-chart"),
                ],
            ),
            # Scatter plot row
            html.Div(
                className="chart-grid single-column",
                children=[
                    graph_card("tournament-scatter-chart", "chart-wide"),
                ],
            ),
            # Standings table card
            html.Div(
                className="chart-card",
                style={"padding": "24px"},
                children=[
                    html.H3("Full Standings", style={"margin": "0 0 16px 0", "fontSize": "16px", "color": COLORS["text"]}),
                    html.Div(id="tournament-ranking-table"),
                ],
            ),
            # 2022 specific insights (populated via callback)
            html.Div(id="tournament-insight-panel"),
        ],
    )


# ── Helper Card Builder ────────────────────────────────────────────────────────

def _card(rank_label: str, team: str, detail: str, color: str) -> html.Div:
    return html.Div(
        className="kpi-card",
        style={"borderLeft": f"4px solid {color}", "padding": "18px"},
        children=[
            html.Div(rank_label, className="kpi-label"),
            html.Div(team, className="kpi-value", style={"fontSize": "22px", "marginTop": "8px"}),
            html.Div(detail, className="kpi-helper", style={"marginTop": "8px"}),
        ],
    )


def _build_insight_panel(year: int, df: pd.DataFrame) -> html.Div:
    if year != 2022:
        return html.Div()

    insights = [
        {
            "team": "Argentina 🇦🇷",
            "color": "#3b82f6",
            "text": "Argentina claimed their third title, ending a 36-year wait. Messi led the tournament with 7 goals and 3 assists, finally completing international football's greatest individual narrative.",
        },
        {
            "team": "France 🇫🇷",
            "color": "#ef4444",
            "text": "The defending champions were fierce to the end — Mbappé's hat-trick in the final made it the most dramatic World Cup final in history. France's 16 goals was the joint-highest of any team.",
        },
        {
            "team": "Croatia 🇭🇷",
            "color": "#8b5cf6",
            "text": "Croatia confirmed their status as tournament stalwarts, claiming 3rd place for the second time in four editions. Solid defensive organisation and Modrić's midfield vision were key.",
        },
        {
            "team": "Morocco 🇲🇦",
            "color": "#10b981",
            "text": "The tournament's great story: Morocco became the first African and Arab nation to reach a World Cup semi-final, beating Spain and Portugal on the way.",
        },
    ]

    cards = []
    for ins in insights:
        cards.append(
            html.Div(
                className="chart-card",
                style={
                    "borderLeft": f"4px solid {ins['color']}",
                    "padding": "16px 20px",
                    "flex": "1",
                    "minWidth": "220px",
                },
                children=[
                    html.Div(ins["team"], style={"fontWeight": "700", "fontSize": "15px", "marginBottom": "8px", "color": COLORS["text"]}),
                    html.P(ins["text"], style={"fontSize": "13px", "color": COLORS["muted"], "margin": 0, "lineHeight": "1.5"}),
                ],
            )
        )

    return html.Div(
        style={"marginTop": "24px"},
        children=[
            html.H3(
                "2022 World Cup Analysis & Insights",
                style={"fontSize": "18px", "fontWeight": "750", "color": COLORS["text"], "marginBottom": "16px"},
            ),
            html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}, children=cards),
        ],
    )


# ── Callbacks Registration ─────────────────────────────────────────────────────

def register_callbacks(app) -> None:
    @app.callback(
        Output("tournament-top4-cards", "children"),
        Output("tournament-meta-host", "children"),
        Output("tournament-meta-teams", "children"),
        Output("tournament-meta-matches", "children"),
        Output("tournament-meta-goals", "children"),
        Output("tournament-meta-avg-goals", "children"),
        Output("tournament-goals-for-chart", "figure"),
        Output("tournament-goals-against-chart", "figure"),
        Output("tournament-scatter-chart", "figure"),
        Output("tournament-ranking-table", "children"),
        Output("tournament-insight-panel", "children"),
        Input("tournament-year-dropdown", "value"),
    )
    def update_all(year: int):
        df = load_year(year)
        df_sorted = df.sort_values("Position").reset_index(drop=True)

        # Summary row for this year
        meta = summary_df[summary_df["YEAR"] == year]

        # ── Top-4 cards ──────────────────────────────────────────────────────────
        top4 = df_sorted[df_sorted["Position"] <= 4].copy()
        card_colors = ["#facc15", "#94a3b8", "#d97706", "#64727d"]
        rank_labels = ["🏆 Champion", "Runner-Up", "3rd Place", "4th Place"]
        cards = []
        for i, (_, row) in enumerate(top4.iterrows()):
            if i >= 4:
                break
            gf = int(row.get("Goals For", 0)) if pd.notna(row.get("Goals For")) else 0
            ga = int(row.get("Goals Against", 0)) if pd.notna(row.get("Goals Against")) else 0
            detail = f"{int(row['Games Played'])} games · {gf} GF · {ga} GA"
            cards.append(_card(rank_labels[i], row["Team"], detail, card_colors[i]))

        top4_section = cards

        # ── Meta values ──────────────────────────────────────────────────────────
        host, teams, matches, goals, avg = "-", "-", "-", "-", "-"
        if not meta.empty:
            m = meta.iloc[0]
            host = str(m["HOST"])
            teams = str(int(m["TEAMS"]))
            matches = str(int(m["MATCHES PLAYED"]))
            goals = str(int(m["GOALS SCORED"]))
            avg = f"{float(m['AVG GOALS PER GAME']):.2f}"

        # ── Goals For chart ──────────────────────────────────────────────────────
        gf_df = df_sorted[["Team", "Goals For", "position_group"]].copy()
        gf_df = gf_df[pd.to_numeric(gf_df["Goals For"], errors="coerce").notna()]
        gf_df["Goals For"] = pd.to_numeric(gf_df["Goals For"])
        fig_gf = px.bar(
            gf_df.sort_values("Goals For", ascending=True),
            x="Goals For",
            y="Team",
            color="position_group",
            color_discrete_map=POS_COLORS,
            orientation="h",
            title=f"Goals Scored — {year}",
            labels={"Goals For": "Goals For", "position_group": "Standing Group"},
        )
        apply_chart_layout(fig_gf, height=380)
        fig_gf.update_layout(**CHART_LAYOUT)
        fig_gf.update_traces(hovertemplate="%{y}<br>Goals: %{x}<extra></extra>")

        # ── Goals Against chart ──────────────────────────────────────────────────
        ga_df = df_sorted[["Team", "Goals Against", "position_group"]].copy()
        ga_df = ga_df[pd.to_numeric(ga_df["Goals Against"], errors="coerce").notna()]
        ga_df["Goals Against"] = pd.to_numeric(ga_df["Goals Against"])
        fig_ga = px.bar(
            ga_df.sort_values("Goals Against", ascending=False),
            x="Goals Against",
            y="Team",
            color="position_group",
            color_discrete_map=POS_COLORS,
            orientation="h",
            title=f"Goals Conceded — {year}",
            labels={"Goals Against": "Goals Conceded", "position_group": "Standing Group"},
        )
        apply_chart_layout(fig_ga, height=380)
        fig_ga.update_layout(**CHART_LAYOUT)
        fig_ga.update_traces(hovertemplate="%{y}<br>Conceded: %{x}<extra></extra>")

        # ── Scatter plot ─────────────────────────────────────────────────────────
        sc_df = df_sorted[["Team", "Goals For", "Goals Against", "position_group", "Points", "Games Played"]].copy()
        for col in ["Goals For", "Goals Against", "Points"]:
            sc_df[col] = pd.to_numeric(sc_df[col], errors="coerce")
        sc_df = sc_df.dropna(subset=["Goals For", "Goals Against"])

        fig_sc = px.scatter(
            sc_df,
            x="Goals For",
            y="Goals Against",
            color="position_group",
            color_discrete_map=POS_COLORS,
            text="Team",
            size="Points",
            size_max=24,
            title=f"Goals Scored vs. Goals Conceded — {year}",
            labels={"position_group": "Standing Group"},
            hover_data={"Points": True, "Games Played": True},
        )
        apply_chart_layout(fig_sc, height=450)
        fig_sc.update_traces(
            textposition="top center",
            textfont_size=10,
            hovertemplate="<b>%{text}</b><br>GF: %{x}  GA: %{y}<br>Points: %{customdata[0]}<extra></extra>",
        )
        fig_sc.update_layout(**CHART_LAYOUT)
        fig_sc.update_layout(yaxis_autorange="reversed")  # Fewer conceded goals at the top is better!

        # ── Ranking table ────────────────────────────────────────────────────────
        display_cols = ["Position", "Team", "Games Played", "Win", "Draw", "Loss", "Goals For", "Goals Against", "Goal Difference", "Points"]
        tbl_cols = [c for c in display_cols if c in df_sorted.columns]
        tbl_df = df_sorted[tbl_cols].copy()
        tbl_df["Position"] = tbl_df["Position"].apply(lambda x: int(x) if pd.notna(x) else "")

        table = dash_table.DataTable(
            id="tournament-data-table",
            data=tbl_df.to_dict("records"),
            columns=[{"name": c, "id": c} for c in tbl_cols],
            sort_action="native",
            style_table={"overflowX": "auto"},
            style_header={
                "backgroundColor": "#f6f8fb",
                "color": "#172026",
                "fontWeight": "600",
                "fontSize": "12px",
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
                {"if": {"filter_query": "{Position} = 1"}, "color": COLORS["accent_2"], "fontWeight": "700"},
            ],
            page_size=20,
        )

        # ── Insight panel (only for 2022) ────────────────────────────────────────
        insight_panel = _build_insight_panel(year, df_sorted)

        return top4_section, host, teams, matches, goals, avg, fig_gf, fig_ga, fig_sc, table, insight_panel
