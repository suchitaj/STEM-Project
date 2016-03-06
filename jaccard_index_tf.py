#!/usr/bin/env python3
'''
./jaccard_index_tf.py tfnd tfnp

Jaccard Index of two sets A and B = |A intersection B|/ |A Union B|

'''

import sys
import os
from collections import defaultdict
from go_obo_parser import go_obo_parser

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


def IsGoFactor(factorName):
    return factorName in ['GO: Molecular Function',
                          'GO: Biological Process',
                          'GO: Cellular Component']

def Processfile(disease, lines, diseaseMap, gp):
    diseaseMap[disease] = {}
    for l in lines:
        if GetMatchingFactor(l):
            currentFactor = GetMatchingFactor(l)
            #print(currentFactor)
            diseaseMap[disease][currentFactor] = {}
        else:
            rows = l.split()
            if rows[0].isdigit():
                factor = rows[1]
                diseaseMap[disease][currentFactor][factor] = set()
                diseaseMap[disease][currentFactor][factor].add(factor)
                isGoFactor = IsGoFactor(currentFactor)
                if isGoFactor:
                    parents = gp.getAncestors(factor)
                    diseaseMap[disease][currentFactor][factor].union(parents)

def processDir(dirname, diseaseMap, gp):
    print('Directory', dirname)
    for filename in os.listdir(dirname):
        print('Processing file ', filename)
        parts = filename.split('.')
        if len(parts) != 2 or not parts[0]:
            print('Skipping', filename)
            continue
        prefix = parts[0]
        diseaseMap[prefix] = set()
        with open(dirname + '/' + filename, 'rb') as f:
            lines = f.readlines()
            Processfile(prefix, lines, diseaseMap, gp)

    return

def IntersectionWithGoFactors(aMap, bMap):
    # intersection using go-factors
    intSet = set()
    for k1,v1 in aMap.items():
        for k2,v2 in bMap.items():
            if k1 in v2 or k2 in v1:
                intSet.add(k1)
                intSet.add(k2)
    return intSet
                
def JaccardIndexGoFactors(aMap, bMap):
    aib = IntersectionWithGoFactors(aMap, bMap)
    a = set(aMap.keys())
    b = set(bMap.keys())
    aub = a | b
    return float(len(aib))/ float(len(aub))

def JaccardIndex(aMap, bMap):
    a = set(aMap.keys())
    b = set(bMap.keys())
    aib = a & b
    aub = a | b
    return float(len(aib))/ float(len(aub))

def CompareSets(map1, map2):
    jiMap = {} 
    jiAvgMap = defaultdict(float)
    for k, f in prefixFactors.items():
        print('\n', f)
        isGoFactor = IsGoFactor(f)
        lst = []
        for k1, v1 in map1.items():
            for k2, v2 in map2.items():
                if isGoFactor:
                    ji = JaccardIndexGoFactors(v1[f], v2[f])
                else:
                    ji = JaccardIndex(v1[f], v2[f])
                lst.append((k1, k2, ji))
        jiMap[f] = list(reversed(sorted(lst, key = lambda tup: tup[2])))
        for tup in jiMap[f]:
            k1 = tup[0]
            k2 = tup[1]
            ji = tup[2]
            print('{:<20} {:<20} {:.2%}'.format(k1, k2, ji))
            jiAvgMap[k1 + ' ' + k2] += ji 

    print('\n\nJaccard Index across all factors, sorted by Average\n')
    lst = []
    for k, v in jiAvgMap.items():
        ks = k.strip().split()
        lst.append((ks[0], ks[1], v, v/len(prefixFactors)))
    l = list(reversed(sorted(lst, key = lambda tup: tup[3])))
    for tup in l:
        print('{:<20} {:<20} {:15.2%}'.format(tup[0], tup[1], tup[3]))
        
def main():
    print("Reading and parsing the obo file.")
    inpOboFile = "./go.obo"
    gp = go_obo_parser()
    gp.parseOBO(inpOboFile)
    print("Parsing complete.", inpOboFile)

    diseaseMap1 = {}
    processDir(sys.argv[1], diseaseMap1, gp)
    #print(diseaseMap1)
    diseaseMap2 = {}
    processDir(sys.argv[2], diseaseMap2, gp)


    #Get all anscestors of a GO Term
    #parents = gp.getAncestors('GO:2001282')
    #print("Parents of GO:2001282")
    #for parent in parents:
    #    print(str(parent))

    CompareSets(diseaseMap1, diseaseMap2)

if __name__ == '__main__':
    main()
g
