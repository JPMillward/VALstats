#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 18:26:31 2021

@author: johnm

Py for making requests to the VALORANT API
Need API key with access

THU NOTES:
    To do - finish constraint enforcement for database.
            craft class for reading data into said database.
            read in economy tables, constants table.
            ensure constraints work.
            begin automation of match data aggregation and storage.
            pray.
            

"""
from pandas.io.json import json_normalize
import pandas as pd
import requests
import personal as env
import constants as c
import sqlite3

path = "/Users/johnm/Documents/learning mats/"
file = "equipment_econ.xlsx"
df = pd.read_excel(path + file)
#print(df)


search_param = '273a40d0-d087-423e-81b5-7c234895e9e5'
r = requests.get( env.match_by_id + search_param, headers = { env.api_header : env.match_key })
json = r.json()

round_result = json['roundResults'][0]
stats = round_result['playerStats'][1]
damage = stats['damage']
kills = stats['kills']

print(round_result.keys())
print(stats.keys())
print(damage[0].keys())
print(len(kills))

for x in range(len(json['roundResults'])):
    round_num = json['roundResults'][x]
    print(f"---Round {x}---")
    print(f"{round_num['roundResult']}, {round_num['roundCeremony']}, {round_num['winningTeam']}")
    print(f"Planter: {round_num['bombPlanter']}, Defuser: {round_num['bombDefuser']}")
    print(f"{round_num['plantLocation']}, {round_num['defuseLocation']}")
    print(f"{round_num['plantRoundTime']}, {round_num['defuseRoundTime']}")
    print(round_num['defusePlayerLocations'])
    for y in range(len(round_num['playerStats'])):
        #print(f"------Player {y}-----")
        player = round_num['playerStats'][y]
        damage = player['damage']
        kills = player['kills']
        economy = player['economy']
        score = player['score']
        ability = player ['ability']
        #print(f"kills: {len(kills)}")
        #print(kills)
        print(damage)

print (json['roundResults'][0].keys())
print(json['roundResults'][0]['roundResultCode'])
'''
print(r.json()['teams'])    
for x in range(len(r.json()['players'])):
    player = r.json()['players'][x]
    agent = c.agent_name[r.json()['players'][x]['characterId']]
    rank = c.player_rank[player['competitiveTier']]
    team = player['teamId']
    print(f"{agent}, {rank}, {team}")
    print(player['stats']['abilityCasts'])

print(r.json()['roundResults'][0].keys())
for x in range(len(r.json()['roundResults'])):
    result = r.json()['roundResults'][x]
    print(f"---Round {result['roundNum']}, {result['winningTeam']} wins by {result['roundResultCode']}---")
    
    for y in range(len(result['playerStats'])):
        player = result['playerStats'][y]
        pid = c.agent_name[r.json()['players'][y]['characterId']]
        team = r.json()['players'][y]['teamId']
        if len(player['economy']['weapon']) > 0:
            weapon = c.equipment_name[player['economy']['weapon'].lower()]
        else: weapon = "None"
        if len(player['economy']['armor']) > 0:
            armor = c.equipment_name[player['economy']['armor']]
        else: armor = "None"
        spent = player['economy']['spent']
        left = player['economy']['remaining']
        print(f'Player: {team} {pid} | Weapon: {weapon} | Armor: {armor} | Spent: {spent} | Left: {left}')

'''
'''
match_id = json['matchInfo']['matchId']
map_id = c.map_id[json['matchInfo']['mapId']]
queue_id = json['matchInfo']['queueId']
match_length_ms = json['matchInfo']['gameLengthMillis']
match_time_ms = json['matchInfo']['gameStartMillis']

print(json['matchInfo'].keys())
#json['matchInfo']['']
ranked = json['matchInfo']['isRanked']
season = json['matchInfo']['seasonId']
print(f"{match_time_ms}, {match_id}, {map_id}, {queue_id}, {ranked}, \n {season}, Match Length: {match_length_ms}")
'''
