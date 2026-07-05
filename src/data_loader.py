from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd


DEFAULT_RAW_PATHS = [
    Path('data/raw/players_data_light-2024_2025.csv'),
    Path('data/raw/players_data-2024_2025.csv'),
    Path('data/raw/all_player_stats.csv'),
]
SAMPLE_PATH = Path('data/sample/sample_players.csv')


def load_player_data(path: Optional[str | Path] = None, allow_sample: bool = True) -> pd.DataFrame:
    """Load ScoutIQ player data.

    The project is designed for a real player-statistics CSV placed in data/raw/.
    During early development, it falls back to a small sample file so the pipeline
    and Streamlit app can be tested before the final dataset is downloaded.
    """
    candidates = [Path(path)] if path else DEFAULT_RAW_PATHS

    for candidate in candidates:
        if candidate.exists():
            return pd.read_csv(candidate)

    if allow_sample and SAMPLE_PATH.exists():
        return pd.read_csv(SAMPLE_PATH)

    tried = ', '.join(str(p) for p in candidates)
    raise FileNotFoundError(
        f'No dataset found. Tried: {tried}. Place the Kaggle CSV in data/raw/ '
        f'or keep allow_sample=True to use {SAMPLE_PATH}.'
    )
