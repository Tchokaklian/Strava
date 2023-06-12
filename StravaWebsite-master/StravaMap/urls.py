from django import views
from django.urls import path, include
from .views import *

urlpatterns = [    
    path('', base_map, name='Base Map View'),
    path('connected/', connected_map, name='Connect Map View'),
    path('cols/', ColsListView.as_view(), name='cols'),
    path('cols06/', Cols06ListView.as_view(), name='cols06'),
    path('cols06ok/', Cols06okListView.as_view(), name='cols06ok'),
    path('cols06ko/', Cols06koListView.as_view(), name='cols06ko'),
    path('activity/', ActivityListView.as_view(), name='activity'),
    path('oauth/', include('social_django.urls', namespace='social')),            
]