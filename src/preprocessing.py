from __future__ import annotations

import re
from typing import Iterable

import numpy as np
import pandas as pd


BASE_COLUMNS = ['Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 'Min']
NUMERIC_HINTS = [
    'Age', 'Min', '90s', 'Gls', 'Ast', 'G+A', 'npxG', 'xG', 'xAG', 'xA',
    'PrgC', 'PrgP', 'Tkl', 'Tackles', 'Int', 'Interceptions', 'Blocks', 'Clr',
    'SavePct', 'Save%', 'PSxGPlusMinus', 'PSxG+/-'
]


def normalise_column_name(name: str) -> str:
    """Make common football-stat column names easier to use in code."""
    cleaned = str(name).strip()
    cleaned = cleaned.replace(' ', '')
    cleaned = cleaned.replace('%', 'Pct')
    cleaned = cleaned.replace('+/-', 'PlusMinus')
    cleaned = cleaned.replace('/', '_')
    cleaned = re.sub(r'[^0-9a-zA-Z_+.-]', '', cleaned)
    return cleaned


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten multi-index style columns that sometimes appear in FBref exports."""
    out = df.copy()
    out.columns = [normalise_column_name(c[-1] if isinstance(c, tuple) else c) for c in out.columns]
    return out


def coerce_numeric(df: pd.DataFrame, columns: Iterable[str] | None = None) -> pd.DataFrame:
    out = df.copy()
    target_cols = list(columns) if columns else list(out.columns)
    for col in target_cols:
        if col in out.columns and (col in NUMERIC_HINTS or out[col].dtype == object):
            converted = pd.to_numeric(out[col].astype(str).str.replace(',', '', regex=False), errors='coerce')
            # Only replace object columns when the conversion produced useful numeric values.
            if converted.notna().sum() > 0 and col not in ['Player', 'Nation', 'Pos', 'Squad', 'Comp']:
                out[col] = converted
    return out


def add_position_group(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if 'Pos' not in out.columns:
        out['Pos'] = 'Unknown'

    def group_position(pos: object) -> str:
        text = str(pos).upper()
        if 'GK' in text:
            return 'GK'
        if any(token in text for token in ['DF', 'CB', 'FB', 'LB', 'RB']):
            return 'DF'
        if any(token in text for token in ['MF', 'DM', 'CM', 'AM']):
            return 'MF'
        if any(token in text for token in ['FW', 'ST', 'LW', 'RW']):
            return 'FW'
        return 'Unknown'

    out['PositionGroup'] = out['Pos'].apply(group_position)
    return out


def clean_player_data(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning used by the MVP baseline."""
    out = flatten_columns(df)
    out = coerce_numeric(out)
    out = add_position_group(out)

    if 'Min' in out.columns:
        out = out[out['Min'].fillna(0) > 0].copy()

    if 'Player' in out.columns:
        out = out.drop_duplicates(subset=['Player', 'Squad', 'Comp', 'Pos'], keep='first')

    return out.reset_index(drop=True)
