#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 18:26:31 2021

@author: johnm

Py for making requests to the VALORANT API
Need API key with access

SUN NOTES:
    To Do:
        -Check for unique matches and players in the table before appending.
        -- key constraints doing their job and that's good. But also bad.
        -Cruch a bunch of test cases and throw a ton of errors
        - Make fetcher fetch all the things. <- That's important
        -cry (again)
    
    
    economy tracking?    
    other questions?
    eventually refactor this monstrosity
"""
import requests
import pandas as pd
import personal as env


class ValMatchConverter():
    def __init__(self, json_response, region):
        self.region = region
        self.json = json_response
        
        self.valid = False
        if isinstance(self.json['roundResults'], list):
            self.valid=True
        self.match = self.json['matchInfo']['matchId']
        #Now assume match integrity based on the fact it got passed through successfully.
        
        self.matches = {}
        self.players = []
        self.match_stats = []
        self.rounds = []
        self.round_stats = []
        self.kill_logs = []
        self.bomb_logs = []
        self.match_logs = []
        self.damage_logs = []
        self.round_start_time = 0
    
  #  def run_conversion(self):
        ### Run Formatting Functions
        if self.valid == True:
            self.format_matches()
            self.format_players()
            self.format_match_stats()
            self.format_rounds()
        return
    
    def get_converted(self):
        if self.valid==False: return print("Error: Invalid Match File")
        
        master_dictionary = {'matches' : self.matches,
                             'players': self.players,
                             'match_stats': self.match_stats,
                             'rounds' : self.rounds,
                             'round_stats' : self.round_stats,
                             'kill_logs' : self.kill_logs,
                             'bomb_logs' : self.bomb_logs,
                             'match_logs' : self.match_logs,
                             'damage_logs' : self.damage_logs,
                            }
        return master_dictionary
          
   
    def format_matches(self):
        match_info = self.json['matchInfo']
        map_id = match_info['mapId']
        game_length = match_info['gameLengthMillis']
        start_time = match_info['gameStartMillis']
        prov_id = match_info['provisioningFlowId']
        game_name = match_info['customGameName']
        queue_id = match_info['queueId']
        season_id = match_info['seasonId']
        winner = None
        score = None
        self.matches= { 'match_id' : self.match,
                        'region' : self.region,
                        'map_id' : map_id,
                        'game_length_ms' : game_length,
                        'game_start_ms' : start_time,
                        'provision_id': prov_id,
                        'game_name' : game_name,
                        'queue_id' : queue_id,
                        'season_id' : season_id,
                        'winner' : winner,
                        'final_score' : score
            }
        #print(matches_row)
        return

    
    def format_players(self):
        players = self.json['players']
        #print(players)

        for x in range(len(players)):
            player = players[x]
            player_id = player['puuid']
            player_name = player['gameName']
            player_tag = player['tagLine']
            
            players_row = { 'player_id' : player_id,
                           'region' : self.region,
                           'game_name' : player_name,
                           'tag' : player_tag
                           }
            self.players.append(players_row)
        #print(pd.DataFrame(self.players))
        return
  
          
    def format_match_stats(self):
        players = self.json['players']
        #print(range(len(players)))
        for x in range(len(players)):
           
            player = players[x]
            player_id = player['puuid']
            team = player['teamId']
            party = player['partyId'].lower()
            
            stats = player['stats']
            if stats == None:
                print(f"Player: {player['gameName']}, Does not have stats. Omitting.")
            else:
                character = player['characterId']
                comp_tier = player['competitiveTier']
                player_card = player['playerCard'].lower()
                player_title = player['playerTitle'].lower()
                rounds_played = stats['roundsPlayed']
                play_time = stats['playtimeMillis']
                
                score = stats['score']
                kills = stats['kills']
                deaths = stats['deaths']
                assists = stats['assists']
                
                ability = stats['abilityCasts']
                if ability != None:
                    grenade_casts = ability['grenadeCasts']
                    ability_casts = ability['ability1Casts']
                    signature_casts = ability['ability2Casts']
                    ultimate_casts = ability['ultimateCasts']
                    
                else:
                    print(f"Error: {player['gameName']} has no ability use response. \nPlease verify match integrity.")
                    print(f"No logging for this. Build it if you see this message too many times.")
                    self.valid = False
                   
                    return
                
            
                match_stats_row = { 'match_id' : self.match,
                               'player_id' : player_id,
                               'team_id' : team, 
                                'party_id' : party,
                                'character_id' : character,
                                'competitive_tier' : comp_tier,
                                'player_card' : player_card,
                                'player_title' : player_title,
                                'rounds_played' : rounds_played,
                                'score' : score,
                                'kills' : kills,
                                'deaths' : deaths,
                                'assists' : assists,
                                'play_time_ms' : play_time,
                                'grenade_casts' : grenade_casts,
                                'ability_casts' : ability_casts,
                                'signature_casts' : signature_casts,
                                'ultimate_casts': ultimate_casts}
                self.match_stats.append(match_stats_row)
        return
            
    def format_rounds(self):
        round_results = self.json['roundResults']
        for x in range(len(round_results)):
            rounds = round_results[x]
            round_num = rounds['roundNum']
            round_result = rounds['roundResult']   
            round_ceremony = rounds['roundCeremony']
            winner = rounds['winningTeam']
            round_code = rounds['roundResultCode']
            
                
            self.format_round_stats(rounds)
            
            rounds_row = { 'match_id' : self.match,
                           'round' : round_num,
                           'round_start_ms' : self.round_start_time,
                           'round_result' : round_result,
                           'round_ceremony' : round_ceremony,
                           'winning_team' : winner,
                           'result_code' : round_code,
                            }
            self.rounds.append(rounds_row)
            
            
            if rounds['bombPlanter'] != None:
                self.format_bomb_logs(rounds,'plant')
            if rounds['bombDefuser'] != None:
                self.format_bomb_logs(rounds, 'defuse')
            if rounds['roundResult'] == 'Bomb detonated':
                self.format_bomb_logs(rounds, 'detonate')
        #print(pd.DataFrame(self.rounds))
    
    def format_round_stats(self, round_dict):
        round_num = round_dict['roundNum']
        for y in range(len(round_dict['playerStats'])):
            player = round_dict['playerStats'][y]
            player_id = player['puuid']
            kill_count = len(player['kills'])
            score = player['score']
            econ = player['economy']
            loadout_value = econ['loadoutValue']
            weapon = econ['weapon']
            armor = econ['armor']
            spent = econ['spent']
            remaining = econ['remaining']
            
                
            round_stats_row = { 'match_id' : self.match,
                                'round' : round_num,
                                'player_id' : player_id,
                                'score' : score,
                                'kills' : kill_count,
                                'loadout_value' : loadout_value,
                                'weapon' : weapon,
                                'armor' : armor,
                                'spent' : spent,
                                'remaining' : remaining }
            self.round_stats.append(round_stats_row)
            if len(player['damage']) > 0:
                self.format_damage_logs(round_num, player_id, player)
            
            if kill_count > 0:
                self.handle_kill_logging(player['kills'], round_num)
        return
                
    
    def handle_kill_logging(self, kill_list, round_number):
        round_start = 0
        for x in range(len(kill_list)):
            kill_num = kill_list[x]
            match_time = kill_num['timeSinceGameStartMillis']
            round_time = kill_num['timeSinceRoundStartMillis']
            
            #Verify Log Integrity, Find round start
            if round_start == 0: round_start = match_time - round_time
            elif round_start != match_time - round_time:
                print(f"ERROR: {round_start} is not {match_time - round_time} = {match_time} - {round_time}")
            
            target_id = kill_num['victim']
            target_loc = str(kill_num['victimLocation']['x']) + ',' + str(kill_num['victimLocation']['y'])
            kill_info = kill_num['finishingDamage']
                        
            player_id = kill_num['killer']
            self.format_kill_logs(round_number = round_number, player_id=player_id, target_id=target_id, kill_info = kill_info, match_time=match_time, round_time=round_time)
            
            #Log player location and match time with event.
            for player in range(len(kill_num['playerLocations'])):
                listed_player = kill_num['playerLocations'][player]
                view = listed_player['viewRadians']
                location = str(listed_player['location']['x']) + ',' + str(listed_player['location']['x'])
                
                if listed_player['puuid'] == player_id:
                    event = 'kill'
                else: event = 'assist'
                
           
                
                self.format_match_logs(round_number=round_number, player=listed_player['puuid'], event_id=event, player_location=location, view=view, target_id=target_id, target_loc=target_loc, match_time=match_time, round_time=round_time)
            self.round_start_time = round_start
        return
                
    def format_kill_logs(self, round_number, player_id, target_id, kill_info, match_time, round_time):
        kill_logs_row = { 'match_id': self.match,
                         'round' : round_number,
                         'match_time_ms': match_time,
                         'round_time_ms': round_time, 
                         'player_id': player_id,
                         'target_id': target_id,
                         'damage_type': kill_info['damageType'],
                         'damage_item': kill_info['damageItem'],
                         'alt_fire': kill_info['isSecondaryFireMode']}
        self.kill_logs.append(kill_logs_row)
        return         
                        
        
    def format_match_logs(self, round_number, player, event_id, player_location, view, target_id, target_loc, match_time, round_time):

        match_logs_row = { 'match_id' : self.match,
                           'player_id' : player,
                           'match_time_ms' : match_time,
                           'round' : round_number,
                           'round_time_ms' : round_time,
                           'event' : event_id,
                           'player_location' : player_location,
                           'view' : view,
                           'target_id' : target_id,
                           'target_location' : target_loc}
        self.match_logs.append(match_logs_row)
        return
                           

    
    def format_bomb_logs(self, round_number, bomb_event):
        match_id = self.json['matchInfo']['matchId']
        bomb_site = round_number['plantSite']
        
        if bomb_event == 'detonate':
            bomb_location = str(round_number['plantLocation']['x']) + ',' + str(round_number['plantLocation']['y'])
            round_time = round_number['plantRoundTime']+45000 #Bomb Timer is 45 Seconds
        else:
            round_time = round_number[bomb_event+'RoundTime']
            bomb_location = str(round_number[bomb_event+'Location']['x']) + ',' + str(round_number[bomb_event+'Location']['y'])
        
        match_time = self.round_start_time + round_time
        
        bomb_logs_row = {'match_id' : match_id,
                         'match_time_ms' : match_time,
                         'round' : round_number['roundNum'],
                         'round_time_ms' : round_time,
                         'event' : bomb_event,
                         'location' : bomb_location,
                         'bomb_site' : bomb_site}
        self.bomb_logs.append(bomb_logs_row)
        self.handle_bomb_event(round_number, bomb_event, round_time)
        return
        
    
    def handle_bomb_event(self, round_info, bomb_event, round_time):
        spike_id = "0afb2636-4093-c63b-4ef1-1e97966e2a3e"
        round_num = round_info['roundNum']
        match_time = self.round_start_time + round_time
        
        if bomb_event == 'plant': interacting_player = 'bombPlanter'
        elif bomb_event == 'defuse': interacting_player = 'bombDefuser'
        
        
        if (bomb_event == 'plant' or bomb_event == 'defuse'):
            
            for player in range(len(round_info[bomb_event+'PlayerLocations'])):
                listed = round_info[bomb_event+'PlayerLocations'][player]
                player_id = listed['puuid']
                player_location = str(listed['location']['x']) + ',' + str(listed['location']['y'])
                view = listed['viewRadians']           
                bomb_location = str(round_info[bomb_event+'Location']['x']) + ',' + str(round_info[bomb_event+'Location']['y'])
                
                if player_id == round_info[interacting_player]:
                    self.format_match_logs(round_num, player_id, bomb_event, player_location, view, spike_id, bomb_location, match_time, round_time)
                else:
                    self.format_match_logs(round_num, player_id, 'ping', player_location, view, spike_id, bomb_location, match_time, round_time)
        
        elif (bomb_event == 'detonate'):
            bomb_location = str(round_info['plantLocation']['x']) + ',' + str(round_info['plantLocation']['y'])
            self.format_match_logs(round_num, round_info['bombPlanter'], bomb_event, bomb_location, None, spike_id, bomb_location, match_time, round_time)
    
                        
    def format_damage_logs(self, round_number, player, player_info):
        round_table = []
        for item in range(len(player_info['damage'])):
            damage_summary = player_info['damage'][item]
            damage_logs_row = {'match_id' : self.match,
                               'round_id' : round_number,
                               'player_id' : player,
                               'target_id' : damage_summary['receiver'],
                               'damage' : damage_summary['damage'],
                               'head_hits' : damage_summary['headshots'],
                               'body_hits' : damage_summary['bodyshots'],
                               'leg_hits' : damage_summary['legshots'],
                               }
            #print(damage_logs_row)
            round_table.append(damage_logs_row)
        self.validate_damage_logs(round_table)
        return
    
    def validate_damage_logs(self, round_table):
        target_map = {}
        duplicates = []
        
        for x in range(len(round_table)):
            this_row = round_table[x]
            target = round_table[x]['target_id']
            
            if target in target_map:
                same_target = round_table[target_map[target]]
                #print(same_target)
                updated_damage_row = {'match_id': self.match,
                                  'round_id': same_target['round_id'],
                                  'player_id': same_target['player_id'],
                                  'target_id': same_target['target_id'],
                                  'damage': same_target['damage'] + this_row['damage'],
                                  'head_hits': same_target['head_hits'] + this_row['head_hits'],
                                  'body_hits': same_target['body_hits'] + this_row['body_hits'],
                                  'leg_hits': same_target['leg_hits'] + this_row['body_hits'],
                                }
                #print(f"Updated Entry: {updated_damage_row}")
                round_table[target_map[target]].update(updated_damage_row)
                duplicates.append(x)
            else: target_map.update({target : x})

        #if len(duplicates) >= 1: print(duplicates)
        
        #print(pd.DataFrame(round_table))
        for duplicate in range(len(duplicates)):
            round_table.pop(duplicates[duplicate]-duplicate)
        
        #print(pd.DataFrame(round_table))
        for row in round_table:
            self.damage_logs.append(row)
        return
    