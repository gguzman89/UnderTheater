from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth import login
from underTheaterApp.models import PlayTheater
from underTheaterApp.forms import UserCreateForm, TheaterCreateForm, ActorCreateForm, SpectatorCreateForm
from django.contrib import messages
from django.shortcuts import redirect


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["plays"] = PlayTheater.objects.next_releases()
        return context


class SelectProfileView(TemplateView):
    template_name = 'create_profile.html'


class SearchView(ListView):
    model = PlayTheater
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        search = self.request.GET.get("search_term", None)
        self.object_list = PlayTheater.objects.filter(play_name__icontains=search)
        context = super(SearchView, self).get_context_data(**kwargs)
        context["search"] = search
        return context


class RegisterView(CreateView):
    "Creates a new user"

    model = User
    form_class = UserCreateForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        response = super(RegisterView, self).post(request, *args, **kwargs)
        if self.object:
            login(request, self.object)
        return response


class ProfileCreateView(CreateView):
    "Creates a new profile"

    template_name = "profile_create.html"
    success_url = '/'
    model_dict = {"actor": ActorCreateForm, "spectator": SpectatorCreateForm, "theater": TheaterCreateForm}

    def dispatch(self, *args, **kwargs):
        if hasattr(self.request.user, "profile"):
            messages.add_message(self.request, messages.INFO, 'No puedes crear el perfil dos veces')
            return redirect("/")
        return super(ProfileCreateView, self).dispatch(*args, **kwargs)

    def get_form_class(self):
        profile = self.request.GET.get('profile', None)
        form = self.model_dict.get(profile)
        return form
