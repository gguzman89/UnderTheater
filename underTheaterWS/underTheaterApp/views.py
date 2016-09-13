# vim: set fileencoding=utf-8 :
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from underTheaterApp.models import PlayTheater
from underTheaterApp.forms import UserCreateForm


class HomeViews(TemplateView):
    template_name = 'home.html'


class SearchView(ListView):
    model = PlayTheater
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        search = self.request.GET.get("search_term", None)
        self.object_list = PlayTheater.objects.filter(play_name__icontains=search)
        context = super(SearchView, self).get_context_data(**kwargs)
        return context


class PlayTheaterDetailView(DetailView):
        model = PlayTheater


class RegisterView(CreateView):
    """Creates a new user
    """
    model = User
    form_class = UserCreateForm
    success_url = "/"

    def post(self, request, *args, **kwargs):
        response = super(RegisterView, self).post(request, *args, **kwargs)
        if self.object:
            login(request, self.object)
        return response


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
