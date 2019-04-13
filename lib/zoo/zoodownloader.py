#!/usr/bin/env python
import os

import lib.menu as menu
import lib.settings as s
import lib.download as dld
import lib.firepool as firepool

def parallel_download(listitem, directory, baseurl):
    sha256 = listitem.split(',', 1)[0]
    md5 = listitem.split(',', 3)[2]
    path = os.path.join(directory, md5+'.apk')
    totalurl = baseurl+'&sha256='+sha256
    dld.perform_download(path, totalurl)

def arg_generator(samplelist, directory, baseurl):
    args = []
    for item in samplelist:
        args.append((item,directory,baseurl,))
    return args

# Gets a csv to randomly choose from
def download(samplelist):
    directory = menu.ask_directory('Where do you want to store apk\'s?')
    baseurl = 'https://androzoo.uni.lu/api/download?apikey='+s.key

    args = arg_generator(samplelist, directory, baseurl)

    pool = firepool.Firepool()
    pool.fire(parallel_download, args)
