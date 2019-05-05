#!/usr/bin/env python
import os

import lib.menu as menu
import lib.settings as s
import lib.download as dld
import lib.firepool as firepool

def parallel_download(element, directory, baseurl):
    path = os.path.join(directory, 'androzoo-{0}.apk'.format(element.md5))
    totalurl = '{0}&sha256={1}'.format(baseurl,element.sha256)
    dld.perform_download(path, totalurl)

def arg_generator(samplelist, directory, baseurl):
    args = []
    for item in samplelist:
        args.append((item,directory,baseurl,))
    return args

# Gets a csv to randomly choose from
def download(samplelist):
    directory = menu.ask_directory('Where do you want to store apk\'s?', must_exist=False)
    baseurl = 'https://androzoo.uni.lu/api/download?apikey={0}'.format(s.key)

    args = arg_generator(samplelist, directory, baseurl)

    pool = firepool.Firepool()
    pool.fire(parallel_download, args)