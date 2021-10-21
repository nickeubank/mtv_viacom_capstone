import requests
import json
import pprint as pp
import numpy as np
import pandas as pd
import re
def extract_distance(response):
    distance=response.json()['rows'][0]['elements'][0]['distance']['text'].split()[0]
    distance = distance.replace(',', '')
    return float(distance)*0.621371


def extract_duration(response):
    try:
        duration=response.json()['rows'][0]['elements'][0]['duration']['text'].split()
        if len(duration)!=2:
            if duration[1]=='days' or duration[1]=='day':
                duration=float(duration[0])*1440 + float(duration[2])*60
            elif duration[1]=='hours' or duration[1]=='hour':
                duration=float(duration[0])*60 + float(duration[2])
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

    for mode in ['walking','driving','transit']:
        
        url =  "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+org_y+"%2C"+org_x+"&destinations="+dest_y+"%2C"+dest_x+"&mode="+mode+"&key="+api_key

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        print("MODE: ", mode)
        print(response.text)
        if response.json()['rows'][0]['elements'][0]['status'] == "ZERO_RESULTS":
            break
        else:
            
            distance=extract_distance(response)
            duration=extract_duration(response)
      
            #if mode =='transit' and "fare" in response.json()['rows'][0]['elements'][0]:
            #    fare=extract_fare(response)
            #    col3='fare_in_dollars'
            #    data.loc[i,col3]=fare
            
            col1='distance_by_'+mode+' (miles)'
            col2='duration_by_'+mode+' (minutes)'
            print("Distance: ",distance)
            print("Duration: ", duration)
            data.loc[i,col1]=distance
            data.loc[i,col2]=duration
            
    
    
    
def load_data():
    data=pd.read_csv("../20_intermediate_files/subset_college_nearest_poll_2020.csv")
    for i,r in data.iterrows():
        polling_location=list(data.loc[i,'nearest_polling_geometry'][7:-1].split())
        x_pol,y_pol=polling_location[0],polling_location[1]
        x_col,y_col=data.loc[i,'x_centroid'],data.loc[i,'y_centroid']
        main_distance(str(y_col),str(x_col),y_pol,x_pol,data,i)
    _=data.to_csv("../20_intermediate_files/final_college_data_set_distance_API.csv")
    
load_data()
#main_distance(str(61.19213),str(-149.815706),str(41.313971), str(-105.571927))