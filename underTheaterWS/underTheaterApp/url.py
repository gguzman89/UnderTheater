from django.conf.urls import include, url
from django.contrib import admin
from underTheaterApp import views

urlpatterns = [
        url(r'^admin/', admin.site.urls),
]
