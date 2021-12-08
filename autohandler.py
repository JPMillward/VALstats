#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 10:39:49 2021

@author: johnm
"""
from os.path import exists as if_exists
import personal as env
import pandas as pd

class ValAutoHandler():
    
    def __init__(self, target = env.aggregation_queue):
        self.limit = env.rate_limit
        self.target = target
        self.get_matches()
        return
    
    def get_matches(self):
        match_list = pd.read_csv(self.target, sep=',')
        #print(len(match_list))
        self.match_list = match_list
        return self.match_list
    
    def get_chunk(self):
        chunk = self.match_list[:self.limit]
        return chunk
        
        
        
    
    def calculate_sample_size(self, unique_entries, time_range, overlap = 0):
        print("Do math to determine how many to add based on time elapse from last queue.")
        
        if time_range > 3600000:
            self.add_entries(unique_entries, priority = True)
            return
        if overlap != 0:
            return print("Currently unable to validate data")
        
        entry_count = unique_entries.match_id.count()
        time_min = int(time_range * .001 / 60)
        max_sample_size = (time_min * self.limit)
        print(max_sample_size)
        
        if entry_count < max_sample_size:
            self.add_entries(unique_entries)
            return
        self.add_entries(unique_entries[-max_sample_size:])
        return 
        
            
    
    def add_entries(self, unique_entries, priority = False):
        if not if_exists(self.target):
            unique_entries.to_csv(self.target, index=False)
            return print("For some reason, no queue was found. Created new one.")
        
        queue_file = pd.read_csv(self.target)
        
        #Basically if it's an esport match
        if priority == True:
            
            new_file = unique_entries.append(queue_file)
            new_file.to_csv(self.target, index=False)
        else:
            new_file = queue_file.append(unique_entries)
            new_file.to_csv(self.target, index=False)
    
    def delete_entries(self):
        self.match_list = self.match_list[self.limit:]        
        self.match_list.to_csv(self.target)
        return