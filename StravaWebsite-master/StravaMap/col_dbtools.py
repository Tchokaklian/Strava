from aifc import Error
import sqlite3
from StravaMap import cols_tools as ct
from StravaMap.models import Activity, Col_counter as cc, Col_perform as cp
from django.db.models import F  


#############################################################################

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

#############################################################################

def select_all_cols(conn, departement):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()

    if departement == "00":
        codeSql = "SELECT col_name,col_alt,col_lat,col_lon,col_code,col_type FROM StravaMap_col"
    else:
        codeSql = "SELECT col_name,col_alt,col_lat,col_lon,col_code,col_type FROM StravaMap_col WHERE col_code like '%FR-"+ departement +"%'"

    cur.execute(codeSql)

    rows = cur.fetchall()
    
    myListeCols = []

    # col indexes
    col_name = 0
    col_alt = 1
    col_lat = 2 
    col_lon = 3
    col_code = 4
    col_type = 5

    for row in rows :                                      
        myCol = ct.PointCol()
        myCol.name = row[col_name]
        myCol.alt = row[col_alt]
        myCol.lat = row[col_lat]        
        myCol.lon = row[col_lon]        
        myCol.col_code = row[col_code]
        myCol.col_type = row[col_type]        
        myListeCols.append(myCol)
                    
    return myListeCols    

#############################################################################
    
def insert_activity (conn, user_id, strava_id, act_name, act_start_date, act_dist, act_den, act_type, act_time, act_power, act_status):
    try:
        cur = conn.cursor()
        sql = "INSERT INTO StravaMap_activity (user_id, strava_id, act_name, act_start_date, act_dist, act_den, act_type, act_time, act_power, act_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        value = (user_id, strava_id, act_name, act_start_date, act_dist, act_den, act_type, act_time, act_power, act_status)
        
        cur.execute(sql, value)
        conn.commit()
        #print("Enregistrement inséré avec succès dans la table StravaMap_activity")                
    except sqlite3.Error as error:
        print("Erreur lors de l'insertion dans la table StravaMap_activity", error)

        
#############################################################################

def delete_activity(conn, strava_id):
    cur = conn.cursor()
    sql = 'DELETE FROM StravaMap_activity WHERE strava_id=?'    
    cur.execute(sql, (strava_id,))
    conn.commit()

def delete_col_perform(conn, strava_id):
    cur = conn.cursor()
    sql = 'DELETE FROM StravaMap_col_perform WHERE strava_id=?'    
    cur.execute(sql, (strava_id,))
    conn.commit()

#############################################################################
    
def insert_col_perform(conn,act_id,rows):
    cur = conn.cursor()
    for row in rows :                 
        sql = "INSERT INTO StravaMap_col_perform (strava_id,col_code) VALUES (?, ?)"    
        value = (act_id, row)
        cur.execute(sql, value)
    conn.commit()      

#############################################################################

def compute_cols_by_act( conn, myUser_id,myActivity_id):
    
    #remove all
    #cc.objects.filter(user_id=myUser_id).delete()        

    #print("activity_id = ", myActivity_id)
                    
    perf = cp.objects.filter(strava_id=myActivity_id).values_list("col_code", flat=True)
                        
    for colCode in perf:        
        
        nbPassage = getActivitiesByCol(conn,colCode)        

        print(" >>>>>>>>>>>>>>>>> Col Matching !!!")

        exists = cc.objects.filter(col_code=colCode, user_id=myUser_id).count()
                
        if exists==0:
            new_cc = cc()
            new_cc.col_code=colCode
            new_cc.col_count=1
            new_cc.user_id=myUser_id
            new_cc.save()            
            print(">>>>>    NEW COL    <<<<<")            
            print(">>>>>"+new_cc.get_col_name()+"<<<<<")
        else:
            my_cc = cc.objects.filter(col_code=colCode, user_id=myUser_id)
            upd_cc = my_cc[0]
            upd_cc.col_count=nbPassage
            upd_cc.save()

        lact = Activity.objects.filter(strava_id=myActivity_id)
        for act in lact:
            act.act_status = 1
            act.save()

                                           
def cols_effectue(conn):

    cur = conn.cursor()
    cur.execute("select col_name, col_alt, col_count, C.col_code from StravaMap_col C , StravaMap_col_counter M where C.col_code = M.col_code order by M.col_count desc")
    rows = cur.fetchall()

    return rows

def getCol(conn,col_id):
    cur = conn.cursor()
    cur.execute("SELECT col_name,col_alt,col_lat,col_lon,col_code FROM StravaMap_col WHERE col_id = "+str(col_id))
    
    rows = cur.fetchall()
    
    myListeCols = []

    # col indexes
    col_name = 0
    col_alt = 1
    col_lat = 2 
    col_lon = 3
    col_code = 4

    for row in rows :                               
        myCol = ct.PointCol()
        myCol.name = row[col_name]
        myCol.alt = row[col_alt]
        myCol.lat = row[col_lat]        
        myCol.lon = row[col_lon]        
        myCol.col_code = row[col_code]
        myListeCols.append(myCol)
                    
    return myListeCols   

###########################################################################################################

def getColByActivity(conn,strava_id):
    cur = conn.cursor()    
    cur.execute("select col_name,col_alt,col_lat,col_lon,P.col_code from StravaMap_col_perform P, StravaMap_col C where P.col_code = C.col_code and strava_id = "+str(strava_id))
        
    rows = cur.fetchall()
    
    myListeCols = []
    
    # col indexes
    col_name = 0
    col_alt = 1
    col_lat = 2 
    col_lon = 3
    col_code = 4

    for row in rows :                               
        myCol = ct.PointCol()
        myCol.name = row[col_name]
        myCol.alt = row[col_alt]
        myCol.lat = row[col_lat]        
        myCol.lon = row[col_lon]        
        myCol.col_code = row[col_code]
        myListeCols.append(myCol)

        #print( myCol.name )
                    
    return myListeCols   
            
###########################################################################################################

def getActivitiesByCol(conn, col_code):                
    cur = conn.cursor()        
    sqlExec = "select act_id from StravaMap_activity A, StravaMap_col_perform P where user_id = 366232 and A.strava_id = P.strava_id and col_code = '"+col_code+"'"
    
    cur.execute(sqlExec)    
    rows = cur.fetchall()    
    myListActivities = 0
        
    for row in rows :                        
        #TODO -        
        myListActivities = myListActivities+1

    #print("col_code", myListActivities)        
                            
    return myListActivities   

###########################################################################################################

def recompute_activity(strava_id, activities_df, strava_user):        

    conn = create_connection('db.sqlite3')

    AllVisitedCols = []
    allCols = []
    myColsList = []
    myGPSPoints = []

    allCols=  select_all_cols(conn,"00")            
    
    for oneCol in allCols:               
        myCol = ct.PointCol()
        myCol.setPoint(oneCol)        
        myColsList.append(myCol)
    
    for pl in activities_df['polylines']:
            if len(pl) > 0:                 
                for onePoint in pl:                    
                    myGPSPoints.append(onePoint)
    
    returnList = ct.getColsVisited(myColsList,myGPSPoints)           
                    
    for ligne in returnList:                
        AllVisitedCols.append(ligne)            

    delete_col_perform(conn,strava_id)                
    insert_col_perform(conn,strava_id, AllVisitedCols)
    compute_cols_by_act(conn,strava_user,strava_id)  

    
    return 0
        
    



    
    
    
    
    


    




