#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 15:40:46 2020

@author: mep53
"""
import logging

class Logger():
    loglevel = logging.INFO
    @staticmethod
    def get_logger(logger_label):   
        l = logging.getLogger(logger_label)
        if not l.hasHandlers():
            l.setLevel(Logger.loglevel)
            h = logging.StreamHandler()
            fileHandler = logging.FileHandler(logger_label+'.log')
            f = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            h.setFormatter(f)
            fileHandler.setFormatter(f)
            l.addHandler(h)
            l.addHandler(fileHandler)
            l.setLevel(Logger.loglevel)
            l.handler_set = True
        return l
    
def main():
    Logger.get_logger("ABC").info('hey')
    

if __name__ == '__main__':
    main() 