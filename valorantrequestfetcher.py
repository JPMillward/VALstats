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

class ValorantFetcher():

    def __init__(self, api_end_point, region, search_parameter):
        print(api_end_point, region, search_parameter)
        self.search_param = search_parameter
        self.end_point = api_end_point
        self.region = region
        return


    def attempt_query(self):
        try:
           r = requests.get( self.region + self.end_point + self.search_param, headers = { env.api_header : env.match_key } )
           if self.validate_response(r.response):
               return r.json()
           else return print(f"Error: {r.response}")
        except: return print('Failed to successfully execute query. If this persists, fix it.\n Trying again in 15 minutes.')   
    
    def validate_response(self, response):
        print(response)
        if response == 200: return True
        else: return False