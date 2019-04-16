#!/usr/bin/env python

import os
import datetime
import configparser

class Filter(object):
    # Filtering possible on
    # sha256,sha1,md5,dex_date,apk_size,
    # pkg_name,vercode, (version code of apk)
    # vt_detection,vt_scan_date, (virus detection rating and scan date)
    # dex_size,markets

    # Markets kan be any of:
    # 1mobile,angeeks,anzhi,apk_bang,appchina,fdroid,
    # freewarelovers,genome,hiapk,markets,mi.com,
    # play.google.com,proandroid,slideme,torrents.

    def __init__(self, path=None):
        self.size_min = None
        self.size_max = None
        self.markets = None
        self.date_min = None
        self.date_max = None
        self.virus_detect_min = None
        self.virus_detect_max = None
        if path != None:
            self.from_file(path)

    def from_file(self, path):
        if not os.path.isfile(path):
            raise RuntimeError('Error: no such file - "'+path+'"')
        config = configparser.ConfigParser()
        config.read(path)
        if 'market' in config and 'markets' in config['market']:
                self.markets = set(config['market']['markets'].split('|'))
        if 'size' in config and 'min' in config['size'] and 'max' in config['size']:
                self.size_range = range(int(config['size']['min']), int(config['size']['max']))
        if 'date' in config:
            if 'min' in config['date']:
                self.date_min = datetime.datetime.strptime(config['date']['min'], "%Y-%m-%d").date()
            if 'max' in config['date']:
                self.date_max = datetime.datetime.strptime(config['date']['max'], "%Y-%m-%d").date()
        if 'virusrating' in config:
            if 'min' in config['virusrating']:
                self.virus_detect_min = int(config['virusrating']['min'])
            if 'max' in config['virusrating']:
                self.virus_detect_max = int(config['virusrating']['max'])

    def to_file(self, path):
        config = configparser.ConfigParser()
        if self.markets != None:
            marketstring = ''
            for market in self.markets:
                marketstring+= (marketstring+'|')
            config['market'] = {'markets':marketstring[:-1]}
        if self.size_min != None or self.size_max != None:
            config['size'] = {}
            if self.size_min != None:
                config['size']['min'] = str(self.size_min)
            if self.size_max != None:
                config['size']['max'] = str(self.size_max)
        if self.date_min != None or self.date_max != None:
            config['date'] = {}
            if self.date_min != None:
                config['date']['min'] = str(self.date_min)
            if self.date_max != None:
                config['date']['max'] = str(self.date_max)
        if self.virus_detect_min != None or self.virus_detect_max != None:
            config['virusrating'] = {}
            if self.virus_detect_min != None:
                config['virusrating']['min'] = str(self.virus_detect_min)
            if self.virus_detect_max != None:
                config['virusrating']['max'] = str(self.virus_detect_max)
        
        with open(path, 'w') as file:
            config.write(file)

    def __hash__(self):
        return hash(str(self.size_min)+str(self.size_max)\
            +str(self.markets)+str(self.date_min)\
            +str(self.date_max)+str(self.virus_detect_min)\
            +str(self.virus_detect_max))