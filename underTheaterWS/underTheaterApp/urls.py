from django.conf.urls import url
from underTheaterApp import views
from django.contrib.auth.decorators import login_required

app_name = 'underTheaterApp'
urlpatterns = [
    url(r'^play_theater/(?P<pk>\d+)/$',
        views.PlayTheaterDetailView.as_view(), name='playtheater_detail'),
    url(r'^create_play_theater/$',
        login_required(views.PlayTheaterCreateView.as_view()), name='create_playtheater'),
    url(r'^play_theater/(?P<pk>\d+)/update/$',
        login_required(views.PlayTheaterUpdateView.as_view()), name='playtheater_update'),
    url(r'^theater/(?P<pk>\d+)/all_room_theater/$',
        login_required(views.all_room_theaters), name='all_room_theater'),
]
