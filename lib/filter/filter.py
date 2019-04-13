#!/usr/bin/env python

import os
import re
import shutil
import datetime
import multiprocessing
import configparser

import lib.menu as menu
import lib.settings as s
import lib.download as dld

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
        self.size_range = None
        self.markets = None
        self.date_min = None
        self.date_max = None
        self.virus_detect_rating_range = None
        if path != None:
            self.from_file(path)

    def match_size(self, size):
        if self.size_range != None:
            return (size in self.size_range)
        else:
            return True

    def match_date(self, date):
        if self.date_min != None and self.date_max != None:
            return date > self.date_min and date < self.date_max
        elif self.date_min != None:
            return date > self.date_min
        elif self.date_max != None:
            return date < self.date_max
        return True

    def match_virus_detect_rating(self, rating):
        if self.virus_detect_rating_range != None:
            return rating in self.virus_detect_rating_range
        return True

    def match_markets(self, markets):
        if self.markets != None:
            return markets.issubset(self.markets)
        return True

    # Returns whether csv line matches specified criteria
    def match_filters(self, line):
        try:
            sha256,sha1,md5,dex_date,apk_size,pkg_name,vercode,vt_detection,vt_scan_date,dex_size,markets=line.split(',')
            if sha256 == 'sha256' or len(dex_date) == 0:
                return False
            dex_date = datetime.datetime.strptime(dex_date.split(' ')[0], "%Y-%m-%d").date()
            if len(vt_detection) == 0:
                vt_detection = 5
            markets = set(markets.split('|'))
            return self.match_size(apk_size) \
            and self.match_date(dex_date) \
            and self.match_virus_detect_rating(vt_detection) \
            and self.match_markets(markets)
        except Exception as e:
            return False

    # Funtion to call to filter a list in parallel
    def parallel_filter(self, line, filtered_list):
        if self.match_filters(line):
            filtered_list.append(line)

    # Parallel landing function: Does the parallel work
    def parallel_host(self, filtered_list, data):
            for line in data:
                self.parallel_filter(line, filtered_list)

    # Chop csv in chunks for multiprocessing purposes.
    # Returns data in one chunk (standard 1 MB)
    def chunkify(self, file_name, size=1024*1024):
        with open(file_name,'r') as f:
            while True:
                data = f.readlines(size)
                if not data:
                    break
                yield data

    # Returns multiprocess-calculated list of apks
    def fire(self, path):
        print('Filtering... (this may take quite a while)')
        print('(And consume up to approximately '+str(os.path.getsize(path)>> 20)+' MB)')
        jobs = []
        filtered_list = multiprocessing.Manager().list()
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            for data in self.chunkify(path):
                jobs.append(pool.apply_async(self.parallel_host,(filtered_list,data,)))
            jobamount = len(jobs)
            jobs_done = 0
            print('Fired '+str(jobamount)+' jobs')
            for job in jobs:
                job.get()
                jobs_done+=1
                print('('+str(jobs_done)+'/'+str(jobamount)+') done')
        list_size = len(filtered_list)
        print('Found '+str(list_size)+' items matching criteria')
        return filtered_list, list_size



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
            if 'min' in config:
                self.date_min = datetime.datetime.strptime(config['date']['min'], "%Y-%m-%d").date()
            if 'max' in config:
                self.date_max = datetime.datetime.strptime(config['date']['max'], "%Y-%m-%d").date()
        if 'virusrating' in config \
            and 'min' in config['virusrating'] and 'max' in config['virusrating']:
            self.virus_detect_rating_range = \
            range(int(config['virusrating']['min']), int(config['virusrating']['max']))

    def to_file(self, path):
        config = configparser.ConfigParser()
        if self.markets != None:
            marketstring = ''
            for market in self.markets:
                marketstring+= (marketstring+'|')
            config['market'] = {'markets':marketstring[:-1]}
        if self.size_range != None:
            config['size'] = {'min':self.size_range.start, 'max': self.size_range.stop,}
        if self.date_min != None or self.date_max != None:
            config['date'] = {}
            if self.date_min != None:
                config['date']['min'] = str(self.date_min)
            if self.date_max != None:
                config['date']['max'] = str(self.date_max)
        if self.virus_detect_rating_range != None:
            config['virusrating'] = {'min':self.virus_detect_rating_range.start,
                                     'max':self.virus_detect_rating_range.stop}
        with open(path, 'w') as file:
            config.write(file)