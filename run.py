#!/usr/bin/env python
import sys
import os

# Checks python version and exits if it is too low
# Must be specified before any lib imports (using v3.3) are done
def check_version():
    if sys.version_info < (3,3):
        print('I am sorry, but this script is for python3.3+ only!')
        exit(1)
check_version()

import lib.settings as s
import lib.csv.csv as csv
import lib.data.dataset as dataset
import lib.filter.filterhandler as filterhandler
import lib.picker.picker as picker
import lib.zoo.zoodownloader as zoo
import lib.menu as menu

# Get absolute path to this script
def get_loc():
    return os.path.abspath(os.path.dirname(sys.argv[0]))

# Ask user for key and write result in key file
def make_key():
    while True:
        print('Please paste your key below:')
        key = input('')
        key = key.strip(' ')
        key = key.strip('\t')
        key = key.strip('\r')
        key = key.strip('\n')
        keylength = len(key)
        if (keylength != 64):
            errortype = 'long' if keylength > 64 else 'short'
            print('Error: Key too '+errortype+'. Please try again')
        else:
            os.makedirs(os.path.dirname(s.keypath), exist_ok=True)
            with open(s.keypath, 'w') as file:
                file.write(key)
            print('Key written to '+s.keypath)
            return key

# Get stored key if available, otherwise ask user for key
def get_key():
    if not os.path.isfile(s.keypath):
        return make_key()
    else:
        with open(s.keypath, 'r') as file:
            key = file.readline()
        if len(key) != 64:
            print('Key is corrupt. Please re-enter key')
            return make_key()
        else:
            print('Key found!')
            return key


# Main function of this simple tool
def main():
    s.init(get_loc())
    s.init_key(get_key())

    print('Hello, this tool has been made to download samples from androzoo dataset')
    print('')

    data_set = dataset.Dataset(csv.CSV(), filterhandler.get_filter())

    print('Dataset ready for use')

    pick = picker.Picker(data_set)

    sample_size = pick.ask_samplesize()

    print('Starting selection procedure')
    sample_array = pick.pick(sample_size)
    print('Done!')
    if menu.standardyesno('Do you want to save full md5-list?'):
        chosen_path = menu.ask_path('Please provide a path')
        with open(chosen_path, 'w') as file:
            for element in sample_array:
                file.write('{0}\n'.format(element))
    zoo.download(sample_array)

if __name__ == '__main__':
    main()