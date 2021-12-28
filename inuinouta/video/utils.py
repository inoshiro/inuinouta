import requests
import os
from django.conf import settings
import boto3

s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_SECRET_KEY"],
    region_name="ap-northeast-1"
)

S3_BUCKET_NAME = "inuinouta"
S3_BUCKET_PATH = "images/thumbs/"


def save_thumbnail(video_id):
    image = download_image(video_id)
    s3.put_object(Bucket=S3_BUCKET_NAME,
                  Key="{}{}.jpg".format(S3_BUCKET_PATH, video_id),
                  Body=image)


def delete_thumbnail(video_id):
    s3.delete_object(Bucket=S3_BUCKET_NAME,
                     Key="{}{}.jpg".format(S3_BUCKET_PATH, video_id))


def download_image(video_id):
    url = "http://img.youtube.com/vi/{}/mqdefault.jpg".format(video_id)
    response = requests.get(url)

    if not response.status_code == 200:
        e = Exception("HTTP Error: {}".format(response.status_code))

    return response.content
