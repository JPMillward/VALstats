#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 15:16:17 2021

@author: johnm


"""
from os.path import exists as if_exists
import sys
import pandas as pd
from autohandler import ValAutoHandler
from valorantrequestfetcher import ValorantFetcher
from valmatchconverter import ValMatchConverter
import personal as env
import sqlite3

class ValStatsAggregator():
    
    def __init__(self, query, region = None):
        self.query = query
        self.region = region
        self.auto = ValAutoHandler()
        self.valid = True
        
        self.parse_region()
        self.parse_query()
        
        if self.valid == True:
            if self.query == 'auto': self.auto_handler()
            else: self.request_handler()
        return
    
    ### Currently overbuilt to take input requests it's never going to take. Then never implemented. Should be fine.
    def parse_query(self):
            #print(len(self.query))
            if len(self.query) == 36 or self.query == 'auto':
                self.api_end_point = env.match_by_id
                self.parse_out_file('match')
            elif len(self.query) == 78:
                self.api_end_point = env.match_by_player
                self.parse_out_file('player')
            elif self.query in ['competitive', 'unrated', 'spikerush', 'tournamentmode']:
                self.api_end_point = env.match_by_queue
                self.parse_out_file('recent')
            else:
                self.valid = False
                return print(f"Error: {self.query} is an invalid parameter")
            return print(f"Successfully found query endpoint.")
            
    def parse_region(self):            
            if self.region == 'na':
                self.api_region = env.region_na
            elif self.region == 'br':
                self.api_region = env.region_br
            elif self.region == 'eu':
                self.api_region = env.region_eu
            elif self.region == 'ap':
                self.api_region = env.region_ap
            elif self.region == 'kr':
                self.api_region = env.region_kr
            elif self.region == 'latam':
                self.api_region = env.region_latam
            elif self.region == 'esports':
                self.api_region = env.region_esports
            else:
                self.valid = False
                return print(f"Error: {self.region} does not exist.")
            return
    
    def parse_out_file(self, input_type):
            if input_type == 'match':
                self.out_location = env.database_path
            elif input_type == 'player':
                self.out_location = env.database_directory + 'player_matches_' + self.region + '.csv'
            elif input_type == 'recent':
                self.out_location = env.database_directory + 'recent_matches_' + self.region + '_' + self.query +'.csv'
            print(self.out_location)
            return
    
    def auto_handler(self):
        chunk = self.auto.get_chunk()
        for x in range(chunk.match_id.count()):
            self.region = chunk.iloc[x]['region']
            self.parse_region()
            search_paramater = chunk.iloc[x]['match_id']
            json = ValorantFetcher(self.api_end_point, self.api_region, search_paramater).attempt_query()
            ValMatchConverter(json, self.region, sqlite3.connect(self.out_location))
        
        
    def request_handler(self):
        json = ValorantFetcher(self.api_end_point, self.api_region, self.query).attempt_query()
        if not isinstance(json, dict): return json
        
        data_frame_list = []
        for match in json['matchIds']:
            data_frame_list.append( {'query_time': json['currentTime'], 'match_id' : match, 'region':self.region} )
        data_frame = pd.DataFrame(data_frame_list)
        print(data_frame.iloc[0]['query_time'])
        self.handle_output(data_frame)
        
        
        #This can be called an unlimited 
        
        
        return        

    def handle_output(self, data_frame):
        if not if_exists(self.out_location):
            print(f'No file found at {self.out_location} to validate. Creating new file')
            data_frame.to_csv(self.out_location, mode='w', index=False)
            return
        
        #everything other than esports has a recent match range of the past 10 minutes. Esports is 12hrs
        if self.region != 'esports':
            time_range = 600000
        else: 
            time_range = 43200000
            
        saved_list = pd.read_csv(self.out_location)
        print(saved_list['query_time'][0], saved_list['query_time'].iloc[-1])
        #print(f"Last query was {saved_list.iloc[-1]['query_time']}, current query time is {data_frame.iloc[0]['query_time']}")
        
        if saved_list.iloc[-1]['query_time'] > data_frame.iloc[0]['query_time'] - time_range :
            merged_data = saved_list.merge(data_frame, how='outer')
            removed_duplicates = merged_data.drop_duplicates(['match_id'])
            only_new = removed_duplicates.loc[removed_duplicates['query_time'] == data_frame.iloc[0]['query_time']]
            print(only_new)
            #remove_duplicates.to_csv(self.out_location, index = False)
            last_query = data_frame.iloc[0]['query_time'] - saved_list.iloc[-1]['query_time']
            print(f"Current Query Time: {data_frame.iloc[0]['query_time']}")
            print(f"Last Query Time: {saved_list.iloc[-1]['query_time']}")
            print(f"Warning: Query cache is {time_range}ms, but {last_query}ms has elapsed since last saved query.")
            
            print(f"Returned matches: {data_frame.match_id.count()}")
            print(f"Saved Matches: {saved_list.match_id.count()}")
            print(f"Total Matches: {merged_data.match_id.count()}")
            print(f"Unique Matches: {removed_duplicates.match_id.count()}")
            
            if (removed_duplicates.match_id.count() != saved_list.match_id.count()):
                ValAutoHandler().calculate_sample_size(only_new.drop(columns='query_time'), time_range)
                removed_duplicates.to_csv(self.out_location, mode= 'w', index=False)
                return print(f"Successfully saved {removed_duplicates.match_id.count() - saved_list.match_id.count()} {self.query} {self.region} matches.")
            else: return print(f"Found nothing new in query. Exiting.")
        
        else:
            data_frame.to_csv(self.out_location, mode='a', index=False)
            ValAutoHandler().calculate_sample_size(data_frame, time_range)
            
            return 
ValStatsAggregator('auto', 'esports')


