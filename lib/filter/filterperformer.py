#!/usr/bin/env python

import datetime
import multiprocessing

class Filterperformer(object):
    """Object to handle filtering, given a filter"""

    def __init__(self, in_filter):
        self.filter = in_filter
    
    @staticmethod
    def match_size(size, in_filter):
        ok = True
        if in_filter.size_min != None:
            if size == None:
                return False
            ok = size >= in_filter.size_min
        if ok and in_filter.size_max != None:
            if size == None:
                return False
            ok = size <= in_filter.size_max
        return ok

    @staticmethod
    def match_date(date, in_filter):
        ok = True
        if date == None or len(date) == 0:
            return in_filter.date_min == None and in_filter.date_max == None

        if in_filter.date_min != None or in_filter.date_max != None:
            c_date = datetime.datetime.strptime(date.split(' ')[0], "%Y-%m-%d").date()

        if in_filter.date_min != None:
            ok = c_date >= in_filter.date_min
        if ok and in_filter.date_max != None:
            ok = c_date <= in_filter.date_max
        return ok

    @staticmethod
    def match_virus_detect_rating(rating, scanned, in_filter):
        ok = True
        if rating == None and (in_filter.virus_detect_min != None or in_filter.virus_detect_max):
            return False

        if in_filter.virus_detect_min != None:
            ok = (rating >= in_filter.virus_detect_min) and scanned
        if ok and in_filter.virus_detect_max != None:
            ok = (rating <= in_filter.virus_detect_max) and scanned
        return ok

    @staticmethod
    def match_markets(markets, in_filter):
        if in_filter.markets != None:
            if markets == None:
                return False
            return markets.issubset(in_filter.markets)
        return True

    # Returns whether csv line matches specified criteria
    def match_filters(self, element):
        return self.match_size(element.apk_size, self.filter) \
            and self.match_virus_detect_rating(element.vt_detection, element.vt_scan_date != '' and element.vt_scan_date != None, self.filter) \
            and self.match_date(element.dex_date, self.filter) \
            and self.match_markets(element.markets, self.filter)

    def filter_dataset(self, dataset):
        print('Start filtering')
        dataset.data = filter(self.match_filters, dataset.data)
