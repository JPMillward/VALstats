#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: johnm
Helper class for manipulating and querying SQL
"""

import pandas as pd
import sqlite3

class MillSql():
    
    def __init__(self, database_connection):
        self.dbc = database_connection
        self.enforce_relationship()
        self.generate_query_whitelist()
        return
   
    ### DB ENUMERATION
    def generate_query_whitelist(self):
        self.valid_queries = {}
        valid_tables = self.list_tables()
        for table in valid_tables:
            dictionary = {table:self.list_columns(table)}
            self.valid_queries.update(dictionary)
        #print(self.valid_queries)
            

    def list_tables(self):
        data_tables = []
        get_all = """SELECT name FROM sqlite_master WHERE type ='table'"""
        db_tables = pd.read_sql(get_all, self.dbc, index_col=None)
        for x in range(len(db_tables)):
            data_tables.append(db_tables.iloc[x][0])
        #print(self.data_tables)
        return data_tables
    
    def list_columns(self, table):
        table_columns = []
        get_columns = f"""PRAGMA table_info({table})"""
        column_names = pd.read_sql(get_columns, self.dbc)['name'].values
        #print(column_names)
        for item in column_names:     
            table_columns.append(item)
        return table_columns
    
    ### Enforce Database Relationships
    def enforce_relationship(self, enforce = True):
        foreign_keys = """PRAGMA foreign_keys"""
        
        if enforce == True: 
            enforce_key = """=true;"""
            pd.read_sql(foreign_keys + enforce_key, self.dbc)
        if enforce == False:
            enforce_key = """=false;"""
            pd.read_sql(foreign_keys + enforce_key, self.dbc)
        
        return #print(pd.read_sql(foreign_keys, self.dbc))
    
    ### CORE FUNCTION
            
    def search_db(self, table, column = None, match = None, return_column = None, index_column = None, discrete = False):
        if self.validate_input(table, column, match) != True: return print("Error: Invalid Query")
        print(f"Searching Database for {match}")
        show_table = """SELECT * FROM """ + table

        if  match == None or str(match) == 'None' or len(str(match)) == 0: param = None
        else:
            param = (match,)
            query1 = " WHERE "
            query2 = "=:match"
            show_table += query1 + column + query2

        ps_show_table = pd.read_sql(show_table, self.dbc,  params=param, index_col=index_column)
        if index_column == None: ps_show_table = ps_show_table.drop(columns='index')
        
        if len(ps_show_table) > 0: ret_table = ps_show_table.iloc[0] if discrete == True else ps_show_table
        else: ret_table = ps_show_table
        
        if  return_column == None: return ret_table
        else: return ret_table[return_column]
    
    ### INSERT ROWS INTO TABLE
    def insert_data(self, table, data_frame):
        if self.validate_input(table) == False: return print(f"Error: {table} does not exist.")
        data_frame.to_sql(table, self.dbc, if_exists='append')
        return(f"***added row to {table}***")
    
    
    def insert_table(self, table_name, data_frame):
        if self.validate_input(table_name): return print(f"Error: {table_name} exists. Please insert_data() instead")
        data_frame.to_sql(table_name, self.dbc)
        self.generate_query_whitelist()
        return print(f"***added {table_name} to sqlite_master***")
    
    
    ### VALIDATION FUNCTIONS
    def validate_input(self, table_name, column_name = None , insecure_string = None):
        valid_table = None
        valid_column = None
        valid_string = None
        
        if table_name not in self.valid_queries.keys(): 
           return False
        else: valid_table = True
        
        if column_name != None and column_name not in self.valid_queries[table_name]:
           valid_column = False
        if column_name in self.valid_queries[table_name]: 
           valid_column = True
        
        if insecure_string != None and ";" in insecure_string:
           valid_string = False
        elif insecure_string !=  None: valid_string = True
        
        #Return Logic
        valid_list = [valid_table, valid_column, valid_string]
        #print(valid_list)
        if False in valid_list: return False
        return True  
           
    ###SQLITE DATABASE FUNCTIONS
    def get_table(self, table):
        get_table = f"SELECT * FROM {table}"
        table_query = pd.read_sql(get_table, self.dbc)
        return table_query
    
    def rename_table(self, table_name, new_name):
        if not self.validate_input(table_name, insecure_string = new_name): return print(f"Error: No table with the name {table_name} exists.")
        alter_table = f"""ALTER TABLE {table_name} """
        rename_table = f"""RENAME to {new_name};"""
        pd.read_sql(alter_table + rename_table, self.dbc)
        self.generate_query_whitelist()
        return        
   
    def alter_table(self, table_name, change, column_name = None, data_type = None):
        #THIS FUNCTION IS A WORKAROUND TO LIMITED ALTER TABLE FUNCTIONALITY IN SQLITE
        change = change.upper()
        if change not in ['ADD', 'DROP', 'ALTER', 'RENAME']: return print(f"Error: {change} not valid")
        if change == 'DROP': 
            self.drop_column(table_name, column_name)
            return
        if change == 'RENAME' and column_name == None:
            self.rename_table(table_name, data_type)
            return
        
        print(f"column : {column_name}, {change}, {table_name}")
        alter_table = f"""ALTER TABLE {table_name} """
        alteration = f"""{change} COLUMN {column_name}"""
        if  change == 'RENAME': alteration += """ TO """
        alteration += f"""{data_type};""" if data_type != None else """;"""
        full_statement = alter_table + alteration
        print(full_statement)
        pd.read_sql(full_statement, self.dbc)
        return
        
    
    def drop_table(self, table):
        if not self.validate_input(table): return print("Error: Cannot drop {table} as it does not exist.")
        drop_table = f"""DROP TABLE {table};"""
        pd.read_sql(drop_table, self.dbc)
        self.generate_query_whitelist()
        return print(f"dropping {table} from database")
    
    def drop_column(self, table_name, column_name):
        if not self.validate_input(table_name, column_name): return print(f"Error: Invalid query. Cannot drop {column_name} from {table_name}")
        new_table = self.get_table(table_name).drop(columns=column_name)
        self.drop_table(table_name)
        self.insert_table(table_name, new_table)
        self.generate_query_whitelist()
        print(f"***Dropped {column_name} from {table_name}")
        return self.get_table(table_name)
    
    def does_exist(self, input_text, table = 'words', column = 'word'):
        check_exist = self.search_db(table = table, column = column, match = input_text, return_column = 'word', discrete = True)
        if str(check_exist) == input_text:
            print(f"{str(check_exist)} || {input_text}")
            return True  
        return False
    
#print(sql.valid_queries)
#print(sql.get_table('symbol_table'))