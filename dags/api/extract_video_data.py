import requests
import json
from datetime import date
from airflow.models import Variable
from airflow.decorators import task


MAX_RESULTS = 50


@task
def get_playlist_id():
    api_key = Variable.get("API_KEY")
    channel_handler = Variable.get("CHANNEL_HANDLER")
    url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handler}&key={api_key}'
    response = requests.get(url)
    data = response.json()

    try:
        extract_playlist = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    except (KeyError, IndexError) as e:
        print(f"Unable to find playlist id: {e}")
        raise

    print(extract_playlist)
    return extract_playlist


@task
def get_video_ids(playlist_id):
    api_key = Variable.get("API_KEY")
    video_ids = []
    pageToken = None
    base_url = (f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={MAX_RESULTS}'
                f'&playlistId={playlist_id}&key={api_key}')

    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items', []):
                video_ids.append(item['contentDetails']['videoId'])

            pageToken = data.get('nextPageToken')
            if not pageToken:
                break

        return video_ids

    except requests.exceptions.RequestException as e:
        raise e


@task
def extract_video_data(video_ids):
    api_key = Variable.get("API_KEY")
    extracted_data = []

    def batch_list(lst, batch_size):
        for i in range(0, len(lst), batch_size):
            yield lst[i:i + batch_size]

    try:
        for batch in batch_list(video_ids, MAX_RESULTS):
            video_ids_str = ",".join(batch)
            url = f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={api_key}'

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items', []):
                snippet = item['snippet']
                content_details = item['contentDetails']
                statistics = item['statistics']

                extracted_data.append({
                    "video_id": item['id'],
                    "title": snippet['title'],
                    "published_at": snippet['publishedAt'],
                    "duration": content_details['duration'],
                    "viewCount": statistics.get("viewCount"),
                    "likeCount": statistics.get("likeCount"),
                    "commentCount": statistics.get("commentCount"),
                })

        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e


@task
def save_to_json(extracted_data):
    file_path = f"/opt/airflow/data/yt_data_{date.today()}.json"

    with open(file_path, "w", encoding='utf-8') as json_outfile:
        json.dump(extracted_data, json_outfile, indent=4, ensure_ascii=False)
