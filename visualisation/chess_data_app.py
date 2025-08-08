import streamlit as st
from visualisation_utils import load_data, show_key_metrics

st.title("Chess data visualisation")
username = st.text_input('Please enter your Chess.com username')
if username and st.button("Load chess data"):
    dataframe_games = load_data(username_input=username)
    if dataframe_games.empty:
        st.warning(f"No data for {username}")
    else:
        show_key_metrics(df=dataframe_games)

