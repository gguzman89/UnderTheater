from django.conf.urls import url
from underTheaterApp import views

app_name = 'underTheaterApp'
urlpatterns = [
        url(r'^play_theater/(?P<pk>\d+)/$',
            views.PlayTheaterDetailView.as_view(), name='playtheater_detail'),
]
