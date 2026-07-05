from __future__ import annotations

import pandas as pd
import streamlit as st

from src.data_loader import load_player_data
from src.preprocessing import clean_player_data
from src.scoring import rank_players


st.set_page_config(page_title='ScoutIQ MVP', layout='wide')
st.title('ScoutIQ — Football Scouting MVP')
st.caption('Early MVP: loads player data, applies basic filters, and produces an explainable baseline ranking.')

uploaded = st.file_uploader('Upload player stats CSV, or leave empty to use the local dataset/sample file.', type=['csv'])

if uploaded is not None:
    raw_df = pd.read_csv(uploaded)
    data_source = 'uploaded CSV'
else:
    raw_df = load_player_data(allow_sample=True)
    data_source = 'local raw dataset or sample fallback'

clean_df = clean_player_data(raw_df)

with st.sidebar:
    st.header('Shortlist filters')
    position_options = ['All'] + sorted([p for p in clean_df['PositionGroup'].dropna().unique().tolist() if p != 'Unknown'])
    selected_position = st.selectbox('Position group', position_options)
    min_minutes = st.slider('Minimum minutes', min_value=0, max_value=3000, value=500, step=100)
    use_age_filter = st.checkbox('Apply max age filter', value=False)
    max_age = st.slider('Maximum age', min_value=16, max_value=40, value=25) if use_age_filter else None

position_group = None if selected_position == 'All' else selected_position
ranked_df = rank_players(clean_df, position_group=position_group, min_minutes=min_minutes, max_age=max_age)

st.subheader('Current data status')
col1, col2, col3 = st.columns(3)
col1.metric('Data source', data_source)
col2.metric('Raw rows', len(raw_df))
col3.metric('Ranked rows', len(ranked_df))

st.subheader('Top ranked players')
main_cols = [
    'Player', 'Nation', 'Pos', 'PositionGroup', 'Squad', 'Comp', 'Age', 'Min',
    'Gls', 'Ast', 'npxG', 'xAG', 'PrgC', 'PrgP', 'Tkl', 'Int', 'Blocks', 'Clr',
    'SavePct', 'PSxGPlusMinus', 'ScoutIQScore', 'ScoreExplanation'
]
visible_cols = [c for c in main_cols if c in ranked_df.columns]
st.dataframe(ranked_df[visible_cols].head(30), use_container_width=True)

st.info(
    'Note: the current score is a transparent baseline, not the final ML model. '
    'It is useful for the interim MVP because it proves the data-loading, filtering, '
    'ranking, and explanation pipeline before advanced modelling is added.'
)
