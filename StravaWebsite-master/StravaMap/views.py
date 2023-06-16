from django.shortcuts import render
import folium
import requests
import pandas as pd
import polyline
from StravaMap.models import Activity
from StravaMap.models import Col
from StravaMap.models import Col_counter
from StravaMap import cols_tools as ct
from StravaMap.col_dbtools import *


# Create your views here.

###################################################################
#   Base Map
###################################################################

def base_map(request):
    # Make your map object
    main_map = folium.Map(location=[43.765, 7.223], zoom_start = 6) # Create base map

    conn = create_connection('db.sqlite3')    

    # Les cols passés
    colOK = cols_effectue(conn)    
    listeOK = []
    for oneCol in colOK:        
        listeOK.append(oneCol[3])   # col_code
        
    # Tous les cols        
    myColsList =  select_all_cols06(conn)         
    # Plot Cols onto Folium Map
    for oneCol in myColsList:
        myCol = ct.PointCol()
        myCol.setPoint(oneCol)
        location = [myCol.lat,myCol.lon]
        colColor = "red"
        if myCol.col_code in listeOK :
            colColor = "green"
         
        folium.Marker(location, popup=myCol.name,icon=folium.Icon(color=colColor, icon="flag")).add_to(main_map)        
    
    main_map_html = main_map._repr_html_() # Get HTML for website

    context = {
        "main_map":main_map_html
    }
                                    
    return render(request, 'index.html', context)

###################################################################
#   Col Map
###################################################################

def col_map(request):
    # Make your map object
    print("col_map View >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    col_map = folium.Map(location=[43.765, 7.223], zoom_start = 6) # Create base map            
    col_map_html = col_map._repr_html_() # Get HTML for website    
    context = {
        "col_map":col_map_html
    }
                                    
    return render(request, 'StravaMap/col_detail.html/', context)

###################################################################
#   Connected Map
###################################################################

def connected_map(request):
    # Make your map object
    main_map = folium.Map(location=[43.765, 7.223], zoom_start = 6) # Create base map 
    user = request.user # Pulls in the Strava User data
    strava_login = user.social_auth.get(provider='strava') # Strava login
    access_token = strava_login.extra_data['access_token'] # Strava Access token
    activites_url = "https://www.strava.com/api/v3/athlete/activities"

    # Get activity data
    header = {'Authorization': 'Bearer ' + str(access_token)}
    
    activity_df_list = []

    ########################################################
    # 1st june 2023     -   1685577600
    ########################################################

    param = {'after': 1685577600, "per_page": 200}
    activities_json = requests.get(activites_url, headers=header, params=param).json()
            
    ########################
    #   Last 100 activities
    ########################
    #for n in range(1):  # Change this to be higher if you have more than 1000 activities
    #    param = {'per_page': 100, 'page': n + 1}

    #    activities_json = requests.get(activites_url, headers=header, params=param).json()
    #    if not activities_json:
    #        break
    
    activity_df_list.append(pd.json_normalize(activities_json))
    
    # Get Polyline Data
    activities_df = pd.concat(activity_df_list)        
        
    activities_df = activities_df.dropna(subset=['map.summary_polyline'])
    
    activities_df['polylines'] = activities_df['map.summary_polyline'].apply(polyline.decode)

    conn = create_connection('db.sqlite3')
    myColsList =  select_all_cols06(conn)        
            
    for ligne in range(len(activities_df)):
        AllVisitedCols = []
        myGPSPoints = []        
        strava_id = int(activities_df['id'][ligne]          )
        activity_name = activities_df['name'][ligne]      
        act_start_date = activities_df['start_date'][ligne]      
        act_dist = activities_df['distance'][ligne]      
        act_den = activities_df['total_elevation_gain'][ligne]       
        sport_type = activities_df['sport_type'][ligne]
        act_time = int(activities_df['moving_time'][ligne])
        act_power = activities_df['average_watts'][ligne]
        act_status = 0 # not analyzed
        strava_user = 366232

        ########## Delete / Insert ###############
        # insert activities and col for each one
        ##########################################

        delete_activity(conn,strava_id)
        delete_col_perform(conn,strava_id)

        insert_activity(conn,strava_user,strava_id,activity_name,act_start_date, act_dist, act_den,sport_type,act_time,act_power,act_status)                

        for pl in activities_df['polylines'][ligne]:
            if len(pl) > 0: 
                myPoint = ct.PointGPS()                
                myPoint = pl                
                myGPSPoints.append(myPoint)
    
        returnList = ct.getColsVisited(myColsList,myGPSPoints)       
        
        for ligne in returnList:                
            AllVisitedCols.append(ligne)
            print(ligne)                
        #print(activity_name)
        #for ligne in AllVisitedCols:                
        #    print(ligne)

        insert_col_perform(conn,strava_id, AllVisitedCols)
        compute_cols(strava_user,strava_id)
                    
    # Plot Polylines onto Folium Map
    for pl in activities_df['polylines']:
        if len(pl) > 0: # Ignore polylines with length zero (Thanks Joukesmink for the tip)
            folium.PolyLine(locations=pl, color='red').add_to(main_map)                
            
    # Return HTML version of map
    main_map_html = main_map._repr_html_() # Get HTML for website
    context = {
        "main_map":main_map_html
    }
        
    return render(request, 'index.html', context)

# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# import folium
#
# # Create your views here.
#
#
# def main_map(request):
#     # Create Map Object
#     main_map = folium.Map(location=[19, -12], zoom_start=2)
#
#     # folium.Marker([39.09616, -117.80612], tooltip='Click for more',
#     #               popup='United States').add_to(main_map)
#     # Get HTML Representation of Map Object
#     main_map = main_map._repr_html_()
#     context = {
#         'main_map': main_map,
#         'form': 'potato',
#     }
#     return render(request, 'index.html', context)


def index(request):

    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_cols = Col.objects.all().count()
    num_cols06 = Col.objects.all().count()

    context = {
        'Nombre de Cols': num_cols,
        'Nombre de Cols (AM)': num_cols06,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context)

from django.views import generic

class ColsListView(generic.ListView):    
    def get_queryset(self):
        return Col.objects.order_by("col_alt")

class Cols06ListView(generic.ListView):    
    def get_queryset(self):
        return Col.objects.filter(col_code__icontains='FR-06').order_by("col_alt")
    
class Cols06okListView(generic.ListView):        
    def get_queryset(self):                
        qsOk = Col_counter.objects.all().order_by("-col_count")
                                                           
        return qsOk
    
class Cols06koListView(generic.ListView):        
    def get_queryset(self):                
        qsOk = Col_counter.objects.all()
        lOk= []

        for oneOk in qsOk:
            lOk.append(oneOk.col_code)

        qsCol =  Col.objects.exclude(col_code__in=lOk)
                                   
        return qsCol.filter(col_code__icontains='FR-06').order_by("col_alt")    
    
class ActivityListView(generic.ListView):        
    def get_queryset(self):                
        return Activity.objects.all().order_by("-act_start_date")
    
class ActivityDetailView(generic.DetailView):                   
    model = Activity        
   
    """        
    
    def get_object(self, queryset=None):                
        strava_id = self.kwargs.get('strava_id') or self.request.GET.get('strava_id') or None                
        myObject = Activity.objects.filter(strava_id=strava_id)                 
        print("CLASSE = ", type(myObject))   
        print("act_name = ", myObject[0].act_name)         
        print("strava_id = ", myObject[0].strava_id)         
        print("act_type = ", myObject[0].act_type)                 
                        
        return myObject
        
    
    
    def get_context_data(self, **kwargs):
        context = super(ActivityDetailView, self).get_context_data(**kwargs)
        selected_Strava_id = self.kwargs.get('strava_id')        
        context['strava_id'] = selected_Strava_id
        print("get_context_data = ", selected_Strava_id)        
        self.get_queryset().filter(strava_id=selected_Strava_id)
        return context
    """    
                                     
class ColsDetailView(generic.DetailView):
	# specify the model to use    
	model = Col    
