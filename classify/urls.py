from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^upload', views.classify, name='index'),
    url(r'^$', views.index, name='index'),
]