# Interim report notes — ScoutIQ

## Evidence / current state wording

At the interim stage, the project repository has been created and the initial MVP pipeline has been scaffolded. The current implementation includes a data loading module, preprocessing functions, position grouping, a transparent baseline ranking/scoring function, and a simple Streamlit interface for filtering and displaying ranked players. A small sample dataset is included only to test the code pipeline; the planned production dataset is a Big 5 European leagues player-statistics CSV downloaded separately from Kaggle.

## Dataset status wording

The primary dataset selected for the MVP is a player-level Big 5 European leagues dataset for the 2024/25 season. It is suitable for the Week 7 MVP because it contains player-level performance features across attacking, passing, defending, and goalkeeping categories. This aligns with the project requirement to use real football performance data rather than subjective overall ratings. The next step is to download the CSV, place it in the repository under `data/raw/`, validate the column names, and run the baseline pipeline on the full dataset.

## Baseline model status wording

The current baseline is an explainable weighted scoring model rather than a final ML model. This is intentional for the MVP because it allows the project to demonstrate a complete end-to-end scouting workflow: data loading, cleaning, filtering, ranking, and explanation. Once the data pipeline is stable, a similarity-based recommender using cosine similarity or nearest neighbours can be added as the main AI/ML component.

## Screenshot suggestion

For the interim report screenshot, use one of the following:

1. Streamlit app showing the ScoutIQ title, filters, and ranked player table.
2. Jupyter notebook showing loaded data, cleaned data shape, and top-ranked players.
3. GitHub repository view showing README, src/, scripts/, notebooks/, and data/ folders.

Use the sample screenshot only if clearly labelled as an early pipeline test, not as final real-data output.
