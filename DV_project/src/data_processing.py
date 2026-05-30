import pandas as pd
import numpy as np

def load_and_clean_upsets_data():
    filepath = 'Data/international_matches.csv'
    df = pd.read_csv(filepath)

    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['home_goal_diff'] = df['home_team_score'] - df['away_team_score']
    df['rank_gap'] = df['home_team_fifa_rank'] - df['away_team_fifa_rank']

    conditions = [
        df['home_team_score'] > df['away_team_score'],
        df['home_team_score'] < df['away_team_score']
    ]
    
    df['winner'] = np.select(conditions, [df['home_team'], df['away_team']], default='Draw')
    df['winner_rank'] = np.select(conditions, [df['home_team_fifa_rank'], df['away_team_fifa_rank']], default=np.nan)
    df['loser_rank'] = np.select(conditions, [df['away_team_fifa_rank'], df['home_team_fifa_rank']], default=np.nan)

    # is_upset: Đội thắng có rank kém hơn đối thủ
    df['is_upset'] = np.where(
        (df['winner'] != 'Draw') & (df['winner_rank'] > df['loser_rank']),
        True,
        False
    )

    df['upset_rank_gap'] = np.where(df['is_upset'], df['winner_rank'] - df['loser_rank'], np.nan)

    # Format ngày tháng thành dạng chuỗi dễ đọc
    df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')
    
    # Label ngắn gọn chỉ dùng để in chữ lên cột của Bar chart
    df['match_short_label'] = df['home_team'] + ' ' + df['home_team_score'].astype(str) + ' - ' + df['away_team_score'].astype(str) + ' ' + df['away_team']

    return df