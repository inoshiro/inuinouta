import os
import pyyoutube

API_KEY = os.environ['YOUTUBE_API_KEY']
INUI_CHANNEL_ID = 'UCXRlIK3Cw_TJIQC5kSJJQMg'

def get_videos(channel_id):
    api = pyyoutube.Api(api_key=API_KEY)
    channel_res = api.get_channel_info(channel_id=channel_id)

    playlist_id = channel_res.items[0].contentDetails.relatedPlaylists.uploads

    print(playlist_id)

def get_video_info(video_id):
    api = pyyoutube.Api(api_key=API_KEY)
    video_res = api.get_video_by_id(video_id=video_id)

    return video_res.items[0]


if __name__ == '__main__':
    get_videos(INUI_CHANNEL_ID)

    video_info = get_video_info('zokUrGt0iuc')
    print(video_info.snippet.title)
