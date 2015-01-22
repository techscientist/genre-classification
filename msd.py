__author__ = 'ag'


import os
import sys
import csv
import time
import glob
import datetime
import sqlite3
import numpy as np
from sklearn.cluster import KMeans
from pyechonest import config, artist
from pyechonest.util import EchoNestIOError, EchoNestAPIError



config.ECHO_NEST_API_KEY="VQXAWFOTEXJJTNJAP"
msd_subset_path= os.getcwd() + '/MillionSongSubset'
msd_subset_data_path=os.path.join(msd_subset_path,'data')
msd_subset_addf_path=os.path.join(msd_subset_path,'AdditionalFiles')
assert os.path.isdir(msd_subset_path),'wrong path'
msd_code_path = os.getcwd() + '/MSongsDB'
assert os.path.isdir(msd_code_path), 'wrong path'

sys.path.append(os.path.join(msd_code_path, 'PythonSrc'))

import hdf5_getters as GETTERS


def apply_to_all_files(basedir ,func=lambda x: x,ext='.h5'):
    row = 0
    for root, dirs, files in os.walk(basedir):

        files = glob.glob(os.path.join(root, '*'+ext))
        # count files
        # apply function to all files
        for f in files:
            print row
            func(f)
            row += 1

pyarray = []
def get_key_tempo(filename):
    h5 = GETTERS.open_h5_file_read(filename)
    tempo = GETTERS.get_tempo(h5)
    key = GETTERS.get_key(h5)
    ar = GETTERS.get_artist_name(h5)
    title = GETTERS.get_title(h5)

    st = ""
    terms = None
    try:
        a = artist.Artist(str(ar))
        terms = a.get_terms()
        time.sleep(.12)
    except EchoNestIOError as e:
        print "echonestIOerror"
    except EchoNestAPIError as e:
        if e.code == 3:
            time.sleep(1)
        elif e.code == 5:
            print "code is 5"
        else:
            print "error.."
    if terms:
        print terms[0]['name']
        with open('points.csv', 'a') as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerow([tempo, key, ar, title, terms[0]['name']])
    h5.close()


def main():
    # with open('points.csv', 'w') as fp:
    #     a = csv.writer(fp, delimiter=',')
    #     a.writerow(['tempo', 'key', 'ar', 'title', 'style'])
    # apply_to_all_files(msd_subset_data_path, func=get_key_tempo)
    a = []
    csvReader = csv.reader(open('points copy.csv', 'rb'), delimiter=',')
    for row in csvReader:
        a.append([row[0], row[1]])
    fb = open('arr', 'w')
    fb.write(str(a))
    fb.close()
    # arr = np.array(a)
    # print arr
    # km = KMeans(n_clusters=777)
    # km.fit(arr)
    #
    # with open('centers.csv', 'w') as fp:
    #     a = csv.writer(fp, delimiter=',')
    #     a.writerow(['tempo', 'key'])
    #     for center in km.cluster_centers_:
    #         a.writerow(center)

if __name__=='__main__':
    main()