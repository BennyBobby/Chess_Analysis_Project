import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

DATA_DIR = "../data/transformed"


@st.cache_data
def load_data(username_input: str) -> pd.DataFrame:
    """
    It loads transformed chess game data for a user. This function
    locates and reads a CSV file containing the player's game data.
    Then, it performs data preprocessing by converting columns to
    appropriate data types.

    Args:
        username_input(str): The username of the user that we want
        to analyse.

    Returns:
        pd.DataFrame: A pandas dataFrame containing the preprocessed
        game

        data. If the file is not found, a empty dataframe is returned.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        Exception: For any other errors that occur while reading the
        file.
    """
    filepath = os.path.join(
        DATA_DIR, username_input, f"{username_input}_transformed_games.csv"
    )
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath)
            df["opening"] = df["opening"].fillna("N/A")
            df["player_color"] = df["player_color"].astype("category")
            df["player_result"] = df["player_result"].astype("category")
            df["time_class"] = df["time_class"].astype("category")
            df["rated"] = df["rated"].astype(bool)
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            st.success(f"Loaded Data from '{username_input}' ({len(df)} game(s).")
            return df
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error(f"No data found from : {filepath}")
        st.stop()

    st.warning("No data loaded.")
    return pd.DataFrame()


def show_number_games(df: pd.DataFrame):
    """
    It shows the number of games done by the user. Firstly, it shows
    the total number of games regardless time class. Then it plots the
    distribution of games number regarding time class.

    Args:
        df (pd.Dataframe): Dataframe containing the user data
    """
    st.metric(label="Total", value=len(df))
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(x="time_class", data=df, palette="Dark2", ax=ax)
    ax.set_title("Number of games by time class")
    ax.set_xlabel("time class")
    ax.set_ylabel("Number of games")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)


def plot_outcome_distribution(df: pd.DataFrame, time_class: str):
    """
    It plots the distribution of game results by time class. This
    function creates a bar chart showing the count of game results.

    Args:
        df (pd.DataFrame): DataFrame containing the user data,
        filtered by time class.

        time_class (str): The time class ('Blitz', 'Bullet' and
        'Rapid') for the plot title
    """
    if df.empty:
        st.warning(f"No {time_class} Data")
        return
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(x="player_result", data=df, palette="Dark2", ax=ax)
    ax.set_title(f"Distribution of {time_class} Results")
    ax.set_xlabel("Results")
    ax.set_ylabel("Number of games")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)


def plot_rating_evolution(df: pd.DataFrame, time_class: str):
    """
    It plots the player's rating evolution following the time class.
    This function create a line plot that shows the player rating
    based on the game date.

    Args:
        df (pd.DataFrame): DataFrame containing the user data, filtered
        by time class.

        time_class (str): The time class ('Blitz', 'Bullet' and 'Rapid')
        for the plot title
    """
    if df.empty:
        st.warning(f"No {time_class} Data")
        return
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        x="date", y="player_rating", data=df, linewidth=2, color="#377E47", ax=ax
    )
    ax.set_title(f"{time_class} Rating")
    ax.set_xlabel("Date")
    ax.set_ylabel("Rating")
    ax.grid(axis="x", linestyle="--", alpha=0.7)
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks(rotation=40)
    st.pyplot(fig)


def plot_frequent_openings(df: pd.DataFrame, time_class: str):
    """
    It plots the most frequent openings played for each time class.
    This function uses a slider to allow user to select the number of
    showed openings.
    It also avoid to show to much openings because some players can
    have thousand of games. It then creates a bar chart of the most
    frequently played openings.

    Args:
        df (pd.DataFrame): DataFrame containing the user data, filtered
        by time class.

        time_class (str): The time class ('Blitz', 'Bullet' and
        'Rapid') for the plot title
    """
    if df.empty:
        st.warning(f"No {time_class} Data")
        return
    total_different_openings_played = len(df["opening"].unique())
    number_frequent_openings = st.slider(
        "How many opening do you want to show",
        1,
        total_different_openings_played if total_different_openings_played < 20 else 20,
        3,
        1,
        key=f"slider_openings_{time_class}",
    )
    frequent_openings = df["opening"].value_counts().head(number_frequent_openings)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x=frequent_openings.values, y=frequent_openings.index, color="#8F0F07", ax=ax
    )
    ax.set_title(f"Most frequent openings played in {time_class}")
    ax.set_xlabel("occurrence")
    st.pyplot(fig)
