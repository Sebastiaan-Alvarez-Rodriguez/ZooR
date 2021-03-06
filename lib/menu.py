#!/usr/bin/env python
import os

# ask user for a directory
# must exist determines wheter it explicitly must or must not exist
def ask_directory(question, must_exist=True):
    while True:
        print(question)
        print('Paths may be absolute or relative to your working directory')
        print('Working directory: {0}'.format(os.getcwd()))
        print('Please specify a directory:')
        choice = input('')
        choice = choice if choice[0]=='/' else os.getcwd()+'/'+choice
        choice = os.path.normpath(choice)
        if must_exist:
            if not os.path.isdir(choice):
                print('Error: no such directory - "{0}"'.format(choice))
            else:
                return choice
        else:
            if os.path.isdir(choice):
                print('"{0}" already exists'.format(choice))
                if standard_yesno('continue?'):
                    return choice
            else:
                os.makedirs(choice, exist_ok=True)
                return choice

# ask user for a directory+filename
def ask_path(question):
    while True:
        print(question)
        print('Paths may be absolute or relative to your working directory')
        print('Please specify a path:')
        choice = input('')
        choice = choice if choice[0]=='/' else os.getcwd()+'/'+choice
        choice = os.path.normpath(choice)
        if not os.path.isdir(os.path.dirname(choice)):
            print('Error: no such directory - "{0}"'.format(os.path.dirname(choice)))
        elif os.path.isfile(choice):
            if standard_yesno('"{0}" exists, override?'.format(choice)):
                return choice
        else:
            return choice

# Maps numbers (starting from 0) to components for user select
def make_optionsdict(components):
    returndict={}
    for number, component in enumerate(components):
        returndict[number] = component
    return returndict

# Simple method to ask user a yes/no question. Result returned as boolean.
# Returns True if user responded positive, otherwise False
def standard_yesno(question):
    while True:
        choice = input(question+' [Y/n] ').upper()
        if choice in ('Y', 'YES'):
            return True
        elif choice in ('N', 'NO'):
            return False
        else:
            print('Invalid option "{0}"'.format(choice))
