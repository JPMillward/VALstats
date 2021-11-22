#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 18:26:31 2021

@author: johnm

Py for making requests to the VALORANT API
Need API key with access

SUN NOTES:
    Got sidetracked building a general algorithm for crawling jsons
    currently succeeds in navigating through lists and dictionaries
    ^ Might be crazy scope creep. Evaluate after sleep
    
    -Primary Key & Foreign Key patterns or no?
    -Relational Database de/re construction?

"""

import pandas as pd
import requests
import personal as env
import constants as c

search_param = '379a1d35-1d93-4aee-bd77-918fa97a2d80'
r = requests.get( env.match_by_id + search_param, headers = { env.api_header : env.match_key })

matchinfo = r.json()['matchInfo']
players = r.json()['players']
coaches = r.json()['coaches']
teams = r.json()['teams']
rounds = r.json()['roundResults']



class TableMaker():
    
    def __init__(self, dictionary):
        print('init')
        self.json = dictionary
        self.dataframes = {}
        self.scan_fields(self.json)
        #print(self.json)
        
    def scan_list(self, input_list):
        if len(input_list) == 0: return print("Empty List")
        if isinstance(input_list[0], dict):
             if not self.validate_series(input_list): return print("Something Went Wrong")
             self.scan_dict(input_list[0])
        elif isinstance(input_list[0], list):
            self.scan_list(input_list)
        else:
            print(input_list)
    
    
    def scan_dict(self, input_dictionary):
        if len(input_dictionary) == 0: return print('Empty Dictionary')
        for key,value in input_dictionary.items():
            if isinstance(value, dict):
                print(f'{key} returns a dictionary. Further delving necessary.')
                self.scan_dict(value)
            elif isinstance(value, list):
                print(f'{key} returns a list. Further delving necessary.')
                self.scan_list(value)
            else:
                print(f'{key} : {value}')
        
    def scan_fields(self, input_input):
        if len(input_input) == 0: return
        for key,value in input_input.items(): 
            if isinstance(value, list):
               self.scan_list(value)
                
            elif isinstance(value, dict):
                print(f'{key} returns a dictionary. Further delving necessary.')
                self.scan_dict(value)

            else: None
        print('Done')
        
    def validate_series(self, input_list):
        for x in range(len(input_list)):
            if input_list[0].keys() != input_list[x].keys():
                return False
        return True
        
        
TableMaker(r.json())
#print(rounds[0].keys())

#df =  pd.DataFrame(rounds)
#print(df.keys())

"""
for round in range(len(rounds)):
    for pair in rounds[round].items():
        if isinstance(pair[1], dict):
            print(f'{pair}: \n')
            print(pair[1].items())
        else: print(pair)
"""
'''
MATCH API NAVIGATION

-matchinfo
-players
-coaches
-teams                
-roundResults

'''



# 379a1d35-1d93-4aee-bd77-918fa97a2d80