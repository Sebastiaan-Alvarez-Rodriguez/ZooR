#!/usr/bin/env python

import lib.filter.filterperformer as filterperformer

class Dataset(object):
    def __init__(self, csv, in_filter):
        self.csv = csv
        self.in_filter = in_filter
        self.filter_performer = filterperformer.Filterperformer(self.in_filter)
        self.length = 0

        print('Filter received:')
        print('size_min: {0}'.format(in_filter.size_min))
        print('size_max: {0}'.format(in_filter.size_max))
        print('markets: {0}'.format(in_filter.markets))
        print('date_min: {0}'.format(in_filter.date_min))
        print('date_max: {0}'.format(in_filter.date_max))
        print('virus_detect_min: {0}'.format(in_filter.virus_detect_min))
        print('virus_detect_max: {0}'.format(in_filter.virus_detect_max))

    def __iter__(self):
        return self

    def __next__(self):
        try:
            element = next(self.csv)
            while not self.filter_performer.match_filters(element):
                element = next(self.csv)
            self.length += 1
            return element
        except StopIteration:
            print('Iterated over {0} items'.format(str(self.length)))
            raise StopIteration

    def __hash__(self):
        return hash(self.csv)+hash(self.in_filter)
