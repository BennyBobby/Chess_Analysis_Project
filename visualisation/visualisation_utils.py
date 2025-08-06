import streamlit as st
import pandas as pd
import os
DATA_DIR = '../data/transformed'
@st.cache_data 
def load_data(username_input: str) -> pd.DataFrame:
    filepath = os.path.join(DATA_DIR, username_input, f"{username_input}_transformed_games.csv")
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath)
            df['opening'] = df['opening'].fillna('N/A')
            df['player_color'] = df['player_color'].astype('category')
            df['player_result'] = df['player_result'].astype('category')
            df['time_class'] = df['time_class'].astype('category')
            df['rated'] = df['rated'].astype(bool)
            
            st.success(f"Loaded Data from '{username_input}' ({len(df)} game(s).")
            return df
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error(f"No data found from : {filepath}")
    
    st.warning("No data loaded.")
    return pd.DataFrame()