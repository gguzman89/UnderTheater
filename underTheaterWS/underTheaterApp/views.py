# vim: set fileencoding=utf-8 :
from django.views.generic import DetailView, CreateView, UpdateView
from underTheaterApp.models import PlayTheater
from underTheaterApp.forms import PlayTheaterForm


class PlayTheaterDetailView(DetailView):
    model = PlayTheater


class PlayTheaterCreateView(CreateView):
    model = PlayTheater
    form_class = PlayTheaterForm


class PlayTheaterUpdateView(UpdateView):
    model = PlayTheater
    form_class = PlayTheaterForm
    template_name = "underTheaterApp/playtheater_form.html"
