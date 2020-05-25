from django.shortcuts import render

from .models import Channel, Video, Song


def all_in_one(request):
    inui_channel = Channel.objects.get(id=1)
    videos = inui_channel.video_set.filter(is_open=True)

    if 'vid' in request.GET:
        try:
            param_vid = request.GET.get('vid')
            initial_video = videos.get(url__contains=param_vid)
        except Video.DoesNotExist:
            initial_video = videos.first()
    else:
        initial_video = videos.first()

    if "sid" in request.GET:
        try:
            param_sid = request.GET.get("sid")
            initial_song = initial_video.song_set.get(pk=param_sid)
        except Song.DoesNotExist:
            initial_song = initial_video.sorted_song_set.first()
    else:
        initial_song = initial_video.sorted_song_set.first()

    context = {
        'videos': videos,
        'initial_video': initial_video,
        'initial_song': initial_song
    }

    if request.user_agent.is_pc:
        return render(request, 'video/all_in_one.html', context)

    return render(request, 'video/all_in_one_mobile.html', context)
