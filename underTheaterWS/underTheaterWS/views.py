# vim: set fileencoding=utf-8 :
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import login
from underTheaterApp.models import PlayTheater, ClassTheater
from underTheaterApp.users import OwnerTheater, Actor, Spectators
from underTheaterApp.forms import UserCreateForm, TheaterCreateForm, ActorCreateForm, SpectatorCreateForm
from django.contrib import messages
from django.shortcuts import redirect
from django.http import Http404, HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["plays"] = PlayTheater.objects.next_releases()
        context["class"] = ClassTheater.objects.next_releases()
        return context


class SelectProfileView(TemplateView):
    template_name = 'select_profile.html'

    def dispatch(self, *args, **kwargs):
        if hasattr(self.request.user, "profile"):
            messages.add_message(self.request, messages.WARN, 'No puedes crear el perfil dos veces')
            return redirect("/")
        return super(SelectProfileView, self).dispatch(*args, **kwargs)


class SearchView(ListView):
    model = PlayTheater
    template_name = 'search.html'
    search_dict = {"zone": "dayfunction_related__theater__contact__address__raw__icontains",
                   "title": "play_name__icontains"}

    def get_context_data(self, **kwargs):
        filter_parms = {}
        search = self.request.GET.get("search_term", None)
        type_search = self.request.GET.get("type", None)
        filter_parms[self.search_dict[type_search]] = search
        paginator = Paginator(PlayTheater.objects.filter(**filter_parms), 8)

        page = self.request.GET.get('page')
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        self.object_list = objects
        context = super(SearchView, self).get_context_data(**kwargs)
        context["search"] = search
        context["type"] = type_search
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
    model_dict = {"actor": ActorCreateForm, "spectator": SpectatorCreateForm, "theater": TheaterCreateForm}
    name_dict = {"actor": u"actor", "spectator": u"espectador", "theater": u"dueño de teatro"}

    def dispatch(self, *args, **kwargs):
        if hasattr(self.request.user, "profile"):
            messages.add_message(self.request, messages.WARN, 'No puedes crear el perfil dos veces')
            return redirect("/")
        return super(ProfileCreateView, self).dispatch(*args, **kwargs)

    def get_form_class(self):
        profile = self.request.GET.get('profile', None)
        form = self.model_dict.get(profile)
        return form

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileCreateView, self).get_context_data(*args, **kwargs)
        context["profile"] = self.name_dict[self.request.GET.get('profile', None)]
        return context


class ProfileDetailView(DetailView):
    template_name = 'profile_detail.html'

    def get_object(self):
        klass = [OwnerTheater, Actor, Spectators]
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = None
        for cl in klass:
            obj = cl.objects.filter(pk=pk)
            if obj:
                break
        if not obj:
            raise Http404("El perfil no existe")
        return obj[0]

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        context["can_edit"] = self.request.user == self.get_object().user
        return context


class ProfileUpdateView(UpdateView):
    template_name = "profile_create.html"
    model_dict = {"actor": ActorCreateForm, "spectator": SpectatorCreateForm, "theater": TheaterCreateForm}

    def dispatch(self, *args, **kwargs):
        if self.request.user != self.get_object().user:
            return HttpResponseForbidden()
        return super(ProfileUpdateView, self).dispatch(*args, **kwargs)

    def get_object(self):
        klass = [(OwnerTheater, TheaterCreateForm), (Actor, ActorCreateForm), (Spectators, SpectatorCreateForm)]
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = None
        for cl in klass:
            obj = cl[0].objects.filter(pk=pk)
            if obj:
                self.form_class = cl[1]
                break
        if not obj:
            raise Http404("El perfil no existe")
        return obj[0]
