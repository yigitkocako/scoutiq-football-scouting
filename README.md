# ScoutIQ — AI/ML Football Scouting MVP

ScoutIQ is an AI/ML-supported football scouting project for identifying and ranking players using real performance data. The MVP focuses on a practical pipeline: load player data, clean it, apply position/criteria filters, and produce an explainable ranked shortlist.

## Current interim status

This repository is a starter implementation for the interim report stage. It includes:

- a planned data workflow for real Big 5 European league player statistics;
- a sample dataset for testing the pipeline before the final dataset is downloaded;
- cleaning and preprocessing scripts;
- a transparent baseline scoring model by position group;
- a basic Streamlit MVP interface;
- a command-line script that outputs a ranked player CSV.

The current ranking is intentionally a baseline, not the final model. It is used to prove that the MVP pipeline is working before more advanced ML or similarity modelling is added.

## Recommended dataset

Primary MVP dataset:

- **Football Players Stats (2024–2025)** by Hubert Sidorowicz on Kaggle.
- It contains player statistics from the 2024–2025 season across the Big 5 European leagues, sourced from FBref.
- The lighter CSV is suitable for a first MVP because it contains key attacking, passing, defending, and goalkeeping features.

Suggested filename after download:

```text
data/raw/players_data_light-2024_2025.csv
```

Backup/extension options:

- European Top Football Leagues Player Stats 25–26: useful for updated player profiles and market value-style attributes.
- StatsBomb Open Data: useful as a later event-level extension, but more complex than needed for the Week 7 MVP.
- Football-Data.co.uk: useful for match-level historical context, but less suitable for player-level scouting.

## Project structure

```text
scoutiq_starter_repo/
├── data/
│   ├── raw/                  # place downloaded real datasets here
│   ├── processed/            # generated outputs
│   └── sample/               # small sample file for early testing
├── docs/
│   └── interim_notes_draft.md
├── notebooks/
│   └── 01_data_exploration.ipynb
├── reports/
│   └── figures/
├── scripts/
│   └── build_baseline.py
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   └── scoring.py
├── streamlit_app.py
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
# .venv\Scripts\activate       # Windows PowerShell
pip install -r requirements.txt
```

## Run the baseline pipeline

Before the final dataset is downloaded, this command uses the small sample dataset:

```bash
python scripts/build_baseline.py
```

After downloading the Kaggle dataset, place it in `data/raw/` and run:

```bash
python scripts/build_baseline.py --input data/raw/players_data_light-2024_2025.csv
```

Output:

```text
data/processed/scoutiq_ranked_players.csv
```

## Run the MVP interface

```bash
streamlit run streamlit_app.py
```

## MVP requirement mapping

| Requirement | MVP status | Notes |
|---|---|---|
| Load real player data | In progress | Primary source selected; local sample included for testing. |
| Clean and preprocess player data | In progress | Basic cleaning, type conversion, position grouping, and duplicate handling implemented. |
| Filter players by position/criteria | In progress | Position, minutes, and age filters included in Streamlit MVP. |
| Produce a ranked player shortlist | In progress | Baseline weighted scoring implemented by broad position group. |
| Explain recommendation/ranking logic | In progress | ScoreExplanation column records feature weights used in baseline. |
| Similarity recommender | Not yet started | Planned after the baseline ranking pipeline is stable. |
| Visual comparison/radar chart | Not yet started | Could be added after real dataset is loaded. |
| Final evaluation | Not yet started | Will compare baseline output against expected position-specific scouting criteria. |

## Notes for final development

Potential next steps:

1. Download the real Big 5 player dataset and place it in `data/raw/`.
2. Confirm actual column names and update feature mappings if needed.
3. Add a similarity model using cosine similarity or nearest neighbours.
4. Add evaluation metrics and manual sanity checks for top-ranked players.
5. Replace the baseline score with a stronger model only if it remains explainable and useful.
