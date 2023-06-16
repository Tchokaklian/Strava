from django import views
from django.urls import path, include
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [    
    path('', base_map, name='Base Map View'),    
    path('oauth/', include('social_django.urls', namespace='social')),     
    path('connected/', connected_map, name='Connect Map View'),        
    path('activity/', ActivityListView.as_view(), name='activity'),        
    path('activity/<pk>', ActivityDetailView.as_view()),            
    path('cols/', ColsListView.as_view(), name='cols'),
    path('cols/<pk>/', ColsDetailView.as_view()),           
    path('cols06/', Cols06ListView.as_view(), name='cols06'),
    path('cols06/<pk>/', ColsDetailView.as_view()),           
    path('cols06ok/', Cols06okListView.as_view(), name='cols06ok'),
    path('cols06ok/<pk>/', ColsDetailView.as_view()),           
    path('cols06ko/', Cols06koListView.as_view(), name='cols06ko'),                    
    path('cols06ko/<pk>/', ColsDetailView.as_view()),               
]

urlpatterns += staticfiles_urlpatterns()