from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "Data"
ARCHIVE_DIR = DATA_DIR / "archive"
SUMMARY_PATH = ARCHIVE_DIR / "FIFA - World Cup Summary.csv"
INTERNATIONAL_MATCHES_PATH = DATA_DIR / "international_matches.csv"

TEAM_NORMALIZATION = {
    "West Germany": "Germany",
}


def normalize_team_name(value: object) -> object:
    if pd.isna(value):
        return value
    cleaned = str(value).strip()
    return TEAM_NORMALIZATION.get(cleaned, cleaned)


def _snake_case_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df


@lru_cache(maxsize=1)
def _load_world_cup_summary_cached() -> pd.DataFrame:
    df = pd.read_csv(SUMMARY_PATH)
    df = _snake_case_columns(df)
    df = df.rename(columns={"runner_up": "runner_up", "third_place": "third_place"})
    numeric_columns = ["year", "teams", "matches_played", "goals_scored", "avg_goals_per_game"]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["champion_norm"] = df["champion"].map(normalize_team_name)
    df["runner_up_norm"] = df["runner_up"].map(normalize_team_name)
    df["third_place_norm"] = df["third_place"].map(normalize_team_name)
    df["host_norm"] = df["host"].map(normalize_team_name)
    df["host_won"] = df["host_norm"] == df["champion_norm"]
    return df.sort_values("year").reset_index(drop=True)


def load_world_cup_summary() -> pd.DataFrame:
    return _load_world_cup_summary_cached().copy()


@lru_cache(maxsize=1)
def _load_world_cup_standings_cached() -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for path in sorted(ARCHIVE_DIR.glob("FIFA - *.csv")):
        if path.name == "FIFA - World Cup Summary.csv":
            continue
        year_text = path.stem.replace("FIFA - ", "")
        if not year_text.isdigit():
            continue

        df = pd.read_csv(path)
        df = _snake_case_columns(df)
        df["year"] = int(year_text)
        df["team_norm"] = df["team"].map(normalize_team_name)
        df["position_group"] = pd.cut(
            df["position"],
            bins=[0, 1, 4, 8, float("inf")],
            labels=["Champion", "Top 4", "Top 8", "Other"],
            include_lowest=True,
        ).astype(str)
        frames.append(df)

    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True).sort_values(["year", "position"]).reset_index(drop=True)


def load_world_cup_standings() -> pd.DataFrame:
    return _load_world_cup_standings_cached().copy()


@lru_cache(maxsize=1)
def _load_international_matches_cached() -> pd.DataFrame:
    df = pd.read_csv(INTERNATIONAL_MATCHES_PATH, parse_dates=["date"])
    df = _snake_case_columns(df)
    df["year"] = df["date"].dt.year
    df["home_team_norm"] = df["home_team"].map(normalize_team_name)
    df["away_team_norm"] = df["away_team"].map(normalize_team_name)
    df["home_goal_diff"] = df["home_team_score"] - df["away_team_score"]
    df["rank_gap"] = df["home_team_fifa_rank"] - df["away_team_fifa_rank"]
    return df


def load_international_matches() -> pd.DataFrame:
    return _load_international_matches_cached().copy()


@lru_cache(maxsize=1)
def _load_upsets_data_cached() -> pd.DataFrame:
    df = _load_international_matches_cached().copy()

    home_win = df["home_team_score"] > df["away_team_score"]
    away_win = df["home_team_score"] < df["away_team_score"]

    df["winner"] = "Draw"
    df.loc[home_win, "winner"] = df.loc[home_win, "home_team"]
    df.loc[away_win, "winner"] = df.loc[away_win, "away_team"]

    df["winner_rank"] = pd.NA
    df.loc[home_win, "winner_rank"] = df.loc[home_win, "home_team_fifa_rank"]
    df.loc[away_win, "winner_rank"] = df.loc[away_win, "away_team_fifa_rank"]

    df["loser_rank"] = pd.NA
    df.loc[home_win, "loser_rank"] = df.loc[home_win, "away_team_fifa_rank"]
    df.loc[away_win, "loser_rank"] = df.loc[away_win, "home_team_fifa_rank"]

    df["winner_rank"] = pd.to_numeric(df["winner_rank"], errors="coerce")
    df["loser_rank"] = pd.to_numeric(df["loser_rank"], errors="coerce")
    df["is_upset"] = (df["winner"] != "Draw") & (df["winner_rank"] > df["loser_rank"])
    df["upset_rank_gap"] = (df["winner_rank"] - df["loser_rank"]).where(df["is_upset"])
    df["date_str"] = df["date"].dt.strftime("%Y-%m-%d")
    df["match_short_label"] = (
        df["home_team"]
        + " "
        + df["home_team_score"].astype(str)
        + " - "
        + df["away_team_score"].astype(str)
        + " "
        + df["away_team"]
    )
    return df


def load_upsets_data() -> pd.DataFrame:
    return _load_upsets_data_cached().copy()
