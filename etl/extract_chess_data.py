import requests
import json
import time
import os

USER_AGENT = "Mozilla/5.0 (compatible; Chess_Analyse/1.0; +https://chess.com)"


def make_request(url: str):
    """
    It makes an HTTP GET request to Chess.com API. This function try to
    retrieve data from URL using the requests library. This includes a
    custom user-agent header to identify the application.

    Args:
        url (str): The GET request uses this URL.
    Returns:
        dict/None: If the request went successfully, the JSON content
        of the response is returned. If not, None is returned.
    """
    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT})
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Error request with {url} which is {err}")
        return None


def get_chess_data(username: str):
    """
    Retrieves the archive URLs for a Chess.com player.

    Args:
        username (str): The chess.com username of the player

    Returns:
        list: A list of archive player's game
    """
    url = f"https://api.chess.com/pub/player/{username}/games/archives"
    data = make_request(url)
    if (
        data and "archives" in data
    ):  # we check if data is not empty and archives key is in data
        return data["archives"]
    return []


def save_games_to_json(username: str, month: int, year: int, games_data: list):
    """
    It saves list of games to JSON file. This function creates the user
    directory in data/json and saves provided games list into JSON file.

    Args:
            username (str): The Chess.com username of the player.
            month (int): The month of the games.
            year (int): The year of the games.
            games_data (list): A list of dictionaries, where each dictionary represents a game.

    Raises:
        IOError: If an error occurs during file saving.

    """
    user_json_dir = os.path.join("data/json", username)
    os.makedirs(user_json_dir, exist_ok=True)  # we create the user folder in data/json
    filename = os.path.join(user_json_dir, f"{username}_{year}_{month}.json")
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(games_data, f, ensure_ascii=False, indent=4)
    except IOError as err:
        print(f"Error {err} during saving file: {filename}")


def download_monthly_games(archive_url: str):
    """
    Downloads all games from a specific monthly archive URL.

    Args:
        archive_url (str): The URL of the monthly game archive.

    Returns:
        list: A list of dictionaries representing the games. Returns
        an empty list if the request fails or no games are found.
    """
    print(f"Downloading games from: {archive_url}")
    data = make_request(archive_url)
    if data and "games" in data:
        return data["games"]
    return []


def extract_chess_player_data(username: str):
    """
    Extracts and downloads all game data for a Chess.com player. This
    function orchestrates the data extraction process. It first gets
    the list of monthly archives, then iterates through each archive
    URL to download the games and save them to JSON files. It includes
    a time delay between requests to comply with API usage policies.

    Args:
        username (str): The chess.com username of the player
    """
    print(f"=>Start of the extraction data of {username}")
    archives = get_chess_data(username)
    if not archives:
        print(f"No data found with {username}, play chess then")
        return 0
    total_games_downloaded = 0

    for i, archive_url in enumerate(archives):
        parts = archive_url.split("/")
        year = int(parts[-2])
        month = int(parts[-1])
        games = download_monthly_games(archive_url)
        if games:
            save_games_to_json(username, year, month, games)
            total_games_downloaded += len(games)
        time.sleep(1)
    print(f"=>Extraction done. {total_games_downloaded} games for {username}")


if __name__ == "__main__":
    test_username = input("Which username do you want to extract data of? ")
    extract_chess_player_data(test_username)
