import os
import json

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YT_API_KEY")
CHANNEL_HANDLER = os.getenv("CHANNEL_HANDLER")

def establish_connection():
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





def extract_video_data(video_ids):
    extracted_data = []

    def batch_list(video_id_list, batch_size):
        for video_id in range(0, len(video_id_list), batch_size):
            yield video_id_list[video_id:video_id + batch_size]

        try:
            for batch in batch_list(video_ids, max_results):
                video_ids_str = ",".join(batch)
                url = f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}'

                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                for item in data.get('items', []):
                    video_id = item['id']
                    snippet = item['snippet']
                    content_details = item['contentDetails']
                    statistics = item['statistics']

                    video_data = {
                        "video_id": video_id,
                        "title": snippet['title'],
                        "published_at": snippet['published_at'],
                        "duration": content_details['duration'],
                        "viewCount": statistics.get("viewCount", None),
                        "likeCount": statistics.get("likeCount", None),
                        "commentCount": statistics.get("commentCount", None),
                    }

                    extracted_data.append(video_data)

             return extracted_data

        except requests.exceptions.RequestException as e:
            raise e


if __name__ == "__main__":
    response = establish_connection()
    result = extract_data(response)


