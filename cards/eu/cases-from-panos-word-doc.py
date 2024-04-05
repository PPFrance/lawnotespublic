#!/usr/bin/python


#""" -*- coding: utf-8 -*-""" 

import codecs

import sys, re
currentLecture = ''
currentSubheading = ''
currentHeading = ''
currentFilename = ''
currentLectureNum = 11

accruedLines = []


def flushAccruedLinesToFile():
    global accruedLines
    print 'Writing '+str(len(accruedLines))+' lines to file "'+currentFilename+'".'
    f = open(currentFilename,'w')
    
    for x in accruedLines:
        f.write(x+'\n')
    f.close()
    accruedLines = []
    
caseEncounters = {}

#Case 1/58 Stork v High Authority, [1959] ECR 17 
for line in open(sys.argv[1]).readlines(): #codecs.open(sys.argv[1], encoding='utf-8').readlines():
    
    if line.startswith('***'):
        currentSubheading = line.lstrip('***').lstrip().rstrip().title()
        
    if line.lstrip().rstrip().isupper():
        currentHeading = line.lstrip().rstrip().title()
        currentSubheading = ''
    
    lm = re.search(r'(Lecture)\s+(\d+)\s+(.*)', line)
    if lm:
        #A new lecture
        if (currentFilename != ''):
            flushAccruedLinesToFile()
        
        currentLecture = lm.groups()[2].lstrip().rstrip().title()
        currentFilename = currentLecture.lower().replace(',','').replace('.','').replace('-','')
        currentFilenameParts = [p for p in currentFilename.split() if p !='' and p !='-' and p != '\xe2\x80\x93']
        
        currentFilename = 'eu-'+str(currentLectureNum).zfill(2) + '-' + ('-'.join(currentFilenameParts))+'.fc.txt'
        currentLectureNum += 1
        accruedLines.append( 'META-FILENAME '+currentFilename+'\n\n\n\n\n')
    
    
    cm = re.search(r'C(ase)?[- ]+(\d+/\d+)[,\s]+([^[]*)[, ]+([\[\]\(\)\t\ \dA-Za-z:]*)', line)
    if cm:
        caseName = cm.groups()[2].lstrip().rstrip().rstrip(',').replace(' v. ',' v ')
        prefix = ''
        if caseName in caseEncounters:
            prefix = str(caseEncounters[caseName])
            print 'will prefix '+caseName+' with '+prefix
            caseEncounters[caseName] = caseEncounters[caseName] + 1
        else:
            caseEncounters[caseName] = 1
            
        accruedLines.append( 'NAME '+prefix+caseName)
        accruedLines.append( 'CASENUM C-'+cm.groups()[1])
        
        citation = cm.groups()[3].lstrip().rstrip().rstrip(',')
        if ': ' in citation: #probably best to get rid of everything after this...
            citation = citation[:citation.index(': ')]
        
        accruedLines.append( 'CITATION '+ caseName+ ' '+ citation)
        cats = [x for x in [currentLecture, currentHeading, currentSubheading] if x != '']
        accruedLines.append( 'CATEGORY '+ "; ".join(cats))
        accruedLines.append( 'FLAGS')
        accruedLines.append( 'SUMMARY TODO.')
        accruedLines.append( 'HELD')
        
        #accruedLines.append( '#fn: '+currentFilename
        accruedLines.append( '\n\n\n')
        
if len(accruedLines) > 0:
    flushAccruedLinesToFile()
        

