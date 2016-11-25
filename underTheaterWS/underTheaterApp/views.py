# vim: set fileencoding=utf-8 :
import json
from django.views.generic import DetailView, CreateView, UpdateView
from underTheaterApp.models import PlayTheater, Theater, Rate, ClassTheater
from underTheaterApp.forms import PlayTheaterForm, ClassTheaterForm
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden


class PlayTheaterDetailView(DetailView):
    model = PlayTheater

    def get_context_data(self, **kwargs):
        context = super(PlayTheaterDetailView, self).get_context_data(**kwargs)
        context["can_rate"] = self.request.user.is_authenticated() and hasattr(self.request.user, "profile")\
            and self.request.user.profile.can_rate_play(self.object.id)
        return context


class PlayTheaterCreateView(CreateView):
    model = PlayTheater
    form_class = PlayTheaterForm

    def _save_actors_formset(self, forms):
        instances = []
        for form in forms:
            instances.append(form.save())
        return instances

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        play_theater = super(PlayTheaterCreateView, self).post(request, *args, **kwargs)
        return play_theater


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


def rate_play(self, pk):
    if self.POST and self.user.profile.can_rate_play(pk):
        play = get_object_or_404(PlayTheater, pk=pk)
        rate = self.POST.get("rate")
        comments = self.POST.get("comments")
        play_rate = Rate(user_profile_rate=self.user.profile, play_theater=play, rate=rate, comment=comments)
        play_rate.save()
        context = {'success': True, 'cause': "ok", "rating": play.rating(),
                   "username": self.user.username, "url_profile": self.user.profile.get_absolute_url()}
        return HttpResponse(json.dumps(context), content_type="application/json")
    else:
        return HttpResponseForbidden()


class ClassTheaterCreateView(CreateView):
    model = ClassTheater
    form_class = ClassTheaterForm

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        play_theater = super(ClassTheaterCreateView, self).post(request, *args, **kwargs)
        return play_theater


class ClassTheaterDetailView(DetailView):
    model = ClassTheater


class ClassTheaterUpdateView(UpdateView):
    model = ClassTheater
    form_class = ClassTheaterForm
    template_name = "underTheaterApp/classtheater_form.html"

    def dispatch(self, *args, **kwargs):
        if self.request.user != self.get_object().owner:
            return HttpResponseForbidden()
        return super(ClassTheaterUpdateView, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return super(ClassTheaterUpdateView, self).post(request, *args, **kwargs)
