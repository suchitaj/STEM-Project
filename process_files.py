#!/usr/bin/env python3
'''
./process_files.py neuropsychiatric-csv-OMIM neuropsychiatric-txt-Entrez neuropsychiatric
./process_files.py neurodegenerative-csv-OMIM neurodegenerative-txt-Entrez neurodegenerative
./process_files.py endrocrine_system-csv-OMIM endrocrine_system-txt-Entrez endrocrine_system
./process_files.py hemic_and_lymphatic-csv-OMIM hemic_and_lymphatic-txt-Entrez hemic_and_lymphatic
./process_files.py respiratory_tract-csv-OMIM respiratory_tract-txt-Entrez respiratory_tract
./process_files.py skin_and_connective_tissue-csv-OMIM skin_and_connective_tissue-txt-Entrez skin_and_connective_tissue

'''
import csv
import sys
import os

def processCsvDir(dirname, sep, diseaseMap):
    print(dirname)
    for filename in os.listdir(dirname):
        print(filename)
        prefix = filename.split('.')[0]
        diseaseMap[prefix] = set()
        with open(dirname + '/' + filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile, dialect='excel', delimiter=sep, quotechar='"')
            #csvreader = csv.reader(csvfile, delimiter=sep, quotechar='"')
            i = 0
            for row in csvreader:
                #print(i, row)
                i += 1
                if row[0] and row[0][0] in ['+', '*']:
                    entrezId = row[5]
                    #print(entrezId, ', '.join(row))
                    diseaseMap[prefix].add(entrezId)
    return

def processTabDir(dirname, sep, diseaseMap):
    print(dirname)
    for filename in os.listdir(dirname):
        print(filename)
        prefix = filename.split('.')[0]
        with open(dirname + '/' + filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=sep, quotechar='"')
            for row in csvreader:
                entrezId = row[2].strip()
                if row[2].isdigit():
                    #print(entrezId, ', '.join(row))
                    diseaseMap[prefix].add(entrezId)
    return

def writeFile(k, v):
    f = open(k + '.txt', 'w')
    f.truncate()
    for i in v:
        f.write(i + '\n')
    f.close()
    
def main():
    diseaseMap = {}
    
    # open the first directory - assume it has csv files
    dirCsv = sys.argv[1]
    processCsvDir(dirCsv, ',', diseaseMap)

    # open the second directory - assume it has \t separated txt files
    dirTab = sys.argv[2]
    processTabDir(dirTab, '\t', diseaseMap)

    for k,v in diseaseMap.items():
        writeFile(sys.argv[3] + '/' + k, v)

if __name__ == '__main__':
    main()
