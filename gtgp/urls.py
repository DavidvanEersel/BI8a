from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home.html', views.index, name='home'),
    path('upload.html', views.upload, name='upload'),
    path('manual.html', views.manual, name='manual'),
    path('about.html', views.about, name='about'),
]
