from django.conf.urls import url
from underTheaterApp import views

app_name = 'underTheaterApp'
urlpatterns = [
    url(r'^play_theater/(?P<pk>\d+)/$',
        views.PlayTheaterDetailView.as_view(), name='playtheater_detail'),
    url(r'^create_play_theater/$',
        views.PlayTheaterCreateView.as_view(), name='create_playtheater'),
    url(r'^play_theater/(?P<pk>\d+)/update/$',
        views.PlayTheaterUpdateView.as_view(), name='playtheater_update'),

]
