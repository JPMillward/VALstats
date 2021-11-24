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
import sys
import pandas as pd
import requests
import io
import personal as env
import constants as c

search_param = 'competitive'
r = requests.get( env.match_by_queue + search_param, headers = { env.api_header : env.match_key })
json = r.json()

print(sys.version)