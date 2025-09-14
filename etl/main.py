from extract_chess_data import extract_chess_player_data
from transform_chess_data import transformed_games


def run_etl(username: str):
    """
    Orchestrates the complete ETL (Extract, Transform, Load) process.

    This function calls the data extraction, then transformation functions
    to download and process a user's chess data.

    Args:
        username (str): The Chess.com username to process.
    """
    extract_chess_player_data(username=username)
    transformed_games(username=username)


if __name__ == "__main__":
    username_input = input("Which username do you want to extract data of? ")
    run_etl(username=username_input)
