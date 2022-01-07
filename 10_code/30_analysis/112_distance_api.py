import requests
import json
import pprint as pp
import numpy as np
import pandas as pd
import re
import sys
import geopandas as gpd


def extract_distance(response):
    #Calculate the distance
    #km_m converter is used to convert km to miles
    km_m_converter=0.621371
    #distance is in km
    distance=response.json()['rows'][0]['elements'][0]['distance']['text'].split()[0]
    distance = distance.replace(',', '')
    return float(distance)*km_m_converter


def extract_duration(response):
    #Calculate the duration it takes
    try:
        min_in_days=1440
        min_in_hour=60
        duration=response.json()['rows'][0]['elements'][0]['duration']['text'].split()
        if len(duration)!=2:
            if duration[1]=='days' or duration[1]=='day':
                duration=float(duration[0])*min_in_days + float(duration[2])*min_in_hour
            elif duration[1]=='hours' or duration[1]=='hour':
                duration=float(duration[0])*min_in_hour + float(duration[2])
        else:
            duration=duration[0]
    except:
        return np.nan
    return duration

def extract_fare(response):

    fare=response.json()['rows'][0]['elements'][0]['fare']['text'].split()[0]
    return fare





def main_distance(org_y,org_x,dest_y,dest_x,data,i):
    api_key="AIzaSyAqWiye83cMRhMGBq2M5fesfUuO1NT4lbw"
    #adding the three different type of mode
    for mode in ['walking','driving','transit']:

        #extract detail from API
        url =  "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+org_y+"%2C"+org_x+"&destinations="+dest_y+"%2C"+dest_x+"&mode="+mode+"&key="+api_key
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        #print(response.json())

        if response.json()['rows'][0]['elements'][0]['status'] == "ZERO_RESULTS":
        #if response.json()['status']== "ZERO_RESULTS":
            break
        else:
            #Calculate distance and duration
            distance=extract_distance(response)
            duration=extract_duration(response)

            #if mode =='transit' and "fare" in response.json()['rows'][0]['elements'][0]:
            #    fare=extract_fare(response)
            #    col3='fare_in_dollars'
            #    data.loc[i,col3]=fare

            col1='early_2020_distance_by_'+mode+' (miles)'
            col2='early_2020_duration_by_'+mode+' (minutes)'
            #print("Distance: ",distance)
            #print("Duration: ", duration)
            data.loc[i,col1]=distance
            data.loc[i,col2]=duration




def main_distance1(org_y,org_x,dest_y,dest_x,data,i):
    api_key="AIzaSyAqWiye83cMRhMGBq2M5fesfUuO1NT4lbw"
    #adding the three different type of mode
    for mode in ['walking','driving','transit']:

        #extract detail from API
        url =  "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+org_y+"%2C"+org_x+"&destinations="+dest_y+"%2C"+dest_x+"&mode="+mode+"&key="+api_key
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        #print(response.json())

        if response.json()['rows'][0]['elements'][0]['status'] == "ZERO_RESULTS":
        #if response.json()['status']== "ZERO_RESULTS":
            break
        else:
            #Calculate distance and duration
            distance=extract_distance(response)
            duration=extract_duration(response)

            #if mode =='transit' and "fare" in response.json()['rows'][0]['elements'][0]:
            #    fare=extract_fare(response)
            #    col3='fare_in_dollars'
            #    data.loc[i,col3]=fare

            col1='Starbucks_distance_by_'+mode+' (miles)'
            col2='Starbucks_duration_by_'+mode+' (minutes)'
            #print("Distance: ",distance)
            #print("Duration: ", duration)
            data.loc[i,col1]=distance
            data.loc[i,col2]=duration



def load_data():
    #input the data
    input_filename = "30_campuses_w_dist_to_nearest_pp"
    print(input_filename)
    #data=gpd.read_file("../../20_intermediate_files/"+input_filename+".geojson")

    data=pd.read_csv("../../20_intermediate_files/"+input_filename+".csv")
    #data = data[data['Longitude_left'].notna()]
    data=data.drop_duplicates(subset=['School Name'])
    count=0
    for i,r in data.iterrows():
        count+=1
        print(count)
        #extracting the polling location and passing the lat long for college and polling into main_distance
        #polling_location=list(data.loc[i,'nearest_polling_geometry'][7:-1].split())
    
        x_pol,y_pol=data.loc[i,'Longitude_2020_early'],data.loc[i,'Latitude_2020_early']
        #x_target,y_target=data.loc[i,'Longitude_target'],data.loc[i,'Latitude_target']

        #x_starbucks,y_starbucks=data.loc[i,'Longitude_starbucks'],data.loc[i,'Latitude_starbucks']
        x_col,y_col=data.loc[i,'centroid_long'],data.loc[i,'centroid_lat']
  
        main_distance(str(y_col),str(x_col),str(y_pol),str(x_pol),data,i)

        #main_distance1(str(y_col),str(x_col),str(y_starbucks),str(x_starbucks),data,i)

    
    _=data.to_csv("../../20_intermediate_files/"+input_filename+".csv")


    #_=data.to_file("../../20_intermediate_files/"+input_filename+".geojson", driver="GeoJSON")
    
    #geo_df.to_file(
    #"../../20_intermediate_files/10_HIFLD_campus_polygons.geojson", driver="GeoJSON")

load_data()
#main_distance(str(61.19213),str(-149.815706),str(41.313971), str(-105.571927))
