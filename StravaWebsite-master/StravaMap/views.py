from django.shortcuts import render
import folium
import requests
import pandas as pd
import polyline
from StravaMap.models import Activity
from StravaMap.models import Col
from StravaMap.models import Col_counter
from StravaMap.models import Strava_user
from StravaMap import cols_tools as ct
from StravaMap.col_dbtools import *
from StravaMap.vars import get_default_departement, get_map_center, get_strava_user, get_strava_user_id
from django.db.models import Max

# Create your views here.

###################################################################
#   Base Map
###################################################################

def base_map(request):
                    
    # Make your map object
    main_map = folium.Map(location=get_map_center(), zoom_start = 6) # Create base map

    conn = create_connection('db.sqlite3')    
    
    feature_group_1000m = folium.FeatureGroup(name="Entre 0 et 1000 m").add_to(main_map)    
    feature_group_2000m = folium.FeatureGroup(name="Entre 1000 et 2000 m").add_to(main_map)    
    feature_group_3000m = folium.FeatureGroup(name="Au dessus de 2000 m").add_to(main_map)  
        
    folium.LayerControl().add_to(main_map)

    # Les cols passés
    colOK = cols_effectue(conn)    
    listeOK = []
    for oneCol in colOK:        
        listeOK.append(oneCol[3])   # col_code
        
    # Tous les cols        
    myColsList =  select_all_cols(conn,get_default_departement())         
    # Plot Cols onto Folium Map
    for oneCol in myColsList:
        myCol = ct.PointCol()
        myCol.setPoint(oneCol)
        location = [myCol.lat,myCol.lon]
        colColor = "red"
        if myCol.col_code in listeOK :
            colColor = "green"

        # Altitude
        if  myCol.alt < 1000:            
            folium.Marker(location, popup=myCol.name,icon=folium.Icon(color=colColor, icon="flag")).add_to(feature_group_1000m)        
        if  myCol.alt > 999 and myCol.alt < 2000 :            
            folium.Marker(location, popup=myCol.name,icon=folium.Icon(color=colColor, icon="flag")).add_to(feature_group_2000m)        
        if  myCol.alt > 1999 :            
            folium.Marker(location, popup=myCol.name,icon=folium.Icon(color=colColor, icon="flag")).add_to(feature_group_3000m)        

    
    main_map_html = main_map._repr_html_() # Get HTML for website

    context = {
        "main_map":main_map_html
    }
                                    
    return render(request, 'index.html', context)

###################################################################
#   Connected Map
###################################################################

def connected_map(request):
        
    # Make your map object    
    main_map = folium.Map(location=get_map_center(), zoom_start = 6) # Create base map 
    user = request.user # Pulls in the Strava User data
    strava_login = user.social_auth.get(provider='strava') # Strava login
    token_type = strava_login.extra_data['token_type'] 
    access_token = strava_login.extra_data['access_token'] # Strava Access token
    refresh_token = strava_login.extra_data['refresh_token'] # Strava Refresh token
    expires = strava_login.extra_data['expires'] 
    
    activites_url = "https://www.strava.com/api/v3/athlete/activities"
    
    myUser_sq = Strava_user.objects.all().filter(strava_user = user)

    if myUser_sq.count() == 0:
        myUser = Strava_user()
        myUser.last_name = user
        myUser.first_name = user
        myUser.token_type = token_type
        myUser.access_token = access_token
        myUser.refresh_token = refresh_token
        myUser.strava_user = user
        myUser.expire_at = expires
        myUser.save()
    else:
        for oneOk in myUser_sq:
            myUser = oneOk
            myUser.access_token = access_token
            myUser.refresh_token = refresh_token
            myUser.expire_at = expires
            myUser.save()
    
    
    # Get activity data
    header = {'Authorization': 'Bearer ' + str(access_token)}
    
    activity_df_list = []

    select_max_act_date = Activity.objects.all().aggregate(Max('act_start_date'))
    ze_date = select_max_act_date["act_start_date__max"]
    ze_epoc = int(ze_date.timestamp())
    un_d_epoc = 86400
    un_jour_avant = ze_epoc - un_d_epoc
    
    param = {'after': un_jour_avant , "per_page": 200}
    #param = {}
    
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
    myColsList =  select_all_cols(conn,get_default_departement())        
            
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
        act_status = 1 # not analyzed
        strava_user = get_strava_user_id()

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
                
        insert_col_perform(conn,strava_id, AllVisitedCols)
        compute_cols_by_act(conn,strava_user,strava_id)
                    
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

def col_map(request, col_id):

    conn = create_connection('db.sqlite3')
    myColsList =  getCol(conn,col_id)     
    
    
    for oneCol in myColsList:
        myCol = ct.PointCol()
        myCol.setPoint(oneCol)
        col_location = [myCol.lat,myCol.lon]
        colColor = "blue"
        map = folium.Map(col_location, zoom_start=15)
        folium.Marker(col_location, popup=myCol.name,icon=folium.Icon(color=colColor, icon="flag")).add_to(map)      

    map_html = map._repr_html_()
    
    context = {
        "main_map": map_html,
        "col_id" : col_id,        
    }
        
    return render(request, 'index.html', context)

def act_map(request, act_id):

    ct.refresh_access_token()

    myActivity_sq = Activity.objects.all().filter(act_id = act_id)

    USER = get_strava_user()
    userList = Strava_user.objects.all().filter(strava_user = USER)
    for userOne in userList:
            myUser = userOne
            access_token = myUser.access_token                

    for myActivity in myActivity_sq:            
            strava_id =  myActivity.strava_id
            act_statut = myActivity.act_status
                    
    activites_url = "https://www.strava.com/api/v3//activities/"+str(strava_id)
    
    # Get activity data
    header = {'Authorization': 'Bearer ' + str(access_token)}            
    param = {'id': strava_id}
    
    activities_json = requests.get(activites_url, headers=header, params=param).json()
    activity_df_list = []
       
    activity_df_list.append(pd.json_normalize(activities_json))
    
    # Get Polyline Data
    activities_df = pd.concat(activity_df_list)        
        
    activities_df = activities_df.dropna(subset=['map.summary_polyline'])
    
    activities_df['polylines'] = activities_df['map.summary_polyline'].apply(polyline.decode)
    
    # Centrage de la carte
                       
    centrer_point = ct.map_center(activities_df['polylines'])           
    map_zoom = ct.map_zoom(centrer_point,activities_df['polylines'])    
    
    map = folium.Map(location=centrer_point, zoom_start=map_zoom)
                                           
    # Plot Polylines onto Folium Map

    myGPSPoints = []
    
    for pl in activities_df['polylines']:
        if len(pl) > 0: # Ignore polylines with length zero (Thanks Joukesmink for the tip)
            folium.PolyLine(locations=pl, color='red').add_to(map)                
            myPoint = ct.PointGPS()                
            myPoint = pl                            
            myGPSPoints.append(myPoint)


    ## Col Display
    conn = create_connection('db.sqlite3')
    myColsList =  getColByActivity(conn,strava_id)     
    
    
    for oneCol in myColsList:
        myCol = ct.PointCol()
        myCol.setPoint(oneCol)
        col_location = [myCol.lat,myCol.lon]
        colColor = "blue"        
        folium.Marker(col_location, popup=myCol.name,icon=folium.Icon(color=colColor, icon="flag")).add_to(map)      
        ##### Count Update #####
                   
            
    # Return HTML version of map
    map_html = map._repr_html_() # Get HTML for website
    context = {
        "main_map":map_html        
    }

    strava_user = get_strava_user_id()

    ## Check col passed new
    if act_statut == 0:
        recompute_activity(strava_id, activities_df,strava_user)
                    
    return render(request, 'index.html', context)


def act_map_by_col(request,col_id,act_id):
    print("col_id = ",col_id)        
    return  act_map(request, act_id)

def col_map_by_act(request,act_id,col_id):
    print("act_id = ",act_id)        
    #return HttpResponse("You're looking at question")
    return  col_map(request, col_id)

##########################################################################

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
                                                                        
class ColsDetailView(generic.DetailView):
	# specify the model to use    
    model = Col    
    




 
    
    
    
    
    