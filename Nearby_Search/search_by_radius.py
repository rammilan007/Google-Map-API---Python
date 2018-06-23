# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 15:45:37 2018

@author: ram.verma
"""
import googlemaps
import geopy.distance
import pandas as pd
import time
key='Put your own Google API KEY here'
gmaps = googlemaps.Client(key)
def nearby_search_by_radius(latitude,longitude,radius=1000,type_='lodging'):
    params = {
            'location': (latitude,longitude),
            'radius': radius,
            'type' : type_,
            'page_token':'',
            #'keyword':'OYO',
            }
    result = gmaps.places_nearby(**params)
    hotel_api_name=list()
    dist=list()
    cd_1=(latitude,longitude)
    if 'next_page_token' in result.keys():
        while 'next_page_token' in result.keys():
            for k in range(len(result['results'])):
                api_name=result['results'][k]['name'].upper()
                hotel_api_name.append(api_name)
                cd_2=(result['results'][k]['geometry']['location']['lat'],result['results'][k]['geometry']['location']['lng'])
                dist.append(geopy.distance.vincenty(cd_1,cd_2).m)
            time.sleep(2)
            params.update({"page_token": result["next_page_token"]})
            result = gmaps.places_nearby(**params)
    if ('next_page_token' in result.keys())==False:
        for j in range(len(result['results'])):
            api_name=result['results'][j]['name'].upper()
            hotel_api_name.append(api_name)
            cd_2=(result['results'][k]['geometry']['location']['lat'],result['results'][k]['geometry']['location']['lng'])
            dist.append(geopy.distance.vincenty(cd_1,cd_2).m)
    d=pd.DataFrame({'name':hotel_api_name,'distance':dist})
    return d
