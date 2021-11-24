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
        #print('init')
        self.json = dictionary
        self.all_keys = []
        self.dict_keys = []
        self.list_keys = []
        self.json_nav = {}
        self.dataframes = {}
        
        self.scan_fields(self.json)
        #print(self.json)
        
    def scan_list(self, input_list, key = None):
        if len(input_list) == 0: return #print("Empty List")
        
        if isinstance(input_list[0], dict):
             if not self.validate_series(input_list): return print("Something Went Wrong")
             #print('Found valid list of dictionaries')
             self.dict_keys.append(key)
             self.dataframes.update({key:input_list})
             self.scan_dict(input_list[0], key)
        
        elif isinstance(input_list[0], list):
            self.list_keys.append(key)
            self.scan_list(input_list)
        
        else:
            #print(input_list)
            None
    
    
    def scan_dict(self, input_dictionary, dict_key = None):
        if len(input_dictionary) == 0: return #print('Empty Dictionary')
        for key,value in input_dictionary.items():
            self.all_keys.append(key)
            self.json_nav[dict_key].append(key)
            if isinstance(value, dict):
                #print(f'{key} returns a dictionary. Further delving necessary.')
                self.dict_keys.append(key)
                self.json_nav.update({key:[]})
                self.scan_dict(value, key)
            
            elif isinstance(value, list):
                #print(f'{key} returns a list. Further delving necessary.')
                self.json_nav.update({key:[]})
                self.list_keys.append(key)
                self.scan_list(value,key)
            
            else:
                #print(f'{key} : {value}')
                None

                
        
    def scan_fields(self, input_input):
        if len(input_input) == 0: return
        for key,value in input_input.items(): 
            self.all_keys.append(key)
            if isinstance(value, list):
                self.json_nav.update({key : []})
                self.scan_list(value, key)
                
            elif isinstance(value, dict):
                #print(f'{key} returns a dictionary. Further delving necessary.')
                self.json_nav.update({key : []})
                self.scan_dict(value, key)

        self.validate_fields()
        print('Done')
    
        
    def validate_fields(self):
        for key, value in self.json_nav.items():
            for x in range(len(value)):
                print(f'{key} : {value[x]}')
                if self.is_nested(value[x]):
                    print(f'{value[x]} is nested in {key}')
                    print(self.is_nested(value[x]))
                    
            
        
    def validate_series(self, input_list):
        for x in range(len(input_list)):
            if input_list[0].keys() != input_list[x].keys():
                return False
        return True
        
    def is_nested(self, input_key):
        #print(input_key)
        if input_key in self.json_nav.keys():
            #print(f'{input_key} is a dictionary key')
            return True
        return False
        
        
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