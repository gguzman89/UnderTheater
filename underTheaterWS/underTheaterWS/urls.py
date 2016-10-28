"""underTheaterWS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from underTheaterApp import urls
from underTheaterWS import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name="home"),
    url(r'^admin/', admin.site.urls),
    url(r'^search/', views.SearchView.as_view(), name="search"),
    url(r'^register/$', views.RegisterView.as_view(),
        name='register_user'),
    url(r'^select_profile/$', views.SelectProfileView.as_view(),
        name='select_profile'),
    url(r'^create_profile/$', views.ProfileCreateView.as_view(),
        name='create_profile'),
    url(r'^profile/(?P<pk>\d+)/$', views.ProfileDetailView.as_view(),
        name='profile_detail'),
    url(r'', include(urls)),
    url(r'^accounts/login/$', auth_views.login,
        {'template_name': 'auth/login.html'}, name="login_user"),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'},
        name="logout_user"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
