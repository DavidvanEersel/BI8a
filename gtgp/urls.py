from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('upload', views.upload, name='upload'),
    path('manual', views.manual, name='manual'),
]
