from django.urls import path

from . import views

app_name = 'uta'
urlpatterns = [
    path('', views.all_in_one, name='all_in_one'),
]
