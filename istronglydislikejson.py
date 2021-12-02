#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Friday Nov 26  05:43:31 2021

@author: BrokenMaze
Tue NOTES:
    Got sidetracked building a general algorithm for crawling jsons
    Something wonky happens during the print. Stuck mentally, need to take a break and come back.
    Meanwhile I should probably focus on the data stuff.

"""

import pandas as pd
import requests
import personal as env
import constants as c

search_param = '1054b5b9-9eab-4322-9ff0-86df58239b8c'
r = requests.get( env.match_by_id + search_param, headers = { env.api_header : env.match_key })

class IHateJson():
    
    def __init__(self, dictionary):
        #print('init')
        self.depth = 0
        self.json = dictionary
        self.json_nav = {}
        self.root = {}
        
        self.scan_fields(self.json)
        print(self.json_nav)
    def scan_list(self, input_list, arg_key):
        if len(input_list) == 0: return print("Empty List: {input_list}")
        self.depth += 1
        print(f"Current Depth: {self.depth}, {arg_key}, List")
        
        if isinstance(input_list[0], dict):
             if self.validate_series(input_list): x = 0
             else: x = self.handle_invalid_series(input_list)
             #print('Found valid list of dictionaries')
             #print(arg_key, '\n', input_list[0])
             new_key = "listof_"+arg_key
             self.json_nav[arg_key].update({new_key : self.depth})
             self.json_nav.update({new_key:{}})
             #print(self.json_nav)
             self.scan_dict(input_list[x], new_key)
             
        elif isinstance(input_list[0], list):
            print('impossible event occurring')
            self.scan_list(input_list)
            
        else: print(input_list)
        
        self.depth -= 1
    
    
    def scan_dict(self, input_dictionary, dict_key):
        if len(input_dictionary) == 0: return #print('Empty Dictionary')
        self.depth += 1
        #print(f"Current Depth: {self.depth}, {dict_key}")
        
        for key,value in input_dictionary.items():
            #print(f"{key}, {value}, {dict_key}")
            self.json_nav[dict_key].update({key:self.depth})
            if isinstance(value, dict):
                #print(f'{key} returns a dictionary. Further delving necessary.')
                self.json_nav.update({ key:{} })
                self.scan_dict(value, key)
            
            elif isinstance(value, list):
                #print(f'{key} returns a list. Further delving necessary.')
                self.json_nav.update({ key:{} })
                self.scan_list(value,key)
            
        self.depth -= 1

        
    def scan_fields(self, input_input):
        if len(input_input) == 0: return
        
        for key,value in input_input.items(): 
            if isinstance(value, list):
                print(f"{key}, {self.depth}. LIST")
                self.json_nav.update({ key:{} })
                self.root.update( { key:self.depth} )
                self.scan_list(value, key)
                
            elif isinstance(value, dict):
                print(f"{key}, {self.depth}. DICT")
                self.json_nav.update({key:{}})
                self.root.update( { key:self.depth} )
                self.scan_dict(value, key)

        #self.print_tree(self.json_nav)
        print('Done')
    
        
    def print_tree(self, input_dict):
        #print(f"!!!!!!validating!!!!!!\n {input_dict}")
        for key, value in input_dict.items():
            if key in self.root: 
                print(f"-{key}")
            else:
                loop_counter = value
                blank_space = ""
                while loop_counter > 0:
                    blank_space = blank_space + "   "
                    loop_counter = loop_counter - 1
                print(f'{blank_space}-{key}')
        
    def validate_series(self, input_list):
        for x in range(len(input_list)):
            if input_list[0].keys() != input_list[x].keys():
                return False
        return True
    
    def handle_invalid_series(self, input_list):
        print("Attempting to salvage dictionary entries.")
        most_keys = {}
        for item in range(len(input_list)):
            if input_list[item].keys() == most_keys.keys():
                return item
            if len(input_list[item].keys()) > len(most_keys.keys()):
                most_keys = input_list[item]
        return print("ERROR: Dictionaries Do Not Match")
            
        

        
    def is_nested(self, input_key):
        if input_key in self.json_nav.keys():
            #print(f'{input_key} is a dictionary key')
            return True
        return False
        
        
#IHateJson(r.json())
#for x in range(len(r.json()['roundResults'])):
 #   economy = r.json()['roundResults'][x]
  #          df = pd.Series(economy)
    #print(df)