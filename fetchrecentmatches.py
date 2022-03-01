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
import constants as c

class Fetcher():

    def __init__(self, search_param, file_location):
        self.search_param = search_param
        self.file_location = file_location
        self.attempt_connection()

    def attempt_connection(self):
        try:
           r = requests.get( env.region + env.match_by_queue + self.search_param, headers = { env.api_header : env.match_key } )
           self.json = r.json()
           self.write_out()
        except: return print('Failed to successfully execute query. If this persists, fix it.\n Trying again in 15 minutes.')
       
    def write_out(self):
        with open(self.file_location, 'a') as file:
            for item in self.json['matchIds']:
                file.write(item + '\n')
        print(f'Succesfully added {len(self.json["matchIds"])} matches to list')

search_field = 'competitive'
file_location = '/home/brokenmaze/pyprojects/compmatchids.txt'
#file_location = '/Users/johnm/Documents/GitHub/VALstats/compmatchids.txt'
Fetcher(search_field, file_location)