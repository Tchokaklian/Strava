from StravaWebsite import settings
from StravaWebsite.settings import APP_CLIENT_ID, COLOMARS, COUNTRY, DEPARTEMENT, LEVEL_COL_DEBUG, SALTA, SOCIAL_AUTH_STRAVA_SECRET

MONTHES = ["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]

def f_debug_col():
    ret = False
    if LEVEL_COL_DEBUG > 0:
        ret = True
    return ret    

def f_debug_trace(classe,function,value):      
    print("Debug >>> Class: ", classe, " >>> function: ",function, " >>> values: ",value)


def set_strava_user_id(suid):
    settings.strava_user_id = suid    
    return 0

def get_strava_user_id():
    return settings.strava_user_id

def set_strava_user(user):
    f_debug_trace("vars.py","set_strava_user",user)
    settings.strava_user = user
    return 0

def get_strava_user():    
    return settings.strava_user

def get_app_client_secret():
    return SOCIAL_AUTH_STRAVA_SECRET   

def get_app_client_id():
    return APP_CLIENT_ID

def get_map_center(continent):        
    ret = COLOMARS
    if continent == "SOUTHAMERICA":
        ret = SALTA        
    return ret

def get_default_departement():    
    return DEPARTEMENT

def get_default_country():    
    return COUNTRY

def display_year_month(month):
    ret = "not found"
    if month > 0 and month < 13:
        ret = MONTHES[month-1]
    else:
        f_debug_trace("vars.py","display_year_month","not found:"+str(month))        
        ret = "not found"
    return ret
