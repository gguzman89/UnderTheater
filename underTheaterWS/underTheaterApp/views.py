# vim: set fileencoding=utf-8 :
from django.views.generic import DetailView
from underTheaterApp.models import PlayTheater


class PlayTheaterDetailView(DetailView):
        model = PlayTheater

