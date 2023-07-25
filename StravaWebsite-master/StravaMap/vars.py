########################
STRAVA_USER_ID = 366232
USER = "tpascal" 
########################
# Also in settings.py
########################
APP_CLIENT_ID = '2711'
SOCIAL_AUTH_STRAVA_SECRET = '144e2d05e4b1b91f095dbafe6b40fbc4a9d0933e'
########################
#DEPARTEMENT = "00"
COUNTRY = "FRA"
DEPARTEMENT = "06"
COLOMARS = [43.76663720260908, 7.2192623894882155]
VALENCE = [44.931782895231485, 4.884539872983281]
########################

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

