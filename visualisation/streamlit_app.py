import streamlit as st

from visualisation_utils import load_data
st.title("Chess data visualisation")
username = st.text_input('Please enter your Chess.com username')
if username and st.button("Load chess data"):
    dataframe_games = load_data(username_input=username)
    st.header("Head of the dataframe")
    st.dataframe(dataframe_games.head())
    
