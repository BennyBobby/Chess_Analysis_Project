import streamlit as st
from visualisation_utils import load_data, show_key_metrics

st.title("Chess data visualisation")
username = st.text_input('Please enter your Chess.com username')
if username:
    dataframe_games = load_data(username_input=username)
    if dataframe_games.empty:
        st.warning(f"No data for {username}")
    else:
        first_game_date=dataframe_games['date'].min().to_pydatetime()
        last_game_date=dataframe_games['date'].max().to_pydatetime()
        date_range=st.slider("Select date range", 
                             min_value=first_game_date,
                             max_value=last_game_date,
                             value=(first_game_date, last_game_date), 
                             format="YYYY-MM-DD"
                             )
        start_date, end_date=date_range
        dataframe_games_filtered = dataframe_games[(dataframe_games['date'] >= start_date) & (dataframe_games['date'] <= end_date)].copy()
        if dataframe_games_filtered.empty:
            st.warning("No data found within the selected date range.")
            st.stop() 
        
        show_key_metrics(df=dataframe_games_filtered)