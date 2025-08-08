import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
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

def show_key_metrics(df: pd.DataFrame):
    st.header("Head of the dataframe")
    st.metric(label="Number of games", value=len(df))
    st.dataframe(df.head())
    st.write("Average rating of opponents")
    column11, column12, column13 = st.columns(3)
    avg_rating_all_time_class=round(df.groupby(['time_class'])['player_rating'].mean())
    with column11:
        st.metric(label="Blitz", value=avg_rating_all_time_class['blitz'])
    with column12:
        st.metric(label="Bullet", value=avg_rating_all_time_class['bullet'])
    with column13:
        st.metric(label="Rapid", value=avg_rating_all_time_class['rapid'])
    st.dataframe(avg_rating_all_time_class)
    
    st.subheader('Games results')
    fig, ax=plt.subplots(figsize=(3,3))
    sns.countplot(x="player_result", data=df, order=df['player_result'].value_counts().index, ax=ax)
    ax.set_title('Results distribution')
    ax.set_xlabel("Results")
    ax.set_ylabel("Games count")
    st.pyplot(fig)