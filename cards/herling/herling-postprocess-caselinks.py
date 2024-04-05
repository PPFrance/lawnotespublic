#!/usr/bin/python


#""" -*- coding: utf-8 -*-""" 

import codecs

import sys, re, glob

names = []

def getNames(lines):
    global names
    
    for line in [l.lstrip().rstrip() for l in lines]:
        if line.startswith('NAME '):
            names.append(line.lstrip('NAME '))


def processFile(lines, newName):
    global names
    accruedLines = []
    currentName = ''
    for l in lines:
        line = l.rstrip()
        
        if line.startswith('NAME '):
            currentName == line.rstrip().lstrip('NAME ')
            
        r = re.search(r'(\<i\>([^<]+)\<\/i\>)', line)
        if r:
            matchWithTags = r.groups()[0]
            potentialName = r.groups()[1].lstrip().rstrip() 
            replacement = ''
            if potentialName in names:
                print potentialName
                if potentialName != currentName:
                    replacement = '|'+potentialName+'|'
                else:
                    replacement = '_'+potentialName+'_'

            if len(replacement) > 0:
                line = line.replace(matchWithTags, replacement)
                    
        accruedLines.append(line)

    f = open(newName,'w')

    for x in accruedLines:
        f.write(x+'\n')
    f.close()
    

files = sys.argv[1:]

for item in sys.argv[1:]:
    fs = sorted(glob.glob(item))
    #print >> sys.stderr, '* Reading "'+repr(fs)+'".'
    #lines += 
    for f in sorted(fs):
        getNames(open(f).readlines())
        

names = list(set(names))

for item in sys.argv[1:]:
    fs = sorted(glob.glob(item))
    #print >> sys.stderr, '* Reading "'+repr(fs)+'".'
    #lines += 
    for f in sorted(fs):
        processFile(open(f).readlines(), f+'.new.fc.txt')
