from django.shortcuts import render
from django.template import loader

from .models import Video

# Create your views here.

def all_in_one(request):
    videos = Video.objects.all()
    context = {
        'videos' : videos
    }
    return render(request, 'video/all_in_one.html', context)

