import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()


def establish_connection():
    try:
        response = requests.get(f'https://youtube.googleapis.com/youtube/v3/videos?part=statistics&id=7B44gyvBsTA&key={os.getenv("YT_API_KEY")}')
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return None


def extract_data(response):
    if response is None:
        print("An api call fail")
        return

    res = json.loads(response.text)

    for data in res['items']:
        id = data['id']
        views = data['statistics']['viewCount']
        likes = data['statistics']['likeCount']
        comments = data['statistics']['commentCount']

        print(f"ID:{id}\nViews Count:{views}\nLikes Count:{likes}\nComments Count:{comments}")


if __name__ == "__main__":
    response = establish_connection()
    extract_data(response)