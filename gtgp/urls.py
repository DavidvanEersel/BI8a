from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home.html', views.index, name='home'),
    path('upload.html', views.upload, name='upload'),
    path('manual.html', views.manual, name='manual'),
    path('about.html', views.about, name='about'),
    i18n_patterns(path('admin/', admin.site.urls), prefix_default_language=False) + \
    #static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) ]
