#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 22:07:40 2021

@author: johnm

sql statements for crafting the database. Saving here for posterity
Also I'm tired of typing them line by line into console.


"""

import sqlite3
import personal as env
from millsql import MillSql
import pandas as pd

constants = """CREATE TABLE constants (
                unique_id TEXT NOT NULL,
                plain_text TEXT NOT NULL,
                PRIMARY KEY (unique_id));"""

#Master table for refering to match info
matches = """CREATE TABLE matches (
          match_id TEXT NOT NULL,
          region TEXT NOT NULL,
          map_id TEXT NOT NULL,
          game_length_ms INT NOT NULL,
          game_start_ms INT NOT NULL,
          provision_id TEXT NOT NULL,
          game_name TEXT,
          queue_id TEXT,
          season_id TEXT,
          winner TEXT,
          final_score TEXT,
          
          PRIMARY KEY(match_id)
        );"""

#Master table for player info
players = """CREATE TABLE players (
            player_id TEXT NOT NULL,
            region TEXT NOT NULL,
            game_name TEXT NOT NULL,
            tag TEXT NOT NULL,
            
            PRIMARY KEY (player_id)
                
            );"""

#Breakdown of stats by match by player
match_stats = """CREATE TABLE match_stats (
                match_id TEXT NOT NULL,
                player_id TEXT NOT NULL,
                team_id TEXT NOT NULL,
                party_id TEXT NOT NULL,
                character_id TEXT NOT NULL,
                competitive_tier INT NOT NULL,
                player_card TEXT NOT NULL,
                player_title TEXT NOT NULL,
                rounds_played INT NOT NULL,
                score INT NOT NULL,
                kills INT NOT NULL,
                deaths INT NOT NULL,
                assists INT NOT NULL,
                play_time_ms INT NOT NULL,
                grenade_casts INT NOT NULL,
                ability_casts INT NOT NULL,
                signature_casts INT NOT NULL,
                ultimate_casts INT NOT NULL,
                FOREIGN KEY (character_id) REFERENCES constants(unique_id)
                FOREIGN KEY(match_id) REFERENCES matches(match_id),
                FOREIGN KEY(player_id) REFERENCES players(player_id),
                PRIMARY KEY(match_id, player_id)
                
                
                   );"""

# Breakdown of each round in a match
rounds = """CREATE TABLE rounds (
            match_id TEXT NOT NULL,
            round INT NOT NULL,
            round_start_ms INT NOT NULL,
            round_result TEXT,
            round_ceremony TEXT,
            winning_team TEXT,
            result_code TEXT,
            FOREIGN KEY (match_id) REFERENCES matches(match_id),
            PRIMARY KEY (match_id, round)
            );"""

#Breakdown of players by round by match
round_stats = """CREATE TABLE round_stats (
                match_id TEXT NOT NULL,
                round INT NOT NULL,
                player_id TEXT NOT NULL,
                score INT NOT NULL,
                kills INT NOT NULL,
                loadout_value INT NOT NULL,
                weapon TEXT NOT NULL,
                armor TEXT NOT NULL,
                spent INT NOT NULL,
                remaining INT NOT NULL,
                
                FOREIGN KEY(match_id, round) REFERENCES rounds(match_id, round),
                FOREIGN KEY(player_id) REFERENCES players(player_id)
                PRIMARY KEY (match_id, player_id, round)
                
                );"""

#Event log organized in long format to make queries by time.
match_logs = """CREATE TABLE match_logs(
            match_id TEXT NOT NULL,
            round INT NOT NULL,
            player_id TEXT NOT NULL,
            match_time_ms INT NOT NULL,
            round_time_ms INT NOT NULL,
            event TEXT NOT NULL,
            player_location BLOB NOT NULL,
            view REAL,
            target_id TEXT NOT NULL,
            target_location BLOB NOT NULL,
            FOREIGN KEY(match_id, round) REFERENCES rounds(match_id, round),
            FOREIGN KEY (player_id) REFERENCES players(player_id),
            PRIMARY KEY (match_id, player_id, match_time_ms, target_id)
);"""

#Track damage by match, round, player, target
damage_logs = """CREATE TABLE damage_logs (
                match_id TEXT NOT NULL,
                round_id INT NOT NULL,
                player_id TEXT NOT NULL,
                target_id TEXT NOT NULL,
                damage INT NOT NULL,
                head_hits INT,
                body_hits INT,
                leg_hits INT,
                FOREIGN KEY (match_id, round_id) REFERENCES rounds(match_id, round)
                FOREIGN KEY (player_id) REFERENCES players(player_id)
                FOREIGN KEY (target_id) REFERENCES players(player_id)
                PRIMARY KEY(match_id, round_id, player_id, target_id)
                );"""

kill_logs = """CREATE TABLE kill_logs (
                match_id TEXT NOT NULL,
                round TEXT NOT NULL,
                match_time_ms INT NOT NULL,
                round_time_ms INT NOT NULL,
                player_id TEXT NOT NULL,
                target_id TEXT NOT NULL,
                damage_type TEXT,
                damage_item TEXT NOT NULL,
                alt_fire TEXT,
                FOREIGN KEY (match_id, round) REFERENCES rounds(match_id, round)
                FOREIGN KEY (player_id) REFERENCES players(player_id)
                FOREIGN KEY (target_id) REFERENCES players(player_id)
                PRIMARY KEY (match_id, match_time_ms, player_id, target_id)
                );"""

#Table for tracking bomb-specific data
bomb_logs = """CREATE TABLE bomb_logs (
                match_id TEXT NOT NULL,
                round INT NOT NULL,
                match_time_ms INT NOT NULL,
                round_time_ms INT NOT NULL,
                event TEXT NOT NULL,
                location BLOB NOT NULL,
                bomb_site TEXT NOT NULL,
                FOREIGN KEY (match_id, round) REFERENCES rounds(match_id, round)
                PRIMARY KEY (match_id, match_time_ms)
                );"""



equipment_econ = """CREATE TABLE equipment_econ (
                    equipment_id TEXT NOT NULL,
                    equipment_name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    cost INT NOT NULL,
                    FOREIGN KEY (equipment_id) REFERENCES constants(unique_id),
                    PRIMARY KEY (equipment_id)
                    );"""

agent_econ = """CREATE TABLE agent_econ (
                agent_id TEXT NOT NULL, 
                agent_name TEXT NOT NULL,
                grenade_cost INT NOT NULL,
                grenade_max INT NOT NULL,
                ability_cost INT NOT NULL,
                ability_max INT NOT NULL,
                signature_cost INT NOT NULL,
                signature_max INT NOT NULL,
                ultimate_point_cost INT NOT NULL,
                FOREIGN KEY (agent_id) REFERENCES constants(unique_id),
                PRIMARY KEY (agent_id)
                );"""


sql = MillSql(sqlite3.connect(env.database_path))
###Delete after table is working properly.
def reset_tables():
    sql.enforce_relationship(False)
    drop = """DROP TABLE """
    drop_list= ['matches', 'players', 'match_stats', 'rounds', 'round_stats', 'match_logs', 'damage_logs', 'bomb_logs', 'kill_logs']
    for key in drop_list:
        pd.read_sql(drop+key+";", sql.dbc)
    return    

def add_tables():
    sql.enforce_relationship(True)
    table_list = [matches, players, match_stats, rounds, round_stats, match_logs, damage_logs, bomb_logs, kill_logs]
    
    for query in table_list:
        pd.read_sql(query, sql.dbc)
    return


reset_tables()
add_tables()


