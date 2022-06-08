import math
from math import radians, cos, sin, asin, sqrt
def bearing(pointA, pointB):

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)


    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def distance(pointA,pointB):
    lat1,lon1 = pointA
    lat2,lon2=pointB
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r
def timephrase(time):
    hourphrase = ''
    minutephrase = ''
    minutes = int((time-int(time))*60)
    hours = int(time)
    if hours != 1:
        hourphrase='s'
    if minutes != 1:
        minutephrase = 's'
    return ["{} hour{} and {} minute{}".format(hours,hourphrase,minutes,minutephrase),time]

    
def time(distance):
    return {'F-16 (Afterburners)':timephrase(distance/2778),'F-16':timephrase(distance/1166),'737':timephrase(distance/852),'787':timephrase(distance/902),'C172':timephrase(distance/224.7),'A318':timephrase(distance/825),'Carrier':timephrase(distance/33)}

def fuel(time):
    time = time*60
    return {'F-16 (Afterburners)':time*1066,'F-16':time*133,'737':time*83.3,'787':time*180,'C172':time*8,'A318':time*68.25,'Carrier':0}
    #return {'F-16 (Afterburners)':0,'F-16':0,'737':0,'787':0,'C172':0,'A318':0}

