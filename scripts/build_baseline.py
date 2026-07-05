from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_player_data
from src.preprocessing import clean_player_data
from src.scoring import rank_players


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Build the ScoutIQ MVP baseline ranking file.')
    parser.add_argument('--input', type=str, default=None, help='Optional path to the raw player CSV.')
    parser.add_argument('--output', type=str, default='data/processed/scoutiq_ranked_players.csv')
    parser.add_argument('--min-minutes', type=int, default=500)
    parser.add_argument('--max-age', type=int, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw = load_player_data(args.input, allow_sample=True)
    clean = clean_player_data(raw)
    ranked = rank_players(clean, min_minutes=args.min_minutes, max_age=args.max_age)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ranked.to_csv(output_path, index=False)

    print(f'Loaded rows: {len(raw)}')
    print(f'Clean rows: {len(clean)}')
    print(f'Ranked rows: {len(ranked)}')
    print(f'Saved: {output_path}')
    cols = [c for c in ['Player', 'Pos', 'Squad', 'Comp', 'Age', 'Min', 'ScoutIQScore'] if c in ranked.columns]
    print(ranked[cols].head(10).to_string(index=False))


if __name__ == '__main__':
    main()
