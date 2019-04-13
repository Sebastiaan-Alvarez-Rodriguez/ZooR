#!/usr/bin/env python
import sys
import os
import multiprocessing
import numpy

import lib.csv.csv as csv

class Picker(object):
    """Object which pickes items from given CSV"""
    def __init__(self, CSV):
        self.CSV = CSV
        self.list_size = self.CSV.list_size

    # Ask user for size of sample
    def ask_samplesize(self):
        while True:
            print('How large do you want your sample (max '+str(self.list_size)+')?')
            choice = input('')
            if len(choice) == 0 or not choice.isdigit():
                print('Please provide a number')
            elif int(choice) > self.list_size:
                print('Specify a number less than '+str(self.list_size))
            else:
                return int(choice)

    # Pick items at random out of the list
    def pick(self, samplesize):
        return numpy.random.choice(self.CSV.filtered_list, samplesize, replace=False)