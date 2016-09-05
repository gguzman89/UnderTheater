from django.views.generic import TemplateView


class HomeViews(TemplateView):
    template_name = 'home.html'

