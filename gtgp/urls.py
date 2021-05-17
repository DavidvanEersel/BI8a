from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home.html', views.index, name='home'),
    path('upload.html', views.upload, name='upload'),
    path('manual.html', views.manual, name='manual'),
    path('about.html', views.about, name='about'),
    ]
