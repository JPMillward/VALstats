#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jan 30, 2022
Created by: BrokenMaze

Used to calculate player economy breakdown (given available informatione)
Might End up falling severely short but we shall see
"""

import sqlite3
import personal as env

class ValEcon():

    def __init__(self):
        print("Initialized")
        self.retrieve_economy()
        return

    def retrieve_economy(self):
        
        sql = sqlite3.connect(env.database_path).cursor()
        print("open")
        return

ValEcon()

    