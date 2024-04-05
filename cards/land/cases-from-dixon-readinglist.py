#!/usr/bin/python


#""" -*- coding: utf-8 -*-""" 

import codecs

import sys, re
currentLecture = ''
currentSubheading = ''
currentHeading = ''

accruedLines = []

namesUsed = []

def flushAccruedLinesToFile():
    global accruedLines
    print 'Writing '+str(len(accruedLines))+' lines to file "'+currentFilename+'".'
    f = open(currentFilename,'w')
    
    for x in accruedLines:
        f.write(x+'\n')
    f.close()
    accruedLines = []
    
caseEncounters = {}


subjectHeading = '';
atLeastOneSummaryTagAdded = False
#nb difflib for evaluating string similarity.

#for cases:
currentParaType = ''
currentBodyCaseName = ''


import difflib 

def alldigits(s):
    for c in s:
        if not c.isdigit():
            return False
    return True

def tit(s):
    #Existing Contractual Obligations To The Promisor As Consideration
    s = s.title()
    for (a,b) in [ ('<I>', '|'), ('</I>','|'), ('V', 'v'), ("'S","'s"), ('To ','to '), ('As ','as '),('The ',''), ('A ','a '), ('Of ','of '), ('On ', 'on '), ('And ','and ') ]:
        s = s.replace(a,b)
    return s


casesSeen = {}
    
    
for line in open(sys.argv[1]).readlines(): 
    if len(line.rstrip()) == 0:
        continue
        
    l = line.rstrip().lstrip()

    if l.upper() == l:  #probably a subject heading
        subjectHeading = tit(line.rstrip().lstrip())
        minorHeading = ''
        continue
        
        
    caseRe = re.match(r'(\**)([ \w\d]{4,50})([[(]{1}\d\d\d\d[\])]{1})(.+)', l)
        
    #caseRe = re.match(r'(\**)([ \w\d]{4,50})([[(]{1}\d\d\d\d[\])]{1})',  l)
    if caseRe:
        importance = len(caseRe.groups()[0])
        flags = ''
        if importance == 1: 
            flags = 'Important'
        elif importance == 2:
            flags = 'Key'
        elif importance == 3:
            flags = 'Vital'
            
        name = caseRe.groups()[1].lstrip().rstrip()
        year = caseRe.groups()[2].lstrip('([').rstrip(')]')
        citation = caseRe.groups()[3].lstrip().rstrip().replace('.','')
        
        for b in [':', ';', '-', ',', '(', ' and ', ' at ', ' on ']:
            if b in citation:
                citation = citation.split(b)[0]
        
        if not name in casesSeen:
            print name+'/'+year+' '+citation
            casesSeen[name] = True
            
    
    
        
    
        
if len(accruedLines) > 0:
    flushAccruedLinesToFile()
        

