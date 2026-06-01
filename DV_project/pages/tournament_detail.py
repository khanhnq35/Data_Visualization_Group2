# -*- coding: utf-8 -*-
import os
import glob
import pandas as pd
import dash
from dash import dcc, html, dash_table, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__, path="/tournament-detail", name="Tournament Detail")

# ── Data loading ──────────────────────────────────────────────────────────────

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
    "Champion": "#FFD700",
    "Top 4": "#C0C0C0",
    "Top 8": "#CD7F32",
    "Other": "#6B7280",
}

# ── Layout ────────────────────────────────────────────────────────────────────

layout = html.Div(
    id="tournament-page-root",
    style={"fontFamily": "Inter, sans-serif", "padding": "24px", "backgroundColor": "#0f172a", "minHeight": "100vh", "color": "#f1f5f9"},
    children=[
        # Header
        html.Div(
            style={"marginBottom": "24px"},
            children=[
                html.H1(
                    "Tournament Detail",
                    style={"fontSize": "28px", "fontWeight": "700", "color": "#f1f5f9", "margin": "0 0 4px 0"},
                ),
                html.P(
                    "Explore team performance for any FIFA World Cup edition.",
                    style={"color": "#94a3b8", "margin": 0},
                ),
            ],
        ),
        # Year selector
        html.Div(
            style={"marginBottom": "28px", "display": "flex", "alignItems": "center", "gap": "16px"},
            children=[
                html.Label("Select Year:", style={"fontWeight": "600", "color": "#94a3b8", "fontSize": "14px"}),
                dcc.Dropdown(
                    id="tournament-year-dropdown",
                    options=[{"label": str(y), "value": y} for y in AVAILABLE_YEARS],
                    value=2022,
                    clearable=False,
                    style={
                        "width": "160px",
                        "backgroundColor": "#1e293b",
                        "color": "#f1f5f9",
                        "border": "1px solid #334155",
                        "borderRadius": "8px",
                    },
                ),
            ],
        ),
        # Top-4 highlight cards
        html.Div(id="tournament-top4-cards", style={"marginBottom": "28px"}),
        # Tournament meta strip
        html.Div(id="tournament-meta-strip", style={"marginBottom": "28px"}),
        # Charts row 1: goals for + goals against
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px", "marginBottom": "20px"},
            children=[
                html.Div(
                    id="tournament-goals-for-card",
                    style={"backgroundColor": "#1e293b", "borderRadius": "12px", "padding": "16px"},
                    children=[dcc.Graph(id="tournament-goals-for-chart", config={"displayModeBar": False})],
                ),
                html.Div(
                    id="tournament-goals-against-card",
                    style={"backgroundColor": "#1e293b", "borderRadius": "12px", "padding": "16px"},
                    children=[dcc.Graph(id="tournament-goals-against-chart", config={"displayModeBar": False})],
                ),
            ],
        ),
        # Charts row 2: scatter
        html.Div(
            style={"backgroundColor": "#1e293b", "borderRadius": "12px", "padding": "16px", "marginBottom": "20px"},
            children=[dcc.Graph(id="tournament-scatter-chart", config={"displayModeBar": False})],
        ),
        # Ranking table
        html.Div(
            style={"backgroundColor": "#1e293b", "borderRadius": "12px", "padding": "16px", "marginBottom": "20px"},
            children=[
                html.H3("Full Standings", style={"margin": "0 0 12px 0", "fontSize": "16px", "color": "#f1f5f9"}),
                html.Div(id="tournament-ranking-table"),
            ],
        ),
        # 2022 insight panel
        html.Div(id="tournament-insight-panel"),
    ],
)

# ── Helpers ───────────────────────────────────────────────────────────────────

CHART_LAYOUT = dict(
    paper_bgcolor="#1e293b",
    plot_bgcolor="#1e293b",
    font_color="#f1f5f9",
    font_size=12,
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="#334155", zeroline=False),
)


def _card(rank_label: str, team: str, detail: str, color: str) -> html.Div:
    return html.Div(
        style={
            "backgroundColor": "#1e293b",
            "borderRadius": "12px",
            "padding": "16px 20px",
            "borderLeft": f"4px solid {color}",
            "flex": "1",
        },
        children=[
            html.Div(rank_label, style={"fontSize": "11px", "color": "#64748b", "fontWeight": "700", "textTransform": "uppercase", "marginBottom": "4px"}),
            html.Div(team, style={"fontSize": "20px", "fontWeight": "700", "color": "#f1f5f9"}),
            html.Div(detail, style={"fontSize": "13px", "color": "#94a3b8", "marginTop": "4px"}),
        ],
    )


# ── Callbacks ─────────────────────────────────────────────────────────────────

@callback(
    Output("tournament-top4-cards", "children"),
    Output("tournament-meta-strip", "children"),
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
    card_colors = ["#FFD700", "#C0C0C0", "#CD7F32", "#6B7280"]
    rank_labels = ["🏆 Champion", "Runner-Up", "3rd Place", "4th Place"]
    cards = []
    for i, (_, row) in enumerate(top4.iterrows()):
        if i >= 4:
            break
        gf = int(row.get("Goals For", 0)) if pd.notna(row.get("Goals For")) else 0
        ga = int(row.get("Goals Against", 0)) if pd.notna(row.get("Goals Against")) else 0
        detail = f"{int(row['Games Played'])} games · {gf} GF · {ga} GA"
        cards.append(_card(rank_labels[i], row["Team"], detail, card_colors[i]))

    top4_section = html.Div(
        style={"display": "flex", "gap": "16px"},
        children=cards,
    )

    # ── Meta strip ───────────────────────────────────────────────────────────
    if not meta.empty:
        m = meta.iloc[0]
        host = m["HOST"]
        teams = int(m["TEAMS"])
        matches = int(m["MATCHES PLAYED"])
        goals = int(m["GOALS SCORED"])
        avg = float(m["AVG GOALS PER GAME"])
        meta_strip = html.Div(
            style={"display": "flex", "gap": "16px", "flexWrap": "wrap"},
            children=[
                _meta_chip("Host", host),
                _meta_chip("Teams", str(teams)),
                _meta_chip("Matches", str(matches)),
                _meta_chip("Goals", str(goals)),
                _meta_chip("Avg Goals/Game", f"{avg:.1f}"),
            ],
        )
    else:
        meta_strip = html.Div()

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
        labels={"Goals For": "Goals For", "position_group": "Group"},
    )
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
        labels={"Goals Against": "Goals Against", "position_group": "Group"},
    )
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
        size_max=30,
        title=f"Goals For vs Goals Against — {year}",
        labels={"position_group": "Group"},
        hover_data={"Points": True, "Games Played": True},
    )
    fig_sc.update_traces(
        textposition="top center",
        textfont_size=10,
        hovertemplate="<b>%{text}</b><br>GF: %{x}  GA: %{y}<br>Points: %{customdata[0]}<extra></extra>",
    )
    fig_sc.update_layout(**CHART_LAYOUT)
    fig_sc.update_layout(yaxis_autorange="reversed")

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
            "backgroundColor": "#0f172a",
            "color": "#94a3b8",
            "fontWeight": "600",
            "fontSize": "12px",
            "border": "1px solid #334155",
            "textTransform": "uppercase",
            "letterSpacing": "0.05em",
        },
        style_data={
            "backgroundColor": "#1e293b",
            "color": "#f1f5f9",
            "fontSize": "13px",
            "border": "1px solid #334155",
        },
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "#243044"},
            {"if": {"filter_query": "{Position} = 1"}, "color": "#FFD700", "fontWeight": "700"},
        ],
        page_size=20,
    )

    # ── Insight panel (only for 2022) ────────────────────────────────────────
    insight_panel = _build_insight_panel(year, df_sorted)

    return top4_section, meta_strip, fig_gf, fig_ga, fig_sc, table, insight_panel


def _meta_chip(label: str, value: str) -> html.Div:
    return html.Div(
        style={
            "backgroundColor": "#0f172a",
            "borderRadius": "8px",
            "padding": "10px 16px",
            "display": "flex",
            "flexDirection": "column",
            "gap": "2px",
        },
        children=[
            html.Span(label, style={"fontSize": "11px", "color": "#64748b", "fontWeight": "600", "textTransform": "uppercase"}),
            html.Span(value, style={"fontSize": "18px", "fontWeight": "700", "color": "#f1f5f9"}),
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
                style={
                    "backgroundColor": "#1e293b",
                    "borderRadius": "12px",
                    "padding": "16px 20px",
                    "borderLeft": f"4px solid {ins['color']}",
                    "flex": "1",
                    "minWidth": "220px",
                },
                children=[
                    html.Div(ins["team"], style={"fontWeight": "700", "fontSize": "15px", "marginBottom": "8px", "color": "#f1f5f9"}),
                    html.P(ins["text"], style={"fontSize": "13px", "color": "#94a3b8", "margin": 0, "lineHeight": "1.5"}),
                ],
            )
        )

    return html.Div(
        style={"marginBottom": "20px"},
        children=[
            html.H3(
                "2022 World Cup Analysis",
                style={"fontSize": "18px", "fontWeight": "700", "color": "#f1f5f9", "marginBottom": "16px"},
            ),
            html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}, children=cards),
        ],
    )
