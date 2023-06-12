from os import path

from django import views


urlpatterns = [
    path('locallibrary', views.index, name='index'),
]