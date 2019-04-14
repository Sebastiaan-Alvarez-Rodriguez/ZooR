#!/usr/bin/env python

import os
import re
import shutil
import datetime

import lib.filter.filter as filtor
import lib.menu as menu
import lib.settings as s

# Returns list of all filter files in csvdir
def get_available_filters():
    if not os.path.isdir(s.filtersdir):
        return []
    return_list = []
    contents = os.listdir(s.filtersdir)
    for item in contents:
        if item.endswith('.filter'):
            return_list.append(os.path.join(s.filtersdir, item))
    return return_list

# Ask user what to use as size-range filter
def ask_size_range():
    minimum = 0
    maximum = 0
    while True:
        choice = input('Please provide a minimal size in bytes: ')
        if len(choice) == 0 or not choice.isdigit():
            print('Please specify a number')
            continue
        else:
            minimum = int(choice)
        choice = input('Please provide a maximum size in bytes: ')
        if len(choice) == 0 or not choice.isdigit():
            print('Please specify a number')
        elif int(choice) < minimum:
            print('Min is more than max. Try again')
        else:
            maximum = int(choice)
            return minimum, maximum

# Ask user what to use as markets filter
def ask_markets():
    returnset = set()
    markets=set(['1mobile','angeeks','anzhi','apk_bang','appchina',
    'fdroid','freewarelovers','genome','hiapk','markets','mi.com',
    'play.google.com','proandroid','slideme','torrents'])
    optionsdict = menu.make_optionsdict(markets)
    while True:
        for item in optionsdict:
            print('\t\t'+'['+str(item)+'] - '+optionsdict[item])
        print('\t[E]verything')
        choice = input('Please make a choice (or multiple, comma-separated): ').upper()
        words = choice.split(',')
        for word in words:
            if word in ('E', 'EVERYTHING'):
                return markets
            elif word.isdigit() and int(word) in optionsdict:
                returnset.add(optionsdict[int(word)])
            else:
                print('Unknown option "'+word+'"')
        if len(returnset) > 0:
            return returnset

# Asks user a date and returns it
def ask_date(minmax):
    while True:
        choice = input('Please specify a '+minmax+' date in YYYY-MM-DD: ')
        try:
            return datetime.datetime.strptime(choice, "%Y-%m-%d").date()
        except Exception as e:
            print('Error: please try again')

# Asks user a min and max date and returns them
def ask_dates():
    minimum = None
    maximum = None
    while True:
        minimum = ask_date('minimum')
        maximum = ask_date('maximum')
        if minimum > maximum:
            print('Minimum date greater than maximum. Try again')
        else:
            return minimum, maximum

# Ask users for a number and return it
def ask_number(minmax):
    while True:
        choice = input('Please give a '+minmax+' value: ')
        if len(choice) == 0 or not choice.isdigit():
            print('Please specify a number')
        else:
            return int(choice)

# Ask user for a virus-range
def ask_virusrange():
    minimum = 0
    maximum = 0
    while True:
        minimum = ask_number('minimum')
        maximum = ask_number('maximum')
        if minimum > maximum:
            print('Minimum date greater than maximum. Try again')
        else:
            return minimum, maximum

# ask user for a directory+filename
def ask_filtername(question):
    while True:
        print(question)
        choice = input('')
        if os.path.isfile(choice+'.filter'):
            if standard_yesno('"'+choice+'" exists, override?'):
                return choice+'.filter'
        else:
            return choice+'.filter'

# Constructs filter with user input and returns it (and asks to save)
def ask_filter():
    return_filter = filtor.Filter()
    if menu.standard_yesno('Do you want a size range?'):
        return_filter.size_min, return_filter.size_min = ask_size_range()
    if menu.standard_yesno('Do you want to specify markets?'):
        return_filter.markets = ask_markets()
    if menu.standard_yesno('Do you want a date range?'):
        return_filter.date_min, return_filter.date_max = ask_dates()
    if menu.standard_yesno('Do you want a virus indication range?'):
        print('0 means not a virus. Higher means detected as virus more often')
        return_filter.virus_detect_min, return_filter.virus_detect_max = ask_virusrange()

    if menu.standard_yesno('Do you want to save this filter configuration?'):
        filename = ask_filtername('Please give a filename')
        os.makedirs(s.filtersdir, exist_ok=True)
        return_filter.to_file(os.path.join(s.filtersdir,filename))
    return return_filter

# Ask user to specify a filter to be returned
def choose_filter():
    available = get_available_filters()
    optionsdict = menu.make_optionsdict(available)
    while True:
        for item in optionsdict:
            print('\t'+'['+str(item)+'] - '+os.path.basename(optionsdict[item]))
        choice = input('Please make a choice: ').upper()
        
        if choice.isdigit() and int(choice) in optionsdict:
            return filtor.Filter(optionsdict[int(choice)])
        else:
            print('Unknown option "'+choice+'"')
    
# Gets a filter to use for choosing
def get_filter():
    available = get_available_filters()
    filter_amount = len(available)
    print('Found '+str(filter_amount)+' filters')

    if filter_amount == 0:
        return ask_filter()
    else:
        if menu.standard_yesno('Do you want to use a stored filter?'):
            return choose_filter()
        else:
            print('Making new filter')
            return ask_filter()
    if menu.standard_yesno('A newer version is available from androzoo. Download?'):
        return download_csv()
    else:
        return latest