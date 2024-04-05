#!/usr/bin/python


#""" -*- coding: utf-8 -*-""" 

import codecs

import sys, re
currentLecture = ''
currentSubheading = ''
currentHeading = ''
currentFilename = ''
currentLectureNum = 2 #starts at 2, no need to put intro  in.

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

consumingToC = False
toc = []

cases = []
casesToHeadings = {}
currentSubjectCaseList = []
lectureHeadings = []


majorHeading = ''
minorHeading = ''
numberHeadingName= ''
numberHeadingNum = ''
atLeastOneSummaryTagAdded = False
#nb difflib for evaluating string similarity.

#for cases:
currentParaType = ''
currentBodyCaseName = ''

listChar = '+'
numChar = '#'
plainChar = ':'
potentialConcept = ''

currentSetOfTags = ''

import difflib 

def alldigits(s):
    for c in s:
        if not c.isdigit():
            return False
    return True

def tit(s):
    #Existing Contractual Obligations To The Promisor As Consideration
    s = s.capitalize().title()
    for (a,b) in [ ('<I>', '|'), ('</I>','|'), (' V ', ' v '), ("'S","'s"), (' To ',' to '), (' As ',' as '),(' The ',' '), (' A ',' a '), (' Of ',' of '), (' On ', ' on '), (' And ',' and ') ]:
        s = s.replace(a,b)
    return s.strip('.').strip('"')



def getCats(s):
    s = s.replace(':',';')
    if ' (' in s:
        s = s.replace(' (','; ').replace(')','')
        
    return [tit(c).strip(' ') for c in s.split('/')]

def prepPara(p):
    if p.endswith('</i>.'):
        p = p[:len('</i>.')] + '.'
        
    p = p.replace('<i>','_').replace('</i>','_')
    return p
    
def prepHeld(p):
    if p.lower().startswith('held:'):
        p = p[len('held:'):].lstrip().rstrip('><');

    return prepPara(p)
    

if __name__=='__main__':
    
    
    prevLineWasACase = False
    namesUsed = []
    
    for l in [line.rstrip() for line in open(sys.argv[1]).readlines()]:
        
        if l.startswith('<p><b><i>'):
            n = l[len('<p><b><i>'): - len('</b></p>') ] #.lstrip('<p><b><i>').rstrip('</b></p>')
            #everything until </i> is the case name, everything after, the citation.
            caseName = n[:n.find('</i>')].strip('><').strip(' ')
            cit = n[n.find('</i>')+3:]

            print '\n\n\n\n\n'
            if caseName in set(namesUsed):
                caseName += ' '+cit[2:8]
                
            print 'NAME '+caseName
            namesUsed += [caseName]
            
            print 'CITATION '+n.replace('</i>','')
            prevLineWasACase = True
        
        elif l.startswith('<p><i>'):
            print 'HELD ' + prepHeld(l[len('<p><b>') : - len('</i></p>') ] )
            #.lstrip('<p><i>').rstrip('</i></p>').lstrip('Held:'))
            prevLineWasACase = False
            
        elif l.startswith('<p>') and prevLineWasACase:
            cats = getCats(l[3:-4])
            for cat in cats:
                print 'CATEGORY '+cat.strip()
                
            prevLineWasACase = False
        elif l.startswith('<p>') and not l.startswith('<p><b>'):
            print 'SUMMARY '+prepPara(l[3:-4]) # .lstrip('<p>').rstrip('</p>'))
        
            
        else:
            if len(l) > 0:
                pass
                #print ' *** indigestible line: "'+l+'"'
            








