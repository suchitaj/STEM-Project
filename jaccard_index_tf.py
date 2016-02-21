#!/usr/bin/env python3
'''
./jaccard_index_tf.py neuropsychiatric neurodegenerative | sort -n -r -k 3 

Jaccard Index of two sets A and B = |A intersection B|/ |A Union B|

'''

import sys
import os
from collections import defaultdict

prefixFactors = {'1: GO: Molecular Function [Display Chart]' : 'GO: Molecular Function',
           '2: GO: Biological Process [Display Chart]' : 'GO: Biological Process',
           '3: GO: Cellular Component [Display Chart]' : 'GO: Cellular Component',
           '4: Human Phenotype [Display Chart]' : 'Human Phenotype',
           '5: Mouse Phenotype [Display Chart]' : 'Mouse Phenotype',
           '7: Pathway [Display Chart]' : 'Pathway'
}

def GetMatchingFactor(line):
    for k, v in prefixFactors.items():
        if k in str(line):
            return v
    return ''
    
    
def Processfile(disease, lines, diseaseMap):
    diseaseMap[disease] = {}
    for l in lines:
        if GetMatchingFactor(l):
            currentFactor = GetMatchingFactor(l)
            print(currentFactor)
            diseaseMap[disease][currentFactor] = set()
        else:
            rows = l.split()
            if rows[0].isdigit():
                diseaseMap[disease][currentFactor].add(rows[1])


def processDir(dirname, diseaseMap):
    print(dirname)
    for filename in os.listdir(dirname):
        print(filename)
        parts = filename.split('.')
        if len(parts) != 2 or not parts[0]:
            print('Skipping', filename)
            continue
        prefix = parts[0]
        diseaseMap[prefix] = set()
        with open(dirname + '/' + filename, 'rb') as f:
            lines = f.readlines()
            Processfile(prefix, lines, diseaseMap)

    return

def JaccardIndex(a, b):
    aib = a & b
    aub = a | b
    return float(len(aib))/ float(len(aub))

def CompareSets(map1, map2):
    jiMap = {} 
    jiAvgMap = defaultdict(float)
    for f in prefixFactors:
        print(f)
        lst = []
        for k1, v1 in map1.items():
            for k2, v2 in map2.items():
                ji = JaccardIndex(v1[f], v2[f])
                lst.append((k1, k2, ji))
        jiMap[f] = list(reversed(sorted(lst, key = lambda tup: tup[2])))
        for tup in jiMap[f]:
            k1 = tup[0]
            k2 = tup[1]
            ji = tup[2]
            print('{:<20} {:<20} {:.2%}'.format(k1, k2, ji))
            jiAvgMap[k1 + ' ' + k2] += ji 

    for k, v in jiAvgMap.items():
        print('{:<20} {:.2%} {:.2%}'.format(k, v, v/len(prefixFactors)))
        
def main():
    diseaseMap1 = {}
    processDir(sys.argv[1], diseaseMap1)
    #print(diseaseMap1)
    diseaseMap2 = {}
    processDir(sys.argv[2], diseaseMap2)
    CompareSets(diseaseMap1, diseaseMap2)

if __name__ == '__main__':
    main()
