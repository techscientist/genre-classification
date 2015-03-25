__author__ = 'ag'


import os
import sys
import csv
import time
import glob
import datetime
import sqlite3
import operator
import json
import random
import numpy as np
from sklearn.cluster import KMeans
from pyechonest import config, artist
from pyechonest.util import EchoNestIOError, EchoNestAPIError
from collections import defaultdict
#import hdf5_getters as GETTERS


def pre():
    config.ECHO_NEST_API_KEY="VQXAWFOTEXJJTNJAP"
    msd_subset_path= os.getcwd() + '/MillionSongSubset'
    msd_subset_data_path=os.path.join(msd_subset_path,'data')
    msd_subset_addf_path=os.path.join(msd_subset_path,'AdditionalFiles')
    assert os.path.isdir(msd_subset_path),'wrong path'
    msd_code_path = os.getcwd() + '/MSongsDB'
    assert os.path.isdir(msd_code_path), 'wrong path'

    sys.path.append(os.path.join(msd_code_path, 'PythonSrc'))



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


# def get_key_tempo(filename):
#     h5 = GETTERS.open_h5_file_read(filename)
#     tempo = GETTERS.get_tempo(h5)
#     key = GETTERS.get_key(h5)
#     ar = GETTERS.get_artist_name(h5)
#     title = GETTERS.get_title(h5)
#
#     terms = None
#     try:
#         a = artist.Artist(str(ar))
#         terms = a.get_terms()
#         time.sleep(.12)
#     except EchoNestIOError as e:
#         print "echonestIOerror"
#     except EchoNestAPIError as e:
#         if e.code == 3:
#             time.sleep(1)
#         elif e.code == 5:
#             print "code is 5"
#         else:
#             print "error.."
#     if terms:
#         print terms[0]['name']
#         with open('points.csv', 'a') as fp:
#             a = csv.writer(fp, delimiter=',')
#             a.writerow([tempo, key, ar, title, terms[0]['name']])
#     h5.close()


'''
Fetches number of artists in data set
Used for Artist histogram
'''


def get_artist():
    d = {}
    csv_reader = csv.reader(open('points copy.csv', 'rb'), delimiter=',')

    for row in csv_reader:
        if row[2] not in d:
            d[row[2]] = 1
        else:
            d[row[2]] += 1
    sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)

    writer = csv.writer(open('total/all_artists.csv', 'wb'))
    for key, value in sorted_d:
        writer.writerow([key, value])

'''
Fetches number of genres in dataset
Used for genre histogram
'''


def get_genres():
    d = {}
    csv_reader = csv.reader(open('points copy.csv', 'rb'), delimiter=',')

    for row in csv_reader:
        if row[4] not in d:
            d[row[4]] = 1
        else:
            d[row[4]] += 1

    sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)

    writer = csv.writer(open('total/all_genres.csv', 'wb'))
    for key, value in sorted_d:
        writer.writerow([key, value])

'''
Random sample of artists and their respective keys in the data set
'''


def artist_to_key():
    d = defaultdict(list)
    l = list(tuple())
    csv_reader = csv.reader(open('points copy.csv', 'rb'), delimiter=',')

    for row in csv_reader:
        l.append((row[2], row[1]))
        d[row[4]].append(row[1])

    rand = [l[i] for i in sorted(random.sample(xrange(len(l)), 100))]

    writer = csv.writer(open('random/artist_key.csv', 'w'))
    for key, value in rand:
        writer.writerow([key, value])

'''
Random sample of artists and their tempos in the data set
'''


def artist_to_tempo():
    d = defaultdict(list)
    l = list(tuple())
    csv_reader = csv.reader(open('points copy.csv', 'rb'), delimiter=',')

    for row in csv_reader:
        l.append((row[2], row[0]))
        d[row[2]].append(row[0])

    rand = [l[i] for i in sorted(random.sample(xrange(len(l)), 100))]

    writer = csv.writer(open('random/artist_tempo.csv', 'w'))
    for key, value in rand:
        writer.writerow([key, value])

'''
Random sample of artists and their tempos in the data set
'''


def genre_to_key():
    d = defaultdict(list)
    l = list(tuple())
    csv_reader = csv.reader(open('points copy.csv', 'rb'), delimiter=',')

    for row in csv_reader:
        l.append((row[4], row[1]))
        d[row[4]].append(row[1])

    rand = [l[i] for i in sorted(random.sample(xrange(len(l)), 100))]

    writer = csv.writer(open('random/genre_key.csv', 'w'))
    for key, value in rand:
        writer.writerow([key, value])

'''
Random sample of genres and their tempos
'''


def genre_to_tempo():
    d = defaultdict(list)
    l = list(tuple())
    csv_reader = csv.reader(open('points copy.csv', 'rb'), delimiter=',')

    for row in csv_reader:
        l.append((row[4], row[0]))
        d[row[4]].append(row[0])

    rand = [l[i] for i in sorted(random.sample(xrange(len(l)), 100))]

    writer = csv.writer(open('random/genre_tempo.csv', 'w'))
    for key, value in rand:
        writer.writerow([key, value])


'''
There are a total of 307 genres, so we will have 307 clusters
'''

def apply_kmeans():
    a = []
    csv_reader = csv.reader(open('points copy.csv', 'rb'), delimiter=',')
    for row in csv_reader:
        a.append([row[0], row[1]])

    arr = np.array(a)
    km = KMeans(n_clusters=307)
    km.fit(arr)

    with open('kmeans_clustercenters.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(['tempo', 'key'])
        for center in km.cluster_centers_:
            a.writerow(center)


def write_key_tempo():
    with open('points.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(['tempo', 'key', 'ar', 'title', 'style'])
    #apply_to_all_files(msd_subset_data_path, func=get_key_tempo)
    a = []
    csvReader = csv.reader(open('points copy.csv', 'rb'), delimiter=',')
    for row in csvReader:
        a.append([row[0], row[1]])
    fb = open('arr', 'w')
    fb.write(str(a))
    fb.close()


def main():
    apply_kmeans()

if __name__=='__main__':
    main()