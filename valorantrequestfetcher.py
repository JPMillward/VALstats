#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pragma once
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
        print(f"Requesting {search_parameter} from {api_end_point}")
        self.search_param = search_parameter
        self.end_point = api_end_point
        self.region = region
        return


    def attempt_query(self):
        try:
           r = requests.get( self.region + self.end_point + self.search_param, headers = { env.api_header : env.match_key } )
           
           if self.validate_response(r.status_code):
               return r.json()
           else: 
               return r.status_code
 
        except: return print('Failed to successfully execute query. Check network connection')   
    
    
    def validate_response(self, response):
        if response == 200: 
            return True
        else: 
            return False