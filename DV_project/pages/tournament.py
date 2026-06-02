# -*- coding: utf-8 -*-
from __future__ import annotations

import glob
import os

import pandas as pd
import plotly.express as px
from dash import Input, Output, dash_table, dcc, html

from src.components import page_header
from src.theme import COLORS, apply_chart_layout, empty_figure

# ── Data loading ───────────────────────────────────────────────────────────────

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


def _load_year(year: int) -> pd.DataFrame:
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


POS_COLORS = {
    "Champion": COLORS["accent_2"],   # amber
    "Top 4":    COLORS["accent"],     # teal
    "Top 8":    "#7c3aed",            # purple — CVD-safe (tránh đỏ-xanh lá)
    "Other":    COLORS["muted"],      # grey
}

# Flag emoji + short label for chart axes
TEAM_LABEL: dict[str, str] = {
    "Argentina":     "ARG",
    "France":        "FRA",
    "Croatia":       "CRO",
    "Morocco":       "MAR",
    "England":       "ENG",
    "Netherlands":   "NED",
    "Portugal":      "POR",
    "Brazil":        "BRA",
    "Japan":         "JPN",
    "Senegal":       "SEN",
    "Australia":     "AUS",
    "Switzerland":   "SUI",
    "USA":           "USA",
    "Spain":         "ESP",
    "Poland":        "POL",
    "South Korea":   "KOR",
    "Germany":       "GER",
    "Ecuador":       "ECU",
    "Cameroon":      "CMR",
    "Uruguay":       "URU",
    "Tunisia":       "TUN",
    "Mexico":        "MEX",
    "Belgium":       "BEL",
    "Ghana":         "GHA",
    "Saudi Arabia":  "KSA",
    "Iran":          "IRN",
    "Costa Rica":    "CRC",
    "Denmark":       "DEN",
    "Serbia":        "SRB",
    "Wales":         "WAL",
    "Canada":        "CAN",
    "Qatar":         "QAT",
    "Italy":         "ITA",
    "West Germany":  "WGR",
    "Hungary":       "HUN",
    "Sweden":        "SWE",
    "Austria":       "AUT",
    "Czechoslovakia":"TCH",
    "Chile":         "CHI",
    "Yugoslavia":    "YUG",
    "United States": "USA",
    "Soviet Union":  "URS",
    "Turkey":        "TUR",
    "Bulgaria":      "BUL",
    "Romania":       "ROU",
    "Paraguay":      "PAR",
    "Bolivia":       "BOL",
    "Peru":          "PER",
    "Colombia":      "COL",
    "Russia":        "RUS",
    "Slovakia":      "SVK",
    "Greece":        "GRE",
    "Algeria":       "ALG",
    "Nigeria":       "NGA",
    "Honduras":      "HON",
    "New Zealand":   "NZL",
    "Ivory Coast":   "CIV",
    "North Korea":   "PRK",
    "Serbia and Montenegro": "SCG",
    "FR Yugoslavia": "YUG",
    "Dutch East Indies": "DEI",
    "East Germany":  "GDR",
    "Israel":        "ISR",
    "El Salvador":   "SLV",
    "Haiti":         "HAI",
    "Cuba":          "CUB",
    "Norway":        "NOR",
    "Scotland":      "SCO",
    "Northern Ireland": "NIR",
    "Republic of Ireland": "IRL",
    "Kuwait":        "KUW",
    "Cameroon":      "CMR",
    "Egypt":         "EGY",
    "South Africa":  "RSA",
    "Togo":          "TOG",
    "Angola":        "ANG",
    "Slovenia":      "SVN",
    "Trinidad and Tobago": "TRI",
    "Ukraine":       "UKR",
    "Czech Republic":"CZE",
}


def _short(team: str) -> str:
    return TEAM_LABEL.get(team, team)

# ── Layout ─────────────────────────────────────────────────────────────────────


def layout() -> html.Div:
    return html.Div(
        className="page-stack",
        children=[
            page_header(
                "Tournament Detail",
                "FIFA World Cup",
                "Explore team performance, standings, and goal profiles for any World Cup edition.",
            ),
            # Year filter
            html.Div(
                className="filter-panel",
                style={"gridTemplateColumns": "200px"},
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
            # Top-4 KPI cards
            html.Div(
                id="tournament-top4-cards",
                className="kpi-grid",
                style={"gridTemplateColumns": "repeat(4, minmax(140px, 1fr))"},
            ),
            # Meta strip
            html.Div(
                className="kpi-grid",
                style={"gridTemplateColumns": "repeat(5, minmax(120px, 1fr))"},
                children=[
                    _kpi_card("Host Country",      "tournament-meta-host"),
                    _kpi_card("Teams",             "tournament-meta-teams"),
                    _kpi_card("Matches Played",    "tournament-meta-matches"),
                    _kpi_card("Total Goals",       "tournament-meta-goals"),
                    _kpi_card("Avg Goals / Match", "tournament-meta-avg"),
                ],
            ),
            # Goals charts
            html.Div(
                className="chart-grid two-column",
                children=[
                    html.Div(className="chart-card", style={"minHeight": "500px"},
                             children=dcc.Graph(id="tournament-goals-for-chart",
                                                config={"displayModeBar": False, "responsive": True},
                                                style={"height": "100%", "minHeight": "500px"})),
                    html.Div(className="chart-card", style={"minHeight": "500px"},
                             children=dcc.Graph(id="tournament-goals-against-chart",
                                                config={"displayModeBar": False, "responsive": True},
                                                style={"height": "100%", "minHeight": "500px"})),
                ],
            ),
            # Scatter
            html.Div(
                className="chart-grid single-column",
                children=[
                    html.Div(className="chart-card chart-wide", style={"minHeight": "460px"},
                             children=dcc.Graph(id="tournament-scatter-chart",
                                                config={"displayModeBar": False, "responsive": True},
                                                style={"height": "100%", "minHeight": "460px"})),
                ],
            ),
            # Standings table
            html.Div(
                className="chart-card",
                style={"padding": "24px"},
                children=[
                    html.H3("Full Standings", style={"margin": "0 0 16px 0", "fontSize": "16px", "color": COLORS["text"]}),
                    html.Div(id="tournament-ranking-table"),
                ],
            ),
            # 2022 insight panel
            html.Div(id="tournament-insight-panel"),
        ],
    )


# ── Small helpers ──────────────────────────────────────────────────────────────


def _kpi_card(label: str, value_id: str) -> html.Div:
    return html.Div(
        className="kpi-card",
        children=[
            html.Div(label, className="kpi-label"),
            html.Div(id=value_id, className="kpi-value"),
        ],
    )


def _rank_card(rank_label: str, team: str, detail: str, accent: str) -> html.Div:
    return html.Div(
        className="kpi-card",
        style={"borderLeft": f"4px solid {accent}"},
        children=[
            html.Div(rank_label, className="kpi-label"),
            html.Div(team, className="kpi-value", style={"fontSize": "22px", "marginTop": "8px"}),
            html.Div(detail, className="kpi-helper", style={"marginTop": "8px"}),
        ],
    )


# ── Callbacks ──────────────────────────────────────────────────────────────────


def register_callbacks(app) -> None:
    @app.callback(
        Output("tournament-top4-cards",      "children"),
        Output("tournament-meta-host",       "children"),
        Output("tournament-meta-teams",      "children"),
        Output("tournament-meta-matches",    "children"),
        Output("tournament-meta-goals",      "children"),
        Output("tournament-meta-avg",        "children"),
        Output("tournament-goals-for-chart",     "figure"),
        Output("tournament-goals-against-chart", "figure"),
        Output("tournament-scatter-chart",       "figure"),
        Output("tournament-ranking-table",       "children"),
        Output("tournament-insight-panel",       "children"),
        Input("tournament-year-dropdown", "value"),
    )
    def update_all(year: int):
        df = _load_year(year)
        df_sorted = df.sort_values("Position").reset_index(drop=True)
        meta = summary_df[summary_df["YEAR"] == year]

        # ── Top-4 cards ───────────────────────────────────────────────────────
        top4 = df_sorted[df_sorted["Position"] <= 4]
        accents = ["#d98324", "#64727d", "#b45309", "#94a3b8"]
        labels  = ["\U0001f3c6 Champion", "Runner-Up", "3rd Place", "4th Place"]
        cards = []
        for i, (_, row) in enumerate(top4.iterrows()):
            if i >= 4:
                break
            gf = int(row["Goals For"])  if pd.notna(row.get("Goals For"))     else 0
            ga = int(row["Goals Against"]) if pd.notna(row.get("Goals Against")) else 0
            detail = f"{int(row['Games Played'])} games · {gf} GF · {ga} GA"
            cards.append(_rank_card(labels[i], row["Team"], detail, accents[i]))

        # ── Meta values ───────────────────────────────────────────────────────
        host = teams = matches = goals = avg = "—"
        if not meta.empty:
            m = meta.iloc[0]
            host    = str(m["HOST"])
            teams   = str(int(m["TEAMS"]))
            matches = str(int(m["MATCHES PLAYED"]))
            goals   = str(int(m["GOALS SCORED"]))
            avg     = f"{float(m['AVG GOALS PER GAME']):.2f}"

        # ── Goals For chart ───────────────────────────────────────────────────
        gf_df = df_sorted[["Team", "Goals For", "position_group"]].copy()
        gf_df["Goals For"] = pd.to_numeric(gf_df["Goals For"], errors="coerce")
        gf_df = gf_df.dropna(subset=["Goals For"]).sort_values("Goals For", ascending=True)
        gf_df["Label"] = gf_df["Team"].map(_short)
        if gf_df.empty:
            fig_gf = empty_figure(f"Sức tấn công {year}")
        else:
            fig_gf = px.bar(
                gf_df, x="Goals For", y="Label", orientation="h",
                color="position_group", color_discrete_map=POS_COLORS,
                title=f"Bàn ghi được — {year}",
                labels={"Goals For": "Bàn ghi", "Label": "", "position_group": "Nhóm"},
                custom_data=["Team"],
            )
            apply_chart_layout(fig_gf, height=max(400, len(gf_df) * 28))
            fig_gf.update_layout(
                title_font_size=14,
                margin={"l": 55, "r": 16, "t": 44, "b": 80},
                legend={"orientation": "h", "yanchor": "top", "y": -0.09, "xanchor": "left", "x": 0, "font": {"size": 11}},
            )
            fig_gf.update_traces(hovertemplate="%{customdata[0]}<br>Bàn ghi: %{x}<extra></extra>")

        # ── Goals Against chart ───────────────────────────────────────────────
        ga_df = df_sorted[["Team", "Goals Against", "position_group"]].copy()
        ga_df["Goals Against"] = pd.to_numeric(ga_df["Goals Against"], errors="coerce")
        ga_df = ga_df.dropna(subset=["Goals Against"]).sort_values("Goals Against", ascending=True)
        ga_df["Label"] = ga_df["Team"].map(_short)
        if ga_df.empty:
            fig_ga = empty_figure(f"Phòng ngự {year}")
        else:
            fig_ga = px.bar(
                ga_df, x="Goals Against", y="Label", orientation="h",
                color="position_group", color_discrete_map=POS_COLORS,
                title=f"Bàn thủng lưới — {year}",
                labels={"Goals Against": "Bàn thủng", "Label": "", "position_group": "Nhóm"},
                custom_data=["Team"],
            )
            apply_chart_layout(fig_ga, height=max(400, len(ga_df) * 28))
            fig_ga.update_layout(
                title_font_size=14,
                margin={"l": 55, "r": 16, "t": 44, "b": 80},
                legend={"orientation": "h", "yanchor": "top", "y": -0.09, "xanchor": "left", "x": 0, "font": {"size": 11}},
            )
            fig_ga.update_traces(hovertemplate="%{customdata[0]}<br>Bàn thủng: %{x}<extra></extra>")

        # ── Scatter ───────────────────────────────────────────────────────────
        sc_df = df_sorted[["Team", "Goals For", "Goals Against", "position_group", "Points", "Games Played"]].copy()
        for col in ["Goals For", "Goals Against", "Points"]:
            sc_df[col] = pd.to_numeric(sc_df[col], errors="coerce")
        sc_df = sc_df.dropna(subset=["Goals For", "Goals Against"])
        sc_df["Label"] = sc_df["Team"].map(_short)
        # only label top 8 to avoid overlap
        sc_df["DisplayLabel"] = sc_df.apply(
            lambda r: r["Label"] if r["position_group"] in ("Champion", "Top 4", "Top 8") else "", axis=1
        )
        if sc_df.empty:
            fig_sc = empty_figure(f"Goals Scored vs Conceded — {year}")
        else:
            fig_sc = px.scatter(
                sc_df, x="Goals For", y="Goals Against",
                color="position_group", color_discrete_map=POS_COLORS,
                text="DisplayLabel", size="Points", size_max=28,
                title=f"Tấn công vs Phòng ngự — {year}",
                labels={"position_group": "Nhóm", "Goals For": "Bàn ghi", "Goals Against": "Bàn thủng"},
                custom_data=["Team", "Points", "Games Played", "Label"],
            )
            apply_chart_layout(fig_sc, height=500)
            # Diagonal reference line GF = GA
            max_val = max(sc_df["Goals For"].max(), sc_df["Goals Against"].max()) + 1
            fig_sc.add_shape(
                type="line", x0=0, y0=0, x1=max_val, y1=max_val,
                line={"dash": "dot", "color": COLORS["muted"], "width": 1.5},
            )
            fig_sc.add_annotation(
                x=max_val * 0.6, y=max_val * 0.6,
                text="GF = GA", showarrow=False,
                font={"size": 10, "color": COLORS["muted"]}, textangle=-35,
            )
            # Annotation vùng hướng dẫn đọc chart
            fig_sc.add_annotation(
                x=max_val * 0.12, y=max_val * 0.82,
                text="Nhiều GA hơn GF<br>(thiên phòng ngự)",
                showarrow=False, font={"size": 9, "color": COLORS["muted"]}, align="center",
            )
            fig_sc.add_annotation(
                x=max_val * 0.82, y=max_val * 0.12,
                text="Nhiều GF hơn GA<br>(thiên tấn công)",
                showarrow=False, font={"size": 9, "color": COLORS["muted"]}, align="center",
            )
            fig_sc.update_layout(
                yaxis_autorange="reversed",
                margin={"l": 48, "r": 48, "t": 56, "b": 48},
                legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
            )
            fig_sc.update_traces(
                textposition="top center",
                textfont_size=10,
                cliponaxis=False,
                hovertemplate="<b>%{customdata[0]}</b> (%{customdata[3]})<br>Bàn ghi: %{x}  Bàn thủng: %{y}<br>Điểm: %{customdata[1]}<extra></extra>",
            )

        # ── Standings table ───────────────────────────────────────────────────
        display_cols = ["Position", "Team", "Games Played", "Win", "Draw", "Loss",
                        "Goals For", "Goals Against", "Goal Difference", "Points"]
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
                "color": COLORS["text"],
                "fontWeight": "600",
                "fontSize": "12px",
                "border": f"1px solid {COLORS['border']}",
                "textTransform": "uppercase",
                "letterSpacing": "0.03em",
            },
            style_data={
                "backgroundColor": COLORS["surface"],
                "color": COLORS["text"],
                "fontSize": "13px",
                "border": f"1px solid {COLORS['border']}",
            },
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "#f8fafc"},
                {"if": {"filter_query": "{Position} = 1"},
                 "color": COLORS["accent_2"], "fontWeight": "700"},
            ],
            page_size=20,
        )

        # ── Insight panel (2022 only) ─────────────────────────────────────────
        insight = _build_insight_panel(year)

        return cards, host, teams, matches, goals, avg, fig_gf, fig_ga, fig_sc, table, insight


# ── 2022 insight panel ─────────────────────────────────────────────────────────


def _build_insight_panel(year: int) -> html.Div:
    if year != 2022:
        return html.Div()

    insights = [
        {
            "team": "Argentina \U0001f1e6\U0001f1f7",
            "color": COLORS["accent_2"],
            "text": "Argentina claimed their third title, ending a 36-year wait. Messi led the tournament with 7 goals and 3 assists, finally completing international football's greatest individual narrative.",
        },
        {
            "team": "France \U0001f1eb\U0001f1f7",
            "color": COLORS["accent"],
            "text": "The defending champions were fierce to the end — Mbappe's hat-trick in the final made it the most dramatic World Cup final in history. France's 16 goals was the joint-highest of any team.",
        },
        {
            "team": "Croatia \U0001f1ed\U0001f1f7",
            "color": COLORS["accent"],
            "text": "Croatia confirmed their status as tournament stalwarts, claiming 3rd place for the second time in four editions. Solid defensive organisation and Modric's midfield vision were key.",
        },
        {
            "team": "Morocco \U0001f1f2\U0001f1e6",
            "color": COLORS["success"],
            "text": "The tournament's great story: Morocco became the first African and Arab nation to reach a World Cup semi-final, beating Spain and Portugal on the way.",
        },
    ]

    cards = [
        html.Div(
            className="chart-card",
            style={
                "borderLeft": f"4px solid {ins['color']}",
                "padding": "16px 20px",
                "flex": "1",
                "minWidth": "220px",
            },
            children=[
                html.Div(ins["team"], style={"fontWeight": "700", "fontSize": "15px",
                                             "marginBottom": "8px", "color": COLORS["text"]}),
                html.P(ins["text"], style={"fontSize": "13px", "color": COLORS["muted"],
                                           "margin": 0, "lineHeight": "1.6"}),
            ],
        )
        for ins in insights
    ]

    return html.Div(
        children=[
            html.H3("2022 World Cup — Key Storylines",
                    style={"fontSize": "18px", "fontWeight": "700",
                           "color": COLORS["text"], "marginBottom": "16px"}),
            html.Div(style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}, children=cards),
        ],
    )
