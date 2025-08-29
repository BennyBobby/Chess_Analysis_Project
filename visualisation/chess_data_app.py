import streamlit as st
from visualisation_utils import (
    load_data,
    show_number_games,
    plot_outcome_distribution,
    plot_rating_evolution,
    plot_frequent_openings,
)

st.title("Chess data visualisation")
username = st.text_input("Please enter your Chess.com username")
if username:
    dataframe_games = load_data(username_input=username)
    if dataframe_games.empty:
        st.warning(f"Dataframe empty for {username}")
    else:
        first_game_date = dataframe_games["date"].min().to_pydatetime()
        last_game_date = dataframe_games["date"].max().to_pydatetime()
        date_range = st.slider(
            "Select date range",
            min_value=first_game_date,
            max_value=last_game_date,
            value=(first_game_date, last_game_date),
            format="YYYY-MM-DD",
            key="slider_date_range",
        )
        start_date, end_date = date_range
        dataframe_games_filtered = dataframe_games[
            (dataframe_games["date"] >= start_date)
            & (dataframe_games["date"] <= end_date)
        ].copy()
        if dataframe_games_filtered.empty:
            st.warning("No data found within the selected date range.")
            st.stop()
        st.dataframe(dataframe_games_filtered.head())
        # show the number of games done by the user
        st.subheader("Number of games")
        show_number_games(dataframe_games_filtered)
        # show average rating of opponents following time class
        st.subheader("Average rating of opponents")
        column11, column12, column13 = st.columns(3)
        avg_rating_all_time_class = round(
            dataframe_games_filtered.groupby(["time_class"])["opponent_rating"].mean()
        )
        with column11:
            st.metric(label="Blitz", value=avg_rating_all_time_class["blitz"])
        with column12:
            st.metric(label="Bullet", value=avg_rating_all_time_class["bullet"])
        with column13:
            st.metric(label="Rapid", value=avg_rating_all_time_class["rapid"])
        # show distribution of win, lose and draw following time class
        st.subheader("Game results")
        tab11, tab12, tab13 = st.tabs(["Blitz", "Bullet", "Rapid"])
        df_blitz = dataframe_games_filtered[
            dataframe_games_filtered["time_class"] == "blitz"
        ]
        df_bullet = dataframe_games_filtered[
            dataframe_games_filtered["time_class"] == "bullet"
        ]
        df_rapid = dataframe_games_filtered[
            dataframe_games_filtered["time_class"] == "rapid"
        ]
        with tab11:
            plot_outcome_distribution(df=df_blitz, time_class="Blitz")
        with tab12:
            plot_outcome_distribution(df=df_bullet, time_class="Bullet")
        with tab13:
            plot_outcome_distribution(df=df_rapid, time_class="Rapid")
        # show ratings evolution of the player
        st.subheader("Ratings Evolution")
        tab21, tab22, tab23 = st.tabs(["Blitz", "Bullet", "Rapid"])
        with tab21:
            plot_rating_evolution(df=df_blitz, time_class="Blitz")
        with tab22:
            plot_rating_evolution(df=df_bullet, time_class="Bullet")
        with tab23:
            plot_rating_evolution(df=df_rapid, time_class="Rapid")
        # show opening ranking by frequency
        st.subheader("Most frequent played openings")
        tab31, tab32, tab33 = st.tabs(["Blitz", "Bullet", "Rapid"])
        with tab31:
            plot_frequent_openings(df=df_blitz, time_class="Blitz")
        with tab32:
            plot_frequent_openings(df=df_bullet, time_class="Bullet")
        with tab33:
            plot_frequent_openings(df=df_rapid, time_class="Rapid")
