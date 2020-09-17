import requests
import os
from django.conf import settings


THUMB_DIR = os.path.join(settings.BASE_DIR, 'static', 'images', 'thumbs')

def save_thumbnail(video_id):
    image = download_image(video_id)
    filename = os.path.join(THUMB_DIR, video_id + ".jpg")

    with open(filename, "wb") as fout:
        fout.write(image)

def download_image(video_id):
    url = "http://img.youtube.com/vi/{}/mqdefault.jpg".format(video_id)
    response = requests.get(url)

    if not response.status_code == 200:
        e = Exception("HTTP Error: {}".format(response.status_code))

    return response.content
