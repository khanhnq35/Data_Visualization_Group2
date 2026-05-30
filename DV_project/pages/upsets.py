import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import numpy as np

from src.data_processing import load_and_clean_upsets_data

dash.register_page(__name__, path='/', name='Competitiveness & Upsets')

df = load_and_clean_upsets_data()

# --- COLOR PALETTE (HARMONIZED) ---
COLOR_UPSET = '#e15759'    # Đỏ nhạt / San hô đậm (Highlight hài hòa)
COLOR_NORMAL = '#94a3b8'   # Xám đá đậm (Giữ độ rõ nét khi giảm opacity)
COLOR_HOME = '#4f81bd'     # Xanh lam dịu
COLOR_AWAY = '#e15759'     # Đỏ nhạt (Đồng bộ với màu Upset)
COLOR_DRAW = '#cbd5e1'     # Xám nhạt
BG_PAGE = '#f8fafc'        
BORDER_COLOR = '#cbd5e1'   

# --- GENERAL STYLES ---
page_style = {'backgroundColor': BG_PAGE, 'minHeight': '100vh', 'padding': '15px 20px', 'boxSizing': 'border-box', 'fontFamily': 'Arial, sans-serif'}
card_style = {'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '8px', 'border': f'1px solid {BORDER_COLOR}', 'boxShadow': '0 2px 4px rgba(0,0,0,0.02)'}
kpi_style = {'textAlign': 'center', 'backgroundColor': 'white', 'padding': '12px 5px', 'borderRadius': '8px', 'border': f'1px solid {BORDER_COLOR}', 'boxShadow': '0 2px 4px rgba(0,0,0,0.02)', 'flex': '1', 'margin': '0 5px', 'borderTop': f'4px solid {COLOR_HOME}'}

layout = html.Div([

    html.H3("Competitiveness & Upsets: Is Football Unpredictable?", style={'textAlign': 'center', 'color': '#475569', 'margin': '0 0 15px 0'}),

    # --- FILTERS SECTION ---
    html.Div([
        html.Div([
            html.Div([html.Label("Year:", style={'fontWeight': 'bold', 'fontSize': '13px', 'color': '#64748b'})], style={'width': '5%'}),
            html.Div([
                dcc.RangeSlider(
                    id='upsets-year-slider',
                    min=df['year'].min(), max=df['year'].max(), step=1, value=[2000, 2022], 
                    marks={str(year): str(year) for year in range(df['year'].min(), df['year'].max()+1, 4)}
                )
            ], style={'width': '95%'})
        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
        
        html.Div([
            html.Div([html.Label("Tournament:", style={'fontSize': '12px', 'color': '#64748b'}), dcc.Dropdown(id='upsets-tournament-dropdown', placeholder="All Tournaments", style={'fontSize': '13px'})], style={'width': '24%'}),
            html.Div([html.Label("Team:", style={'fontSize': '12px', 'color': '#64748b'}), dcc.Dropdown(id='upsets-team-dropdown', placeholder="Select Team", style={'fontSize': '13px'})], style={'width': '24%'}),
            html.Div([html.Label("Continent:", style={'fontSize': '12px', 'color': '#64748b'}), dcc.Dropdown(id='upsets-continent-dropdown', placeholder="Select Continent", style={'fontSize': '13px'})], style={'width': '24%'}),
            html.Div([
                html.Label("Match Type:", style={'fontSize': '12px', 'color': '#64748b'}),
                dcc.Dropdown(
                    id='upsets-match-type-dropdown',
                    options=[{'label': 'All', 'value': 'All'}, {'label': 'Shoot-out', 'value': 'Shootout'}, {'label': 'Neutral Location', 'value': 'Neutral'}], value='All', style={'fontSize': '13px'}
                )
            ], style={'width': '24%'})
        ], style={'display': 'flex', 'justifyContent': 'space-between'})
    ], style={**card_style, 'marginBottom': '15px'}),
    
    # --- KPI CARDS ---
    html.Div(id='upsets-kpi-row', style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '15px'}),
    
    # --- CHARTS AREA ---
    html.Div([
        # LEFT COLUMN
        html.Div([
            html.Div([
                html.H5("Rank Gap vs Goal Difference", style={'textAlign': 'center', 'margin': '0', 'color': '#475569'}),
                html.Div("Note: Rank Gap = (Home Rank - Away Rank) | Goal Diff = (Home Goals - Away Goals)", style={'fontSize': '11px', 'color': '#94a3b8', 'textAlign': 'center', 'marginBottom': '5px'}),
                dcc.Graph(id='upsets-scatter-plot', style={'flex': '1'}, config={'displayModeBar': False})
            ], style={**card_style, 'flex': '1', 'marginBottom': '15px', 'display': 'flex', 'flexDirection': 'column'}),
            
            html.Div(
                id='upsets-detail-container', 
                style={**card_style, 'height': '65px', 'padding': '10px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'backgroundColor': '#fef3c7'}
            )
        ], style={'width': '58%', 'display': 'flex', 'flexDirection': 'column'}),
        
        # RIGHT COLUMN
        html.Div([
            html.Div([
                html.H5("Top 5 Biggest Upsets", style={'textAlign': 'center', 'margin': '0 0 10px 0', 'color': '#475569'}),
                dcc.Graph(id='upsets-bar-chart', style={'flex': '1'}, config={'displayModeBar': False})
            ], style={**card_style, 'flex': '1', 'marginBottom': '15px', 'display': 'flex', 'flexDirection': 'column'}),
            
            html.Div([
                html.H5("Result by Neutral Location", style={'textAlign': 'center', 'margin': '0 0 10px 0', 'color': '#475569'}),
                dcc.Graph(id='upsets-stacked-bar', style={'flex': '1'}, config={'displayModeBar': False})
            ], style={**card_style, 'flex': '1', 'display': 'flex', 'flexDirection': 'column'})
        ], style={'width': '40.5%', 'display': 'flex', 'flexDirection': 'column'})
        
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'height': '62vh'})

], style=page_style)

# --- CALLBACK 1: CROSS-FILTERING ---
@callback(
    [Output('upsets-tournament-dropdown', 'options'),
     Output('upsets-team-dropdown', 'options'),
     Output('upsets-continent-dropdown', 'options')],
    [Input('upsets-year-slider', 'value'),
     Input('upsets-tournament-dropdown', 'value'),
     Input('upsets-team-dropdown', 'value'),
     Input('upsets-continent-dropdown', 'value')]
)
def update_dropdown_options(year_range, tournament, team, continent):
    temp_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    t_df, tm_df, c_df = temp_df.copy(), temp_df.copy(), temp_df.copy()
    
    if team: t_df = t_df[(t_df['home_team'] == team) | (t_df['away_team'] == team)]
    if continent: t_df = t_df[(t_df['home_team_continent'] == continent) | (t_df['away_team_continent'] == continent)]
    if tournament: tm_df = tm_df[tm_df['tournament'] == tournament]
    if continent: tm_df = tm_df[(tm_df['home_team_continent'] == continent) | (tm_df['away_team_continent'] == continent)]
    if tournament: c_df = c_df[c_df['tournament'] == tournament]
    if team: c_df = c_df[(c_df['home_team'] == team) | (c_df['away_team'] == team)]
    
    t_opts = [{'label': t, 'value': t} for t in sorted(t_df['tournament'].dropna().unique())]
    tm_opts = [{'label': t, 'value': t} for t in sorted(pd.concat([tm_df['home_team'], tm_df['away_team']]).dropna().unique())]
    c_opts = [{'label': c, 'value': c} for c in sorted(pd.concat([c_df['home_team_continent'], c_df['away_team_continent']]).dropna().unique())]
    
    return t_opts, tm_opts, c_opts

# --- CALLBACK 2: UPDATE GRAPHS & KPIS ---
@callback(
    [Output('upsets-scatter-plot', 'figure'),
     Output('upsets-bar-chart', 'figure'),
     Output('upsets-stacked-bar', 'figure'),
     Output('upsets-kpi-row', 'children')],
    [Input('upsets-year-slider', 'value'),
     Input('upsets-tournament-dropdown', 'value'),
     Input('upsets-team-dropdown', 'value'),
     Input('upsets-continent-dropdown', 'value'),
     Input('upsets-match-type-dropdown', 'value')]
)
def update_graphs(year_range, tournament, team, continent, match_type):
    filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])].copy()
    
    if tournament: filtered_df = filtered_df[filtered_df['tournament'] == tournament]
    if team: filtered_df = filtered_df[(filtered_df['home_team'] == team) | (filtered_df['away_team'] == team)]
    if continent: filtered_df = filtered_df[(filtered_df['home_team_continent'] == continent) | (filtered_df['away_team_continent'] == continent)]
    if match_type == 'Shootout': filtered_df = filtered_df[filtered_df['shoot_out'].isin([True, 'Yes', 'True', 1, 'yes'])]
    elif match_type == 'Neutral': filtered_df = filtered_df[filtered_df['neutral_location'].isin([True, 'True', 1, 'yes', 'Yes'])]

    if filtered_df.empty:
        empty_fig = px.scatter(title="No Data Available").update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        return empty_fig, empty_fig, empty_fig, html.Div()

    # --- KPI CALCULATION ---
    total_matches = len(filtered_df)
    home_wins = len(filtered_df[filtered_df['home_team_score'] > filtered_df['away_team_score']])
    draws = len(filtered_df[filtered_df['home_team_score'] == filtered_df['away_team_score']])
    away_wins = total_matches - home_wins - draws
    
    neutral_matches = len(filtered_df[filtered_df['neutral_location'].isin([True, 'True', 1, 'yes', 'Yes'])])
    shootout_matches = len(filtered_df[filtered_df['shoot_out'].isin([True, 'Yes', 'True', 1, 'yes'])])
    
    home_win_rate = (home_wins / total_matches) * 100 if total_matches > 0 else 0
    draw_rate = (draws / total_matches) * 100 if total_matches > 0 else 0
    away_win_rate = (away_wins / total_matches) * 100 if total_matches > 0 else 0

    kpi_cards = [
        html.Div([html.H4(f"{total_matches:,}", style={'margin': '0 0 5px 0', 'color': '#334155'}), html.P("Total Matches", style={'color': '#94a3b8', 'fontSize': '12px', 'margin': '0'})], style=kpi_style),
        html.Div([html.H4(f"{home_win_rate:.1f}%", style={'margin': '0 0 5px 0', 'color': '#334155'}), html.P("Home Win Rate", style={'color': '#94a3b8', 'fontSize': '12px', 'margin': '0'})], style=kpi_style),
        html.Div([html.H4(f"{draw_rate:.1f}%", style={'margin': '0 0 5px 0', 'color': '#334155'}), html.P("Draw Rate", style={'color': '#94a3b8', 'fontSize': '12px', 'margin': '0'})], style=kpi_style),
        html.Div([html.H4(f"{away_win_rate:.1f}%", style={'margin': '0 0 5px 0', 'color': '#334155'}), html.P("Away Win Rate", style={'color': '#94a3b8', 'fontSize': '12px', 'margin': '0'})], style=kpi_style),
        html.Div([html.H4(f"{neutral_matches:,}", style={'margin': '0 0 5px 0', 'color': '#334155'}), html.P("Neutral Matches", style={'color': '#94a3b8', 'fontSize': '12px', 'margin': '0'})], style=kpi_style),
        html.Div([html.H4(f"{shootout_matches:,}", style={'margin': '0 0 5px 0', 'color': '#334155'}), html.P("Shoot-out", style={'color': '#94a3b8', 'fontSize': '12px', 'margin': '0'})], style=kpi_style)
    ]

    custom_data_cols = ['date_str', 'tournament', 'home_team', 'home_team_fifa_rank', 'home_team_score', 'away_team_score', 'away_team_fifa_rank', 'away_team', 'upset_rank_gap']
    
    # 1. SCATTER PLOT
    fig_scatter = px.scatter(
        filtered_df, x='rank_gap', y='home_goal_diff', color='is_upset',
        color_discrete_map={True: COLOR_UPSET, False: COLOR_NORMAL}, custom_data=custom_data_cols,
        labels={'rank_gap': 'Rank Gap', 'home_goal_diff': 'Goal Difference'}
    )
    fig_scatter.update_traces(
        hovertemplate="<b>%{customdata[0]} | %{customdata[1]}</b><br>%{customdata[2]} (Rank %{customdata[3]}) <b>%{customdata[4]} - %{customdata[5]}</b> %{customdata[7]} (Rank %{customdata[6]})<br>Rank Gap: %{x}<br>Goal Diff: %{y}<extra></extra>",
        marker=dict(size=7, line=dict(width=0.5, color='white'))
    )
    # Tinh chỉnh lại opacity để chấm xám nổi rõ hơn nhưng không đè chấm Upset
    fig_scatter.for_each_trace(lambda trace: trace.update(opacity=0.45) if trace.name == 'False' else trace.update(opacity=0.9))
    fig_scatter.update_layout(
        template='plotly_white', legend_title="Is Upset?", margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )
    fig_scatter.add_hline(y=0, line_dash="dash", line_color=BORDER_COLOR, opacity=0.8)
    fig_scatter.add_vline(x=0, line_dash="dash", line_color=BORDER_COLOR, opacity=0.8)

    # 2. BAR CHART (Căn lề chữ & Thêm lưới trục X)
    upsets_df = filtered_df[filtered_df['is_upset'] == True]
    top_upsets = upsets_df.sort_values(by='upset_rank_gap', ascending=False).head(5).copy()
    
    fig_bar = px.bar(
        top_upsets, x='upset_rank_gap', y='match_short_label', orientation='h',
        text='match_short_label', custom_data=custom_data_cols, color_discrete_sequence=[COLOR_UPSET]
    )
    fig_bar.update_traces(
        textposition='inside', 
        insidetextanchor='start', # Neo chữ sát về bên trái của cột
        textfont=dict(size=12, color='white', weight='bold'),
        hovertemplate="<b>%{customdata[0]} | %{customdata[1]}</b><br>%{customdata[2]} (Rank %{customdata[3]}) <b>%{customdata[4]} - %{customdata[5]}</b> %{customdata[7]} (Rank %{customdata[6]})<br>Upset Rank Gap: %{customdata[8]}<extra></extra>"
    )
    fig_bar.update_layout(
        template='plotly_white', 
        yaxis={'title': '', 'categoryorder':'total ascending', 'showticklabels': False},
        # Bật lưới gridline cho trục X để dễ đối chiếu mốc 50, 100, 150
        xaxis={'title': 'Rank Gap', 'visible': True, 'showticklabels': True, 'showgrid': True, 'gridcolor': '#e2e8f0'}, 
        margin=dict(l=10, r=15, t=10, b=30), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )

    # 3. STACKED BAR CHART
    conditions = [filtered_df['home_team_score'] > filtered_df['away_team_score'], filtered_df['home_team_score'] < filtered_df['away_team_score']]
    filtered_df['match_result'] = np.select(conditions, ['Home Win', 'Away Win'], default='Draw')
    filtered_df['neutral_label'] = filtered_df['neutral_location'].map({False: 'Home/Away', True: 'Neutral Location'})
    
    counts = filtered_df.groupby(['neutral_label', 'match_result']).size().reset_index(name='count')
    totals = counts.groupby('neutral_label')['count'].transform('sum')
    counts['percentage'] = (counts['count'] / totals) * 100
    counts['text_label'] = counts['percentage'].round(1).astype(str) + '%'
    
    fig_stacked = px.bar(
        counts, x='neutral_label', y='percentage', color='match_result',
        text='text_label', custom_data=['count'],
        color_discrete_map={'Home Win': COLOR_HOME, 'Away Win': COLOR_AWAY, 'Draw': COLOR_DRAW},
        labels={'neutral_label': '', 'percentage': 'Percentage (%)', 'match_result': 'Result'}
    )
    fig_stacked.update_traces(
        textfont=dict(color='white'),
        hovertemplate="Location: %{x}<br>Result: %{color}<br>Percentage: %{y:.1f}%<br>Matches: %{customdata[0]}<extra></extra>"
    )
    
    totals_df = counts.groupby('neutral_label')['count'].sum().reset_index()
    for _, row in totals_df.iterrows():
        fig_stacked.add_annotation(
            x=row['neutral_label'], y=100, yshift=12, 
            text=f"Total: {row['count']:,}",
            showarrow=False, font=dict(size=11, color='#64748b', weight='bold')
        )

    fig_stacked.update_layout(
        template='plotly_white', 
        xaxis={'tickfont': dict(size=11, color='#64748b')}, 
        yaxis={'title': '', 'visible': False, 'range': [0, 110]}, 
        margin=dict(l=10, r=10, t=10, b=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )

    return fig_scatter, fig_bar, fig_stacked, kpi_cards

# --- CALLBACK 3: DETAIL PANEL ---
@callback(
    Output('upsets-detail-container', 'children'),
    [Input('upsets-scatter-plot', 'clickData'),
     Input('upsets-bar-chart', 'clickData')]
)
def display_click_data(scatter_click, bar_click):
    ctx = dash.callback_context
    default_msg = html.Div([
        html.Div("🔍 SELECTED MATCH DETAILS", style={'fontSize': '11px', 'color': '#d97706', 'fontWeight': 'bold', 'letterSpacing': '1px', 'marginBottom': '3px'}),
        html.Div("🖱️ Click on a match in the charts to view details...", style={'color': '#94a3b8', 'fontSize': '13px', 'fontStyle': 'italic'})
    ], style={'textAlign': 'center', 'width': '100%'})
    
    if not ctx.triggered: return default_msg
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    click_data = scatter_click if trigger_id == 'upsets-scatter-plot' else bar_click
    
    if click_data:
        cd = click_data['points'][0]['customdata']
        date_str, tournament, home_team, home_rank, home_score, away_score, away_rank, away_team, upset_gap = cd
        
        return html.Div([
            html.Div("🔍 SELECTED MATCH DETAILS", style={'fontSize': '11px', 'color': '#d97706', 'fontWeight': 'bold', 'letterSpacing': '1px', 'marginBottom': '3px'}),
            html.Div([
                html.Span(f"🏆 {tournament} ({date_str})", style={'color': '#64748b', 'fontWeight': 'bold', 'marginRight': '25px', 'fontSize': '13px'}),
                html.Span(f"{home_team} (Rank {home_rank})", style={'color': '#334155', 'fontSize': '15px'}),
                html.Span(f" {home_score} - {away_score} ", style={'color': COLOR_UPSET, 'fontWeight': '900', 'fontSize': '22px', 'margin': '0 15px', 'letterSpacing': '2px'}),
                html.Span(f"{away_team} (Rank {away_rank})", style={'color': '#334155', 'fontSize': '15px'})
            ])
        ], style={'textAlign': 'center', 'width': '100%'})
        
    return default_msg