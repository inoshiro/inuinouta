from django.shortcuts import render
from django.template import loader

from .models import Video


def all_in_one(request):
    videos = Video.objects.all()
    context = {
        'videos' : videos
    }

    if request.user_agent.is_pc:
        return render(request, 'video/all_in_one.html', context)

    return render(request, 'video/all_in_one_mobile.html', context)

