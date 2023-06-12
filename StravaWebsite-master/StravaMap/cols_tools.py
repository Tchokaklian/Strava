from numpy import sin, cos, arccos, pi, round
import numpy as N

####################################################

class PointGPS:
    "Definition d'un point geometrique"
    def __init__(self):
        self.lat = 0
        self.lon = 0

####################################################

GPSPointsList = list[PointGPS] 

####################################################

class PointCol(PointGPS):
    "Definition d'un point col geometrique"
    def __init__(self):
        self.lat = 0
        self.lon = 0
        self.alt = 0
        self.name = "colName"
        self.col_code = "-"


####################################################        

ColsList = list[PointCol]        

####################################################

def rad2deg(radians):
    degrees = radians * 180 / pi
    return degrees

####################################################

def deg2rad(degrees):
    radians = degrees * pi / 180
    return radians

####################################################

def getDistanceBetween2Points(p1:PointGPS, p2:PointGPS):
    calcDistance = 0           
    calcDistance = getDistanceBetweenPoints(p1.lat,p1.lon,p2.lat,p2.lon,'kilometers')
    return calcDistance

####################################################

def getDistanceBetweenPoints(latitude1, longitude1, latitude2, longitude2, unit = 'miles'):
    
    theta = longitude1 - longitude2
    
    distance = 60 * 1.1515 * rad2deg(
        arccos(
            (sin(deg2rad(latitude1)) * sin(deg2rad(latitude2))) + 
            (cos(deg2rad(latitude1)) * cos(deg2rad(latitude2)) * cos(deg2rad(theta)))
        )
    )
    
    if unit == 'miles':
        return round(distance, 2)
    if unit == 'kilometers':
        return round(distance * 1.609344, 5)        

####################################################

def getColsVisited(colsList: ColsList, pointsList: GPSPointsList):
    visitedColList = []
    for onePoint in pointsList:
        myGPSPoint = PointGPS()
        myGPSPoint.lat = onePoint[0]
        myGPSPoint.lon = onePoint[1]
        laList = getColsVisitedList(colsList,myGPSPoint)
        visitedColList = visitedColList + laList
    
    visitedColList = N.unique(visitedColList) 

    return visitedColList


####################################################

def getColsVisitedList(colsList: ColsList, onePoint: PointGPS ):
    visitedList = []
    for oneCol in colsList:        
        myColPoint = PointCol()
        myColPoint.lat = oneCol.lat
        myColPoint.lon = oneCol.lon
        myColPoint.name = oneCol.name
        myColPoint.col_code = oneCol.col_code
        distance = getDistanceBetween2Points(myColPoint,onePoint)        
        if distance < 0.250:         
            visitedList.append(myColPoint.col_code)                            
    return visitedList

####################################################

def getListColsUniques(colsList: ColsList):
    colsList = N.unique(colsList) 
    return colsList
    


        







    