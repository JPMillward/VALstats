#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pragma once
"""
@author: johnm

Py for making requests to the VALORANT API.
Running every 15 minutes using the folowing daemons
valapicall.service and valapicall.timer
"""
import sys
import logging
import asyncio
import httpx
import personal as env


async def log_request( request ):
    log.warning( f'Attempt: {request.method} {request.url}' )

async def log_response( response ):
    log.warning( f'Status: {response.status_code} {response.headers["x-app-rate-limit"]}, {response.headers["x-app-rate-limit-count"]} ')

async def request_limiter( request ):
    log.warning( f'Checking Request Limit' )
class ValorantFetcher():

    def __init__(self, api_end_point, search_parameter, headers ):
        log.info(f"Requesting {search_parameter} from {api_end_point}")
        self.search_param = search_parameter
        self.end_point = api_end_point
        self.headers = headers
        log.warning(self.headers, headers)
        return
    
    def validate_response(self, response_code):
        if response_code == 200: 
            return True
        else: 
            return False

    def standard_query(self, query):
        url = self.end_point + self.search_param + query
        my_headers = { env.api_header : env.match_key }
        log.warning(f'Attempting: {url}')

        with httpx.Client() as client:
            try:
                response = client.get( url, headers = my_headers )
                return response.json()
            except:
                log.warning('Unable to establish connection')


    async def attempt_query(self, query):
        url = self.end_point + self.search_param + query

        async with httpx.AsyncClient( event_hooks={ 'request' : [log_request], 'response' : [log_response] } ) as client:
            response = await client.get( url, headers = self.headers )
            return response.json()



async def main():
    log.warning('Main Called')
    my_headers = { env.api_header : env.match_key }
    log.warning(my_headers)
    request_recent_matches = ValorantFetcher( env.region_esports, env.match_by_queue, headers = my_headers )
    
    search = await request_recent_matches.attempt_query('tournamentmode')
    
    request_match = ValorantFetcher( env.region_esports, env.match_by_id, my_headers)
    tasks = [ asyncio.create_task( request_match.attempt_query( match ) ) for match in search['matchIds'] ]
    
    match_results = await asyncio.gather( *tasks )
    log.warning( f"Gathered {len( match_results )}" )
    return match_results
    

log = logging.getLogger(__name__)
if __name__ == '__main__':
    log.setLevel( 10 )
    log.warning(log.level, log.getEffectiveLevel)
    log.debug( sys.version_info )
    match_results = asyncio.run( main() )
