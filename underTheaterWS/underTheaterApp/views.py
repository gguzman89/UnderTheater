# vim: set fileencoding=utf-8 :
from django.views.generic import DetailView, CreateView, UpdateView
from underTheaterApp.models import PlayTheater, Theater
from underTheaterApp.forms import PlayTheaterForm
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.http import HttpResponse


class PlayTheaterDetailView(DetailView):
    model = PlayTheater


class PlayTheaterCreateView(CreateView):
    model = PlayTheater
    form_class = PlayTheaterForm

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return super(PlayTheaterCreateView, self).post(request, *args, **kwargs)


class PlayTheaterUpdateView(UpdateView):
    model = PlayTheater
    form_class = PlayTheaterForm
    template_name = "underTheaterApp/playtheater_form.html"

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return super(PlayTheaterUpdateView, self).post(request, *args, **kwargs)


def all_room_theaters(self, pk):
    theater = get_object_or_404(Theater, pk=pk)
    rooms = theater.theater_room.all()
    data = serializers.serialize('json', rooms)
    return HttpResponse(data, content_type="application/json")
