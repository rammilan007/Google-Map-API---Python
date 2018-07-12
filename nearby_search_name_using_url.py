# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 14:38:12 2018

@author: ram.verma
"""
import os
import googlemaps
import pandas as pd
import numpy as np
import csv
import urllib.request, json
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

oyo=pd.read_csv('C:/Users/ram.verma/Desktop/hotels_nearby_search/check_gmb.csv')
#oyo=pd.read_csv('check_gmb.csv')
oyo['oyo_name']=oyo['oyo_name'].str.upper()
oyo['alternate_name']=oyo['alternate_name'].str.upper()

oyo['oyo_name_m_frac']='default'
oyo['alt_name_m_frac']='default'
oyo['oyoname_match_status']='default'
oyo['altname_match_status']='default'
oyo['matched_alt_name']='default'
oyo['matched_oyo_name']='default'
key='put google api key here'
in_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
radius='1000'
type='business'      #---remove this to get all type names
#keyword='OYO'

#location='{},{}'.format(oyo.latitude[0],oyo.longitude[0])

#end_url = 'location={}&radius={}&type={}&key={}'.format(location,radius,type,key)
#request = in_url + end_url
#request

#response = urllib.request.urlopen(request).read()
#Loads response as JSON
#response = json.loads(response)
#response.keys()
#response['results'][0]['geometry']['location']   # to get location coordinates as well
#n=len(response['results'])
#hotel_api_name=list()
#for i in range(0,n):
#    hotel_api_name.append(response['results'][i]['name'].upper())

l=len(oyo)
count=0
for i in range(l) :
    
    location='{},{}'.format(oyo.latitude[i],oyo.longitude[i])
    end_url = 'location={}&radius={}&type={}&key={}'.format(location,radius,type,key)
    request = in_url + end_url
    response = urllib.request.urlopen(request).read()
    response = json.loads(response)
    n=len(response['results'])
    hotel_api_name=list()
    for k in range(0,n):
        hotel_api_name.append(response['results'][k]['name'].upper())
    
    o_frac_list=list()
    a_frac_list=list()
    o_name=oyo['oyo_name'][i]
    a_name=oyo['alternate_name'][i]
    
    for j in hotel_api_name :
        o_m_frac=similar(o_name,j)
        o_frac_list.append(o_m_frac)
        a_m_frac=similar(a_name,j)
        a_frac_list.append(a_m_frac)
    o_m=max(o_frac_list)
    o_m_index=o_frac_list.index(o_m)
    a_m=max(a_frac_list)
    a_m_index=a_frac_list.index(a_m)
    oyo.matched_oyo_name[count]=hotel_api_name[o_m_index]
    oyo.oyo_name_m_frac[count]=o_m
    oyo.matched_alt_name[count]=hotel_api_name[a_m_index]
    oyo.alt_name_m_frac[count]=a_m
    if o_m>0.5 :
        if o_m>0.9 : oyo.oyoname_match_status[count]=1 
        else :  oyo.oyoname_match_status[count]='P'
    else :  oyo.oyoname_match_status[count]=0
    
    if a_m>0.5 :
        if a_m>0.9 : oyo.altname_match_status[count]=1 
        else :  oyo.altname_match_status[count]='P'
    else :  oyo.altname_match_status[count]=0
    count=count+1
    
    if count==10 : break

oyo['comment']='default'

for i in range(l):
    if oyo.oyoname_match_status[i]==1 : oyo.comment[i]='oyo_name_match'
    if oyo.altname_match_status[i]==1 : oyo.comment[i]='alt_name_match'
    if (oyo.oyoname_match_status[i]==1 and oyo.altname_match_status[i]==1) : oyo.comment[i]='both match'
    if (oyo.oyoname_match_status[i]=='P' and oyo.altname_match_status[i]!=1) :  oyo.comment[i]='review'
    if (oyo.oyoname_match_status[i]==0 and oyo.altname_match_status[i]==0) : oyo.comment[i]='create'
    if (oyo.altname_match_status[i]=='P' and oyo.oyoname_match_status[i]==0) : oyo.comment[i]='review'
#oyo.to_csv('oyo.csv')
