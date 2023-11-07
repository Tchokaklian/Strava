########################
STRAVA_USER_ID = 366232
USER = "tpascal" 
########################
# Also in settings.py
########################
APP_CLIENT_ID = '2711'
#SOCIAL_AUTH_STRAVA_SECRET = '144e2d05e4b1b91f095dbafe6b40fbc4a9d0933e'
SOCIAL_AUTH_STRAVA_SECRET = "c55adf130e27f791abf1b51078239c43e4e59693"
COUNTRY = "FRA"
DEPARTEMENT = "06"
COLOMARS = [43.76663720260908, 7.2192623894882155]
VALENCE = [44.931782895231485, 4.884539872983281]
########################
MONTHES = ["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]

def get_strava_user_id():
    return STRAVA_USER_ID

def get_strava_user():    
    return USER

def get_app_client_id():
    return APP_CLIENT_ID

def get_app_client_secret():
    return SOCIAL_AUTH_STRAVA_SECRET   

def get_map_center():        
    return COLOMARS

def get_default_departement():    
    return DEPARTEMENT

def get_default_country():    
    return COUNTRY

def display_year_month(month):
    ret = "not found"
    if month > 0 and month < 13:
        ret = MONTHES[month-1]
    else:
        print("display_year_month / not found:",str(month))
    return ret
