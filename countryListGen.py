import pandas as pd
import random 
from random import randrange
import datetime
from random import randint
from datetime import timedelta
import numpy as np
import re
from faker import Faker 
from math import sin, cos, sqrt, atan2, radians

def distance_travel_variable(distance):
    if distance < 5000:
        distance_Travel=randint(1,3)
    elif distance <10000:
        distance_Travel=randint(4,7)
    else :
            distance_Travel=randint(8,10)
    return  (distance_Travel)

#Function that returns the latitude for a spesific country
def DLatitudeFinder(country,ISO):
    lat=ISO.loc[country,'longitude']
    return(lat)


#Function that returs the longtitude for a spessific country
def DlongitudeFinder(country,ISO):
    lat=ISO.loc[country,'longitude']
    return(lat)


def DistanceCalculator(country1,country2,ISO):

    R = 6373.0

    lat1 = radians(DLatitudeFinder(country1, ISO))
    lon1 = radians(DlongitudeFinder(country1, ISO))
    lat2 = radians(DLatitudeFinder(country2, ISO))
    lon2 = radians(DlongitudeFinder(country2, ISO))
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    
    return(distance+distance*0.1)



## Create the Dataset
ISO=pd.read_csv('Countries.csv')
countries=ISO['name']
ISO=ISO.set_index('name')
df = pd.DataFrame()
for i in range(5000):

    #Location and Distance
    From=random.choice(countries)#Add weights based on the real dataset values Netherlands 60% etc
    To=random.choice(countries)#Add weights based on the real dataset values Netherlands 60% etc
    originCode=ISO.loc[From,'country']
    destinationCode=ISO.loc[To,'country']
    distance=DistanceCalculator(From,To,ISO)

    #COST
    cost=random.randint(1,9)*distance


    #TIME
    
    startDate=datetime.date(2022, randint(1,12),randint(1,28))
    EDA=startDate+datetime.timedelta(randint(1,15))
    ADA=startDate + (EDA - startDate) * random.random()
    TravelTime=(ADA-startDate).days
    WasteTime=(EDA-ADA).days
    
    #Status
    ini_string=str(random.choices(["IM", "EX"],weights=[6,4])).strip()
    status=re.sub('[\W_]+', '', ini_string)
    

    df = df.append({'Sender':From,
                    'OriginCodde':originCode,
                    'Receiver':To,
                    'DestinationCode':destinationCode,
                    'Status':status,
                    'Cost':cost,
                    'DepartureDate':startDate,
                    'EstimatedDA':EDA,
                    'ActualDA':ADA,
                    'TravelTime(Days)':TravelTime,
                    'WasteTime(Days)':WasteTime,
                    'Distance':distance,
                    'LostMoney$':WasteTime*200*distance/5000},#200 is the money we lose per day 
                    ignore_index=True)


    




print(df)
df.to_csv('FictionalDataset.csv')