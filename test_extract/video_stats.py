import os
import json

import requests
from dotenv import load_dotenv

load_dotenv()

def establish_connection():
    API_KEY = os.getenv("YT_API_KEY")
    CHANNEL_HANDLER = os.getenv("CHANNEL_HANDLER")
    url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLER}&key={API_KEY}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        raise e


def extract_data(response):
    data = response.json()
    json_data = json.dumps(data, indent=4)
    print(json_data)

    try:
        extract_playlist = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    except (KeyError, IndexError) as e:
        print(f"Unable to find playlist id: {e}")
        raise

    print(extract_playlist)
    return extract_playlist


if __name__ == "__main__":
    response = establish_connection()
    extract_data = extract_data(response)


