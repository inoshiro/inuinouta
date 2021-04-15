import json
from django.shortcuts import render

from .models import Video, Song


def all_in_one(request):
    videos = Video.objects.filter(is_open=True)

    if not request.user.is_superuser:
        videos = videos.filter(is_member_only=False)

    newest_video = videos.latest('published_at')

    if "sid" in request.GET:
        try:
            param_sid = request.GET.get("sid")
            initial_song = Song.objects.get(pk=param_sid)
        except Song.DoesNotExist:
            initial_song = newest_video.sorted_song_set.first()
    else:
        initial_song = newest_video.sorted_song_set.first()

    # ネタ対応
    font_rainbow = False
    if 'rainbow' in request.GET:
        font_rainbow = True

    data_playlist = []
    data_videos = {}
    data_songs = {}
    for v in videos:
        data_videos[v.video_id] = {
            "title": v.title
        }
        for s in v.sorted_song_set:
            content_song = {
                "id": s.id,
                "video_id": v.video_id,
                "title": s.title,
                "artist": s.artist,
                "start_at": s.start_at,
                "end_at": s.end_at
            }
            data_playlist.append(content_song)
            data_songs[s.id] = content_song

    context = {
        'videos': videos,
        'initial_song': initial_song,
        'json_playlist': json.dumps(data_playlist, ensure_ascii=False),
        'json_songs': json.dumps(data_songs, ensure_ascii=False),
        'json_videos': json.dumps(data_videos, ensure_ascii=False),
        'font_rainbow': font_rainbow
    }

    template_file = 'video/all_in_one.html'

    return render(request, template_file, context)
