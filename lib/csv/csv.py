#!/usr/bin/env python

import lib.csv.csvhandler as csvhandler
import lib.data.element as element
class CSV(object):
    """Object representing CSV object, with built-in file iterator"""

    # Constructor, requires path to csv file
    def __init__(self):
        self.path = csvhandler.get_csv()
        self.file = open(self.path, 'r')
        next(self.file)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            line = next(self.file)
            sha256,sha1,md5,dex_date,apk_size,pkg_name,vercode,vt_detection,vt_scan_date,dex_size,markets = line.strip('\n').replace('"', '').split(',')
            return element.Element(sha256,sha1,md5,dex_date,apk_size,pkg_name,vercode,vt_detection,vt_scan_date,dex_size,markets)
        except Exception as e:
            self.file.close()
            raise e