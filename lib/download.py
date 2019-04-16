#!/usr/bin/env python
import os
import urllib.request
import tarfile
import zipfile
import gzip
import shutil

def download(path, url):
    print('downloading '+url)

    u = urllib.request.urlopen(url)
    with open(path, 'wb') as out_file:
        out_file.write(u.read())

def extract(compressed_path, decompressed_path):
    if compressed_path.endswith(".tar")\
    or compressed_path.endswith(".tar.xz")\
    or compressed_path.endswith(".tar.gz")\
    or compressed_path.endswith(".tgz"):
        print('extracting ' + os.path.basename(compressed_path))
        ttar = tarfile.open(compressed_path, 'r')
        ttar.extractall(path=decompressed_path)
    elif compressed_path.endswith(".zip"):
        print('extracting ' + os.path.basename(compressed_path))
        tzip = zipfile.ZipFile(compressed_path, 'r')
        tzip.extractall(decompressed_path)
        tzip.close()
    elif compressed_path.endswith(".gz"):
        print('extracting ' + os.path.basename(compressed_path))
        with gzip.open(compressed_path, 'rb') as f_in:
            with open(decompressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    else:
        print('no format found (required: zip|tar(.xz)|tgz)')
        return

# Perform a download operation
def perform_download(path, url, extraced_path=None):
    try:
        download(path, url)
        if extraced_path != None:
            if path.endswith(".tar") or path.endswith(".tar.gz") \
            or path.endswith(".tar.xz") or path.endswith(".tgz") \
            or path.endswith(".zip") or path.endswith('.gz'):
                extract(path, extraced_path)
    except urllib.error.HTTPError as e:
        print('HTTPError = {0}'.format(str(e.code)))
    except urllib.error.URLError as e:
        print('URLError = {0}'.format(str(e.reason)))
    except urllib.error.HTTPException as e:
        print('HTTPException = {0}'.format(str(e)))
    except Exception as e:
        print('Error: {0}'.format(str(e)))
