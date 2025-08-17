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
    st.dataframe(df.head())
    st.metric(label="Number of games", value=len(df))
    st.write("Average rating of opponents")
    column11, column12, column13 = st.columns(3)
    avg_rating_all_time_class=round(df.groupby(['time_class'])['opponent_rating'].mean())
    with column11:
        st.metric(label="Blitz", value=avg_rating_all_time_class['blitz'])
    with column12:
        st.metric(label="Bullet", value=avg_rating_all_time_class['bullet'])
    with column13:
        st.metric(label="Rapid", value=avg_rating_all_time_class['rapid'])
    
    st.subheader('Game results')
    tab11, tab12, tab13 = st.tabs(["Blitz", "Bullet", "Rapid"])
    df_blitz = df[df['time_class'] == 'blitz']
    df_bullet = df[df['time_class'] == 'bullet']
    df_rapid = df[df['time_class'] == 'rapid']
    with tab11:
        if df_blitz.empty:
            st.warning("No Blitz Data")
            return
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(x="player_result", data=df_blitz, order=df_blitz['player_result'].value_counts().index, palette='Set2', ax=ax)
        ax.set_title('Distribution of Blitz Results')
        ax.set_xlabel("Results")
        ax.set_ylabel("Number of games")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
    with tab12:
        if df_bullet.empty:
            st.warning("No Bullet Data")
            return
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(x="player_result", data=df_bullet, order=df_bullet['player_result'].value_counts().index, palette='Set2', ax=ax)
        ax.set_title('Distribution of Bullet Results')
        ax.set_xlabel("Results")
        ax.set_ylabel("Number of games")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
    with tab13:
        if df_rapid.empty:
            st.warning("No Rapid Data")
            return
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(x="player_result", data=df_rapid, order=df_rapid['player_result'].value_counts().index, palette='Set2', ax=ax)
        ax.set_title('Distribution of Rapid Results')
        ax.set_xlabel("Results")
        ax.set_ylabel("Number of games")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)

    st.subheader('Ratings Evolution')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df_blitz_monthly = df.loc[df['time_class'] == 'blitz', ['date', 'player_rating']].copy()
    df_blitz_monthly['month'] = df_blitz_monthly['date'].dt.to_period('M')
    df_blitz_monthly = df_blitz_monthly.groupby('month')['player_rating'].mean().reset_index()
    df_blitz_monthly['month'] = df_blitz_monthly['month'].astype(str)

    df_bullet_monthly = df.loc[df['time_class'] == 'bullet', ['date', 'player_rating']].copy()
    df_bullet_monthly['month'] = df_bullet_monthly['date'].dt.to_period('M')
    df_bullet_monthly = df_bullet_monthly.groupby('month')['player_rating'].mean().reset_index()
    df_bullet_monthly['month'] = df_bullet_monthly['month'].astype(str)

    df_rapid_monthly = df.loc[df['time_class'] == 'rapid', ['date', 'player_rating']].copy()
    df_rapid_monthly['month'] = df_rapid_monthly['date'].dt.to_period('M')
    df_rapid_monthly = df_rapid_monthly.groupby('month')['player_rating'].mean().reset_index()
    df_rapid_monthly['month'] = df_rapid_monthly['month'].astype(str)

    col21, col22, col23 = st.columns(3)
    with col21:
        blitz_button = st.button('Blitz')
    with col22:
        bullet_button = st.button('Bullet')
    with col23:
        rapid_button = st.button('Rapid')
    if blitz_button:
        st.markdown("Blitz Rating")
        if not df_blitz_monthly.empty:
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.lineplot(x='month', y='player_rating', data=df_blitz_monthly, marker='o', ax=ax)
            ax.set_title('Blitz Rating')
            ax.set_xlabel('Month')
            ax.set_ylabel('Average rating per month')
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            plt.xticks(rotation=40)
            st.pyplot(fig)
        else:
            st.warning("No Blitz Data")

    elif bullet_button:
        st.markdown("Bullet Rating")
        if not df_bullet_monthly.empty:
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.lineplot(x='month', y='player_rating', data=df_bullet_monthly, marker='o', ax=ax)
            ax.set_title('Bullet Rating')
            ax.set_xlabel('Month')
            ax.set_ylabel('Average rating per month')
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            plt.xticks(rotation=40)
            st.pyplot(fig)
        else:
            st.warning("No Bullet Data")

    elif rapid_button:
        st.markdown("Rapid Rating")
        if not df_rapid_monthly.empty:
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.lineplot(x='month', y='player_rating', data=df_rapid_monthly, marker='o', ax=ax)
            ax.set_title('Rapid Rating')
            ax.set_xlabel('Month')
            ax.set_ylabel('Average rating per month')
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            plt.xticks(rotation=40)
            st.pyplot(fig)
        else:
            st.warning("No Rapid Data")
    else:
        st.info("Select time class rating")