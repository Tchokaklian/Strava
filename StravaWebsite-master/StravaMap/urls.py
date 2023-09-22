from django import views
from django.urls import path, include
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = [
    path('', base_map, name='Base Map View'),    
    path('oauth/', include('social_django.urls', namespace='social')),     
    path('connected/', connected_map, name='Connect Map View'),                                       
    path('index/',base_map,name='index'),
    path('col_map/<int:col_id>', col_map, name = 'Col Map View'),
    path('act_map/<int:act_id>', act_map, name = 'Activity Map View'),    
    ###
    path('activity/', ActivityListView.as_view(), name='activity'),        
    path('activity/<pk>', ActivityDetailView.as_view()),            
    path('activity/<int:act_id>/<int:col_id>/', col_map_by_act,name = "act-col"),            
    ###
    path('cols/', ColsListView.as_view(), name='cols'),
    path('cols/<pk>/', ColsDetailView.as_view(), name = "col-detail"),                           
    path('cols/<int:col_id>/<int:act_id>/', act_map_by_col, name = "col-act"),                           
    ###
    path('cols06/', Cols06ListView.as_view(), name='cols06'),
    path('cols06/<pk>/', ColsDetailView.as_view(),name = "col-detail"),           
    path('cols06/<int:col_id>/<int:act_id>/', act_map_by_col, name = "col-act"), 
    ###
    path('cols06ok/', ColsOkListView.as_view(), name='colsok'),                           
    path('cols06ok/<pk>/', ColsDetailView.as_view(),name = "col-detail"),           
    path('cols06ok/<int:col_id>/<int:act_id>/', act_map_by_col, name = "col-act"),                                  
    ###
    path('cols06ko/', Cols06koListView.as_view(), name='cols06ko'),                    
    path('cols06ko/<pk>/', ColsDetailView.as_view(),name = "col-detail"),                           
    path('cols06ok/<int:col_id>/<int:act_id>/', act_map_by_col, name = "col-act"),    
    ### 04
    path('cols04/', Cols04ListView.as_view(), name='cols04'),
    path('cols04/<pk>/', ColsDetailView.as_view(),name = "col-detail"),           
    path('cols04/<int:col_id>/<int:act_id>/', act_map_by_col, name = "col-act"), 
    ### 07
    path('cols07/', Cols07ListView.as_view(), name='cols07'),
    path('cols07/<pk>/', ColsDetailView.as_view(),name = "col-detail"),           
    path('cols07/<int:col_id>/<int:act_id>/', act_map_by_col, name = "col-act"), 
    ### 26
    path('cols26/', Cols26ListView.as_view(), name='cols26'),
    path('cols26/<pk>/', ColsDetailView.as_view(),name = "col-detail"),           
    path('cols26/<int:col_id>/<int:act_id>/', act_map_by_col, name = "col-act"), 
    ### 38     
    path('cols38/', Cols38ListView.as_view(), name='cols38'),
    path('cols38/<pk>/', ColsDetailView.as_view(),name = "col-detail"),           
    path('cols38/<int:col_id>/<int:act_id>/', act_map_by_col, name = "col-act"), 
    ### 83 
    path('cols83/', Cols83ListView.as_view(), name='cols83'),
    path('cols83/<pk>/', ColsDetailView.as_view(),name = "col-detail"),           
    path('cols83/<int:col_id>/<int:act_id>/', act_map_by_col, name = "col-act"), 
    ### IT
    path('cols_it_im/', Cols_it_imListView.as_view(), name='cols_it_im'),
    path('cols_it_im/<pk>/', ColsDetailView.as_view(),name = "col-detail"),           
    path('cols_it_im/<int:col_id>/<int:act_id>/', act_map_by_col, name = "col-act"), 



        
]

urlpatterns += staticfiles_urlpatterns()