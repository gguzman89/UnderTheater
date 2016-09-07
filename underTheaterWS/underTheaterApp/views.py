from django.views.generic import TemplateView, ListView, DetailView
from underTheaterApp.models import PlayTheater


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
