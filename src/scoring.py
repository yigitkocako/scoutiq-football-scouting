from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


@dataclass(frozen=True)
class FeatureWeight:
    feature: str
    weight: float


# MVP baseline: transparent weighted score by broad position group.
# These are deliberately simple and explainable for the interim version.
POSITION_WEIGHTS: Dict[str, List[FeatureWeight]] = {
    'FW': [
        FeatureWeight('Gls', 0.30),
        FeatureWeight('npxG', 0.25),
        FeatureWeight('Ast', 0.15),
        FeatureWeight('xAG', 0.15),
        FeatureWeight('PrgC', 0.10),
        FeatureWeight('PrgP', 0.05),
    ],
    'MF': [
        FeatureWeight('Ast', 0.20),
        FeatureWeight('xAG', 0.20),
        FeatureWeight('PrgP', 0.25),
        FeatureWeight('PrgC', 0.10),
        FeatureWeight('Tkl', 0.15),
        FeatureWeight('Int', 0.10),
    ],
    'DF': [
        FeatureWeight('Tkl', 0.25),
        FeatureWeight('Int', 0.25),
        FeatureWeight('Blocks', 0.20),
        FeatureWeight('Clr', 0.15),
        FeatureWeight('PrgP', 0.15),
    ],
    'GK': [
        FeatureWeight('SavePct', 0.55),
        FeatureWeight('PSxGPlusMinus', 0.45),
    ],
}

ALIASES = {
    'Tkl': ['Tkl', 'Tackles'],
    'Int': ['Int', 'Interceptions'],
    'SavePct': ['SavePct', 'Save%'],
    'PSxGPlusMinus': ['PSxGPlusMinus', 'PSxG+/-'],
    'xAG': ['xAG', 'xA'],
    'npxG': ['npxG', 'xG'],
}


def resolve_feature(df: pd.DataFrame, feature: str) -> Optional[str]:
    """Return the available column matching a desired feature."""
    candidates = ALIASES.get(feature, [feature])
    for candidate in candidates:
        if candidate in df.columns:
            return candidate
    return None


def available_weighted_features(df: pd.DataFrame, position_group: str) -> List[FeatureWeight]:
    result: List[FeatureWeight] = []
    for fw in POSITION_WEIGHTS.get(position_group, []):
        resolved = resolve_feature(df, fw.feature)
        if resolved is not None:
            result.append(FeatureWeight(resolved, fw.weight))
    return result


def _scale_features(df: pd.DataFrame, features: Iterable[str]) -> pd.DataFrame:
    out = df.copy()
    cols = list(features)
    if not cols:
        out['ScoutIQScore'] = 0.0
        return out

    values = out[cols].apply(pd.to_numeric, errors='coerce').fillna(0)
    if len(out) > 1:
        scaled = MinMaxScaler().fit_transform(values)
    else:
        scaled = np.ones((len(out), len(cols)))
    scaled_df = pd.DataFrame(scaled, columns=[f'{c}_scaled' for c in cols], index=out.index)
    return pd.concat([out, scaled_df], axis=1)


def score_position_group(df: pd.DataFrame, position_group: str) -> pd.DataFrame:
    subset = df[df['PositionGroup'] == position_group].copy()
    if subset.empty:
        return subset

    weights = available_weighted_features(subset, position_group)
    if not weights:
        subset['ScoutIQScore'] = 0.0
        subset['ScoreExplanation'] = 'No matching scoring features available yet.'
        return subset

    subset = _scale_features(subset, [w.feature for w in weights])
    total_weight = sum(w.weight for w in weights) or 1.0
    score = np.zeros(len(subset))
    explanation_parts = []
    for w in weights:
        scaled_col = f'{w.feature}_scaled'
        score += subset[scaled_col].to_numpy() * (w.weight / total_weight)
        explanation_parts.append(f'{w.feature}={w.weight:.2f}')

    subset['ScoutIQScore'] = (score * 100).round(2)
    subset['ScoreExplanation'] = '; '.join(explanation_parts)
    return subset


def rank_players(
    df: pd.DataFrame,
    position_group: Optional[str] = None,
    min_minutes: int = 500,
    max_age: Optional[int] = None,
) -> pd.DataFrame:
    """Create an explainable baseline player ranking for the MVP."""
    working = df.copy()
    if 'Min' in working.columns:
        working = working[working['Min'].fillna(0) >= min_minutes]
    if max_age is not None and 'Age' in working.columns:
        working = working[working['Age'].fillna(999) <= max_age]
    if position_group:
        working = working[working['PositionGroup'] == position_group]

    scored_groups = []
    groups = [position_group] if position_group else ['FW', 'MF', 'DF', 'GK']
    for group in groups:
        scored_groups.append(score_position_group(working, group))

    scored = pd.concat(scored_groups, ignore_index=True) if scored_groups else working
    if 'ScoutIQScore' not in scored.columns:
        scored['ScoutIQScore'] = 0.0
    return scored.sort_values('ScoutIQScore', ascending=False).reset_index(drop=True)
