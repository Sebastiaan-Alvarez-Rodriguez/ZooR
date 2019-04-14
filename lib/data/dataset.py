#!/usr/bin/env python

import lib.filter.filterperformer as filterperformer

class Dataset(object):
    def __init__(self, csv=None, in_filter=None):
        self.csv = csv
        self.in_filter = in_filter
        self.filter_performer = filterperformer.Filterperformer(in_filter)
        self.length = 0

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
            
        
# class Dataset(object):
#     def __init__(self, data):
#         self.data = set(data) if data != None else set([])

#     def add(self, elem):
#         self.data.append(elem)

#     def contains(self, subset):
#         return set(subset.apks).issubset(self.data)

#     def is_empty(self):
#         return len(self.data) == 0

#     def __hash__(self):
#         return hash(frozenset(self.data))

#     def __len__(self):
#         return len(self.data)

#     def __iter__(self):
#         return iter(self.data)