#!/usr/bin/env python3
'''
./jaccard_index.py neuropsychiatric neurodegenerative

Computes Jaccard Index across all pairs of files in two directories.
Then emits all possible pairs reverse sorted by their Jaccard Index values.

Jaccard Index of two sets A and B = |A intersection B|/ |A Union B|

'''

import sys
import os

def processDir(dirname, diseaseMap):
    #print(dirname)
    for filename in os.listdir(dirname):
        #print(filename)
        parts = filename.split('.')
        if len(parts) != 2 or not parts[0]:
            #print('Skipping', filename)
            continue
        prefix = parts[0]
        diseaseMap[prefix] = set()
        with open(dirname + '/' + filename, 'rb') as f:
            for l in f.readlines():
                diseaseMap[prefix].add(l)
    return

def JaccardIndex(a, b):
    aib = a & b
    aub = a | b
    return float(len(aib))/ float(len(aub))

def CompareSets(map1, map2):
    lst = []
    for k1, v1 in map1.items():
        for k2, v2 in map2.items():
            ji = JaccardIndex(v1, v2)
            lst.append((k1, k2, ji))
    l = list(reversed(sorted(lst, key = lambda tup: tup[2])))
    for tup in l:
        print('{:<20} {:<20} {:.2%}'.format(tup[0], tup[1], tup[2]))
            
def main():
    diseaseMap1 = {}
    processDir(sys.argv[1], diseaseMap1)
    diseaseMap2 = {}
    processDir(sys.argv[2], diseaseMap2)
    CompareSets(diseaseMap1, diseaseMap2)

if __name__ == '__main__':
    main()
