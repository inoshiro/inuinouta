import os
import pyyoutube

API_KEY = os.environ['YOUTUBE_API_KEY']
INUI_CHANNEL_ID = 'UCXRlIK3Cw_TJIQC5kSJJQMg'

def get_videos(channel_id):
    api = pyyoutube.Api(api_key=API_KEY)
    channel_res = api.get_channel_info(channel_id=channel_id)

    playlist_id = channel_res.items[0].contentDetails.relatedPlaylists.uploads

    print(playlist_id)


if __name__ == '__main__':
    get_videos(INUI_CHANNEL_ID)
