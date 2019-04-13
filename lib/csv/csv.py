#!/usr/bin/env python

import lib.csv.csvhandler as csvhandler
import lib.filter.filterhandler as filterhandler

class CSV(object):
    """Object representing CSV object, with built-in filter options"""

    # Constructor, requires path to csv file
    def __init__(self):
        self.path = csvhandler.get_csv()
        self.filter = filterhandler.get_filter()
        self.filtered_list, self.list_size = self.filter.fire(self.path)