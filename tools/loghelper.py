#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 09:18:55 2022

@author: johnm
"""
import logging
import sys

class LoggerHelper:
    
    def __init__( self ):
        self.name = None
        self.folder = None
        self.logger = None
        return
    
    def log_program( self, application_name = __name__, file_folder = None, format_type = 'default', ow = False ):
        self.logger = logging.getLogger( application_name )
        self.logger.setLevel(10)
        self.logger.propogate = True
        logging_format = self.get_format( format_type )
        
        self.instantiate_stream_handler( self.logger, log_format = logging_format)
        
        if file_folder:
            self.instantiate_file_handlers( self.logger, file_folder, log_format = logging_format )
            
        
        return self.logger
    
    
    def check_instance( self, handler_type):       
        self.logger.debug(f'checking {len(self.logger.handlers)} handlers for {handler_type}')
        for handler in self.logger.handlers:
            self.logger.debug(f'current handler: {handler}')
            
            if isinstance(handler, type(handler_type)):
                self.logger.debug(f'Found a handler of {type(handler_type)}')
                return True
        self.logger.debug(f"No handler matching {handler_type}")
        return False
    
    
    def instantiate_stream_handler( self, logger, log_format = 'default', log_level = 'DEBUG' ):
        
        stream_out = logging.StreamHandler( sys.stdout )
        stream_out.setLevel( log_level )
        stream_out.propogate = False
        logger.debug( f'checking for a stream handler using log_level {log_level}' )
        
        if log_format:
            stream_out.setFormatter( log_format )
        
        if not self.check_instance( stream_out ):
            logger.info(f'No Stream Handler, adding console debug for {__name__}')
            logger.addHandler( stream_out )
        return 
    
    
    def instantiate_file_handlers( self, logger, file_folder, log_format = None):
        for log_level in [ 'INFO', 'WARNING', 'ERROR', 'CRITICAL' ]:
            
            new_file_handler = logging.FileHander( file_folder + log_level, 'a' )
            new_file_handler.setLevel( log_level )
            
            if log_format:
                new_file_handler.setFormatter( log_format )
            
            if new_file_handler not in logger.handlers:
                logger.addHandler( new_file_handler )
        return
    
    
    def get_format( self, format_type = 'default' ):
        logging.debug(f'Using {format_type} settings.')
        if format_type == 'minimal':
            log_formatter = logging.Formatter( '%(asctime)s - %(levelname)s - %(message)s' )
        else:
            log_formatter = logging.Formatter( '%(asctime)s - %(levelname)s - %(message)s')

        return log_formatter
    
        

def main():
    logger = LoggerHelper().log_program(__name__)
    logger.warning('Finished call')

    
    for logger in logger.handlers:
        print(logger)
    logger.handlers.clear()


if __name__ == '__main__':
    main()
else:
    logging.warning(f'Called by {__name__}')