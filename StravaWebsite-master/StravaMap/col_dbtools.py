from aifc import Error
import sqlite3
from StravaMap import cols_tools as ct
from StravaMap.models import Col_counter as cc, Col_perform as cp
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

def select_all_cols06(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT col_name,col_alt,col_lat,col_lon,col_code FROM StravaMap_col WHERE col_code like '%FR-06%'")

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

def compute_cols( myUser_id,myActivity_id):
    
    #remove all
    #cc.objects.filter(user_id=myUser_id).delete()        

    #print("activity_id = ", myActivity_id)
                
    perf = cp.objects.filter(strava_id=myActivity_id).values_list("col_code", flat=True)
                    
    for codeCode in perf:
        # Update if Exists
        nbRet = cc.objects.filter( user_id=myUser_id, col_code=codeCode).update(col_count=F('col_count')+1)       
        # Else Insert new Col
        if nbRet == 0:            
            new_cc = cc()        
            new_cc.col_code = codeCode
            new_cc.col_count = 1
            new_cc.user_id = myUser_id        
            new_cc.save()      
        
def cols_effectue(conn):

    cur = conn.cursor()
    cur.execute("select col_name, col_alt, col_count from StravaMap_col C , StravaMap_col_counter M where C.col_code = M.col_code order by M.col_count desc")
    rows = cur.fetchall()

    return rows

            
        
        
        

      
        
    



    
    
    
    
    


    




