#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: johnm

Py for making requests to the VALORANT API.
Running every 15 minutes using the folowing daemons
valapicall.service and valapicall.timer
"""
import requests
import personal as env
import sys

class ValorantFetcher():

    def __init__(self, api_end_point, region, search_parameter, output_location):
        print(api_end_point, region, search_parameter, output_location)
        self.search_param = search_parameter
        self.end_point = api_end_point
        self.region = region
        self.output_location = output_location
        self.attempt_connection()

    def attempt_connection(self):
        try:
           print(self.region + self.end_point + self.search_param)
           r = requests.get( self.region + self.end_point + self.search_param, headers = { env.api_header : env.match_key } )
           print(r.json())
           self.json = r.json()
           self.write_out()
        except: return print('Failed to successfully execute query. If this persists, fix it.\n Trying again in 15 minutes.')
       
    def write_out(self):
        with open(self.output_location, 'a') as file:
            for item in self.json:
                file.write(item + ',')
        print(f'Succesfully added {len(self.json["matchIds"])} matches to list')

search_field = 'competitive'
file_location = '/home/brokenmaze/pyprojects/compmatchids.txt'
#file_location = '/Users/johnm/Documents/GitHub/VALstats/compmatchids.txt'

ValorantFetcher(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])