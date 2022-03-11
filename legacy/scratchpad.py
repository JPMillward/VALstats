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
            ensure constraints w?|2 "
            

"""
import pandas as pd
import requests
import personal as env
from millsql import sql
import sqlite3
import sys



#Reformat weird csv issue.
#csv = pd.read_csv(env.aggregation_queue)
#print(csv)
#csv.drop(columns='Unnamed: 0').to_csv(env.aggregation_queue, index=False)