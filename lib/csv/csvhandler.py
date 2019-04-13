#!/usr/bin/env python
import os
import re
import shutil
import datetime

import lib.menu as menu
import lib.settings as s
import lib.download as dld

# Returns list of all csv paths in csvdir
def get_available_csvs():
    return_list = []
    contents = os.listdir(s.csvdir)
    for item in contents:
        if re.match(r'[0-9]*-[0-9]{2}\.csv', item):
            return_list.append(os.path.join(s.csvdir, item))
    return return_list

# Returns path to latest csv path, or None, if there are no files
def get_latest_available_csv():
    current_newest = 0
    available = get_available_csvs()
    if len(available) == 0:
        return None
    else:
        available.sort()
        return available[-1]

# Removes all old csv files
def remove_old_csv():
    current_year, current_week = datetime.date.today().isocalendar()[0:2]

    available = get_available_csvs()
    for item in available:
        if re.match(r'[0-9]*-[0-9]{2}*\.csv', os.path.basename(item)):
            csv_year = int(item[-11:-7])
            csv_week = int(item[-6:-4])
            if csv_year != current_year or csv_week != current_week:
                shutil.rmtree(item)

# Download latest csv file. Returns path to extracted csv file
def download_csv():
    current_year, current_week = datetime.date.today().isocalendar()[0:2]

    basename = '{0}-{1:02d}'.format(current_year,current_week)

    gz_path = os.path.join(s.csvdir, basename+'.gz')
    url = 'https://androzoo.uni.lu/static/lists/latest.csv.gz'
    store_path = os.path.join(s.csvdir, basename+'.csv')
    dld.perform_download(gz_path, url, store_path)
    os.remove(gz_path)
    return store_path

# Gets a csv to randomly choose from
def get_csv():
    current_year, current_week = datetime.date.today().isocalendar()[0:2]
    latest = get_latest_available_csv()
    if latest == None:
        print('No csv\'s found')
        return download_csv()

    print('Found latest csv: '+os.path.basename(latest))
    if '{0}-{1:02d}'.format(current_year,current_week) in latest:
        return latest

    if menu.standard_yesno('A newer version is available from androzoo. Download?'):
        return download_csv()
    else:
        return latest