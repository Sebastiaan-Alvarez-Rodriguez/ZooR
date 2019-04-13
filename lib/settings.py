#!/usr/bin/env python
import os

def init(_path):
    global root
    root = _path
    global filtersdir
    filtersdir = os.path.join(_path, 'saved_filters')
    global csvdir
    csvdir=os.path.join(_path, 'androzoo')
    global keypath
    keypath=os.path.join(os.path.join(_path, 'androzoo'), '.key')

def init_key(_key):
    global key
    key=_key