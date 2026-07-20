import requests
import os
import json

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YT_API_KEY")
CHANNEL_HANDLER = os.getenv("CHANNEL_HANDLER")
MAX_RESULTS = 50

def get_playlist_id():
    url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLER}&key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    json_data = json.dumps(data, indent=4)
    # print(json_data)

    try:
        extract_playlist = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    except (KeyError, IndexError) as e:
        print(f"Unable to find playlist id: {e}")
        raise

    print(extract_playlist)
    return extract_playlist


def get_video_ids(playlist_id):
    video_ids = []
    pageToken = None
    base_url = (f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={MAX_RESULTS}'
                f'&playlistId={playlist_id}&key={API_KEY}')

    try:
        while True:
            url = base_url

            if pageToken:
                url += f"&pageToken={pageToken}"

            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)

            pageToken = data.get('nextPageToken')

            if not pageToken:
                break

        return video_ids

    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    playlist_id = get_playlist_id()
    # print(get_video_ids(playlist_id))


