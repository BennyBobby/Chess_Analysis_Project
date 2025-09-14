import json
import pandas as pd
import os
import re

JSON_DATA_DIR = "data/json"
TRANSFORMED_DATA_DIR = "data/transformed"


def transformed_single_game(game: dict, username: str):
    """
    Transforms a single raw game dictionary into a clean, standardised
    format. This function extracts key data points from a raw game
    dictionary from the Chess.com API. It also determines the player's
    color, rating, opponent's details, and standardises the game
    result (win, loss, or draw).

    Args:
        game (dict): A dictionary representing a single chess game.
        username (str): The chess.com username of the player

    Returns:
        dict/None: A dictionary containing the transformed game data,
        or None if there is data from the user.
    """
    transformed_data = {}
    transformed_data["game_url"] = game.get("url")
    transformed_data["game_id"] = game["url"].split("/")[-1]
    date_pattern = r"\[Date \"(.*?)\"\]"
    date_match = re.search(date_pattern, game.get("pgn", ""))
    transformed_data["date"] = date_match.group(1) if date_match else None
    transformed_data["rated"] = game.get("rated")
    transformed_data["time_class"] = game.get("time_class")
    opening = game.get("eco")
    transformed_data["opening"] = opening.split("/")[-1]
    accuracies = game.get(
        "accuracies", {}
    )  # get {} if there are no accuracies availables
    transformed_data["white_accuracy"] = accuracies.get("white")
    transformed_data["black_accuracy"] = accuracies.get("black")

    player = False
    if game["white"]["username"].lower() == username.lower():
        transformed_data["player_color"] = "white"
        transformed_data["player_rating"] = game["white"]["rating"]
        transformed_data["opponent_username"] = game["black"]["username"]
        transformed_data["opponent_rating"] = game["black"]["rating"]
        player_result = game["white"]["result"]
        player = True
    elif game["black"]["username"].lower() == username.lower():
        transformed_data["player_color"] = "black"
        transformed_data["player_rating"] = game["black"]["rating"]
        transformed_data["opponent_username"] = game["white"]["username"]
        transformed_data["opponent_rating"] = game["white"]["rating"]
        player_result = game["black"]["result"]
        player = True

    if not player:
        return None

    if player_result == "win":
        transformed_data["player_result"] = "win"
    elif player_result in ["resigned", "timeout", "checkmated"]:
        transformed_data["player_result"] = "loss"
    elif player_result in [
        "draw",
        "stalemate",
        "insufficientmaterial",
        "50move",
        "agreed",
        "repetition",
    ]:
        transformed_data["player_result"] = "draw"
    else:
        transformed_data["player_result"] = "N/A"
    return transformed_data


def transformed_games(username: str, raw_dir: str = JSON_DATA_DIR):
    """
    Reads raw JSON game data, transforms it, and saves it as a CSV.

    This function iterates through all JSON files in a user's raw data
    directory. It processes each game using transformed_single_game
    function and compiles the results into a single list. This list is
    then converted into a pandas DataFrame. Finally, the DataFrame is
    saved as a CSV file in the user's transformed data directory.

    Args:
        username (str): The chess.com username of the player.
        raw_dir (str): The directory where the raw JSON data is stored.

    Returns:
        pd.DataFrame: A pandas DataFrame containing all transformed
        game data. Returns an empty DataFrame if no files are found or
        if an error occurs.
    """
    all_games = []
    raw_dir = os.path.join(JSON_DATA_DIR, username)
    if not os.path.exists(raw_dir):
        print(f"User raw data directory not found: '{raw_dir}'.")
        return pd.DataFrame()
    for file in os.listdir(raw_dir):
        filepath = os.path.join(raw_dir, file)
        if not os.path.isfile(filepath) or not file.endswith(
            ".json"
        ):  # we only look at .json file and not .git file for example
            continue
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                games = json.load(f)
                print(f"Processing: {filepath}")
                for game in games:
                    transformed_game = transformed_single_game(game, username)
                    if transformed_game:
                        all_games.append(transformed_game)
        except Exception as e:
            print(f"Transform step: Error {e} from {filepath}")
    if all_games:
        df = pd.DataFrame(all_games)
        df["opening"] = df["opening"].fillna("N/A")
        df["player_color"] = df["player_color"].astype("category")
        df["player_result"] = df["player_result"].astype("category")
        df["time_class"] = df["time_class"].astype("category")
        df["rated"] = df["rated"].astype(bool)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        user_transformed_output_dir = os.path.join(TRANSFORMED_DATA_DIR, username)
        os.makedirs(user_transformed_output_dir, exist_ok=True)
        output_filename = os.path.join(
            user_transformed_output_dir, f"{username}_transformed_games.csv"
        )
        df.to_csv(output_filename, index=False, encoding="utf-8")
        print(f"Data saved: {output_filename}")
        return df

    else:
        print(f"There is no found games with {username}")
        return pd.DataFrame()


if __name__ == "__main__":
    username = input("Which username do you want to transform data of? ")
    df = transformed_games(username=username)
    if df.empty:
        print("The dataframe is empty.")
    else:
        print(df.head())
