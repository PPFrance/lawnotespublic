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
    s = s.title()
    for (a,b) in [ ('<I>', '|'), ('</I>','|'), ('V', 'v'), ("'S","'s"), ('To ','to '), ('As ','as '),('The ',''), ('A ','a '), ('Of ','of '), ('On ', 'on '), ('And ','and ') ]:
        s = s.replace(a,b)
    return s

#Case 1/58 Stork v High Authority, [1959] ECR 17 
for line in open(sys.argv[1]).readlines(): #codecs.open(sys.argv[1], encoding='utf-8').readlines():
    if len(line.rstrip()) == 0:
        continue
    #<p><b>GDL CONTRACT LECTURE 9</b></p>
    
    mLecture = re.search(r'(GDL CONTRACT LECTURE )(\d+) ([^\<]+)', line, re.IGNORECASE)
    if mLecture:
        if currentLecture != '':
            flushAccruedLinesToFile()
        else:
            accruedLines.append('META-SUBJECT herling')
            lectureHeadings = []
            
            
            
        num = mLecture.groups()[1]
        nam = tit(mLecture.groups()[2])
        currentLecture = nam
        currentLectureNum = num
        currentFilename = currentLecture.lower().replace(',','').replace('.','').replace('-','')
        currentFilenameParts = [p for p in currentFilename.split() if p !='' and p !='-' and p != '\xe2\x80\x93']
        
        currentFilename = 'herling-'+str(currentLectureNum).zfill(2) + '-' + ('-'.join(currentFilenameParts))+'.fc.txt'
        accruedLines.append( 'META-FILENAME '+currentFilename+'\n\n\n\n\n')
        print >> sys.stderr, 'New lecture: "'+currentLecture+'", filename: '+currentFilename
        
        continue
    
    if re.search(r'Contents and references', line, re.IGNORECASE ):
        consumingToC = True
        majorHeading = ''
        minorHeading = ''
        numberHeadingName= ''
        numberHeadingNum = ''
        toc = []


        accruedLines.append('NAME '+currentLecture+' - Table of Contents')
        accruedLines.append('TYPE Table of Contents')
        print >> sys.stderr, 'Consuming ToC'
        continue

    
        
    if consumingToC:
        
        majh = re.match(r'\<p\>([A-Z ]{2,})([\(\w\) ]*)\<\/p\>', line)
        if majh:
                        
            if len(currentSubjectCaseList) >0:
                accruedLines.append( '/-->--' + (' - '.join([ '|'+name+'|' for (name, citation) in currentSubjectCaseList]) ))
                #print >> sys.stderr, ' *** Printing cases: '+accruedLines[-1]
                currentSubjectCaseList = []


            majorHeading = tit(majh.groups()[0])
            #print >> sys.stderr, '\n\nMatched major heading: '+line+' - found "'+majorHeading+'".'
            #print >> sys.stderr, '**************************************************************'
            if len(majh.groups()[1])>0:
                majorHeading += ' '+tit(majh.groups()[1])
            
            lectureHeadings.append(majorHeading)
            
            #Reset all lower headings.
            minorHeading = ''
            numberHeadingName = ''
            numberHeadingNum = ''
            
            
            headingText = majorHeading
            if majorHeading.lower().rstrip().endswith('act') and alldigits(majh.groups()[1]):
                headingText = '|'+majorHeading+'|'
            accruedLines.append( 'SUMMARY ~*'+headingText+'*~')
            
            casesToHeadings[minorHeading] = ('', [h for h in [currentLecture, majorHeading] if len(h) > 0])
            
            
            continue
        
        
        
        minh = re.match(r"\<p\>([^<]+(\<i\>)?[^<]*(\<\/i\>)?[^<]*)\<\/p\>", line)
        if minh and len(minh.groups()[0])>0:
            if len(currentSubjectCaseList) >0:
                accruedLines.append( '/ -->--' + (' - '.join([ '|'+name+'|' for (name, citation) in currentSubjectCaseList]) ))
                #print >> sys.stderr, ' *** Printing cases: '+accruedLines[-1]
                currentSubjectCaseList = []

            minorHeading = tit(minh.groups()[0])
            lectureHeadings.append(minorHeading)
            print >> sys.stderr, '\n\nMatched minor heading: '+line+' - found "'+minorHeading+'".'
            
            numberHeadingName = ''
            numberHeadingNum = ''
            
            if ''== majorHeading:
                #print >> sys.stderr, "No major heading, so starting new SUMMARY block"
                accruedLines.append( 'SUMMARY ~*' +minorHeading+'*~')
            else:
                print sys.stderr, 'minorHeading was "'+minorHeading+'", majorHeading was "'+majorHeading+'".'
                accruedLines.append( '/ *' +minorHeading+'*')
                
                #print >> sys.stderr, "Below a major heading, adding as '<cr>/' block"
                
            casesToHeadings[minorHeading] = ('', [h for h in [currentLecture, majorHeading, minorHeading] if len(h) > 0])
            
                
            continue
            
        numh = re.match(r'\<p\>\(([A-Za-z0-9]{1})\) ([\w ]+)\<\/p\>', line)
        if numh:
            if len(currentSubjectCaseList) >0:
                accruedLines.append( '/ -->--' + (' - '.join([ '|'+name+'|' for (name, citation) in currentSubjectCaseList]) ))
                #print >> sys.stderr, ' *** Printing cases: '+accruedLines[-1]
                currentSubjectCaseList = []            
            numberHeadingNum = numh.groups()[0]
            numberHeadingName = numh.groups()[1]
            lectureHeadings.append('('+numberHeadingNum+') '+numberHeadingName)
            
            accruedLines.append( '/ *(' +numberHeadingNum+')* ' +numberHeadingName )
            
            continue

        casen = re.match(r'\<p\>\<i\>([^<[]+)(\<\/i\>)?[ ]*([[(]{1}\d{4}[)\]]{1}[^<]+)(\<\/i\>)?\<\/p\>', line)
        if casen:
            caseName = casen.groups()[0].lstrip().rstrip().replace('.','').replace('"','')
            citation = casen.groups()[2].lstrip().rstrip().replace('.','').replace('"','')
            #print >> sys.stderr, ' *** Matched case "'+caseName+'" with citation "'+citation+'", currentSubjectCaseList: "'+repr(currentSubjectCaseList)+'".'
            
            cases.append((caseName,citation))
            currentSubjectCaseList.append((caseName,citation))
            casesToHeadings[caseName] = (citation, [h for h in [currentLecture, majorHeading, minorHeading, numberHeadingName] if len(h) > 0])
            
            continue
            
        if re.search(r'\-\-endtoc\-\-', line, re.IGNORECASE ):
            #print >> sys.stderr, 'Done consuming ToC'
            consumingToC = False   
        
            if len(currentSubjectCaseList) >0:
                accruedLines.append( '/ -->--' + (' - '.join([ '|'+name+'|' for (name, citation) in currentSubjectCaseList]) ))
                #print >> sys.stderr, ' *** Printing cases: '+accruedLines[-1]
                currentSubjectCaseList = []
            continue
            accruedLines.append('#End TOC\n\n\n\n')
        
            continue
        
        print >> sys.stderr, '! The current line in the ToC was not consumed: "'+line.rstrip()+'"'
            
        
    else:
        #In body...
        #########################

        types = {'overview':'overview',
                 'detail': 'detail',
                 'details': 'detail',
                 '<i>acloserlook</i>': 'closerlook',
                 'explanation': 'explanation',
                 'discussion': 'discussion'}
                 
                 
        
        matched = False
        for t in types:
            if line.replace(' ','').lower().startswith('<p><b>'+t+'</b></p>'):
                currentParaType = types[t]
                l = line.rstrip().lstrip('<p><b>').rstrip('</b></p>').lstrip('<i>').rstrip('</i>')
                accruedLines.append('SUMMARY ~*'+l+'*~')
                atLeastOneSummaryTagAdded = True
                potentialConcept = ''
                matched = True
        
        if matched:
            continue
            
        #Now try to get case name.
        #caseConceptOrStatuteHeading = re.match(r'\<p\>\<b\>\<i\>([^<]+)\<\/i\>\<\/b\>\<\/p\>', line)
        caseConceptOrStatuteHeading = re.match(r'\<p\>\<b\>\<i\>([^<]+)(\<\/i\>)?.*?(\<\/i\>)?\<\/b\>\<\/p\>', line)
        if caseConceptOrStatuteHeading:
            potentialConcept = ''
            text = caseConceptOrStatuteHeading.groups()[0]
            currentParaType = ''
            
            text[:-5]
            case = re.match(r'([^\<]+?)\((\d{4})\)', text)
            if case:
                n = case.groups()[0].rstrip().replace('.','').replace('"','')
                y = case.groups()[1]
                if n not in casesToHeadings:
                    suggs = difflib.get_close_matches(n, casesToHeadings.keys(), 1)
                    print >> sys.stderr, '!!! No match found for case "'+n+'" in cases seen so far. Suggestions are: "'+ (', '.join(suggs))+'.'
                    if len(suggs)>0:
                        n = suggs[0]
                
                
                if len(currentSetOfTags)>0:
                    print >> sys.stderr, ' *** Previous card had tags: "'+repr(currentSetOfTags)+'", adding FLAGS element.'
                    #Disgorge the tags to the previous card...
                    accruedLines.append('FLAGS '+ ('; '.join(currentSetOfTags)))
                currentSetOfTags = []

                
                print >> sys.stderr, ' *** Making new card for case: "'+n+'"'
                accruedLines.append('\n\n\n')
                
                
                i = 0
                while n in namesUsed and i<10:
                    n += '.'
                    i += 1
                    
                namesUsed.append(n)
                accruedLines.append('NAME '+n)
                atLeastOneSummaryTagAdded = False
                if n in casesToHeadings:
                    (citation, cats) = casesToHeadings[n]
                    accruedLines.append('CITATION '+n+' '+citation)
                    accruedLines.append('CATEGORY '+('; '.join(cats)))
                    print >> sys.stderr, '$$$$$$$$$$$$ for case "'+n+'", added categories: "'+repr(cats)+'".\n\n'
                #accruedLines.append('YEAR '+y)
            else:
                print >> sys.stderr, '!!! Line "'+line.rstrip()+'" wasn\'t a casename, will make a concept card...'

                if len(currentSetOfTags)>0:
                    print >> sys.stderr, ' *** Previous card had tags: "'+repr(currentSetOfTags)+'", adding FLAGS element.'
                    #Disgorge the tags to the previous card...
                    accruedLines.append('FLAGS '+ ('; '.join(currentSetOfTags)))
                currentSetOfTags = []


                accruedLines.append('\n\n\n')
                
                i = 0
                while text in namesUsed and i<10:
                    text += '.'
                    i += 1
                namesUsed.append(text)

                accruedLines.append('NAME '+text)
                accruedLines.append('TYPE Concept')
                
                if text in casesToHeadings:
                    #may nevertheless have categories...
                    (citation, cats) = casesToHeadings[text]
                    accruedLines.append('CATEGORY '+('; '.join(cats)))
                    print >> sys.stderr,' @@@@@@ For non-case "'+text+'", found categories "'+repr(cats)+'".'
                    
                else:
                    accruedLines.append('CATEGORY '+currentLecture)
                accruedLines.append('SUMMARY ~*'+text+'*~')
                
            
            continue
        
        
        
        l = tit(line.lstrip('<p>').rstrip().rstrip('</p>').rstrip().lstrip().lower())
        if len(l) < 70:
            print >> sys.stderr, ' *** Encountered a short para: "'+l+'".'
            
            if l in ['Introduction','Conclusion']:
                print >> sys.stderr, ' *** *** and made it a new card.'


                if len(currentSetOfTags)>0:
                    print >> sys.stderr, ' *** Previous card had tags: "'+repr(currentSetOfTags)+'", adding FLAGS element.'
                    #Disgorge the tags to the previous card...
                    accruedLines.append('FLAGS '+ ('; '.join(currentSetOfTags)))
                currentSetOfTags = []

                
                accruedLines.append('\n\n\n')
                accruedLines.append('NAME '+ currentLecture + ' - '+ l)
                accruedLines.append('TYPE Concept')
                accruedLines.append('CATEGORY '+currentLecture)
                accruedLines.append('SUMMARY ~*'+l+'*~')
                currentParaType = ''
            elif l in lectureHeadings:
                print >> sys.stderr, '*** *** it was a heading. If the next para is not a case, we\'ll treat it as a new concept.' 
                potentialConcept = l
                
        else:
            
            lCleaned = line.rstrip().lstrip('<p>').rstrip('</p>').lstrip('<i>').rstrip('</i>')
            if potentialConcept != '':
                print >> sys.stderr, ' >>>>> Encountered a long para, and previously saw a potentialConcept ("'+potentialConcept+'")'
                accruedLines.append('\n\n\n')

                i = 0
                while potentialConcept in namesUsed and i<10:
                    potentialConcept += '.'
                    i += 1
                
                namesUsed.append(potentialConcept)

                if len(currentSetOfTags)>0:
                    print >> sys.stderr, ' *** Previous card had tags: "'+repr(currentSetOfTags)+'", adding FLAGS element.'
                    #Disgorge the tags to the previous card...
                    accruedLines.append('FLAGS '+ ('; '.join(currentSetOfTags)))
                currentSetOfTags = []

                
                accruedLines.append('NAME '+ potentialConcept)
                accruedLines.append('TYPE Concept')
                
                if potentialConcept in casesToHeadings:
                    #may nevertheless have categories...
                    (citation, cats) = casesToHeadings[potentialConcept]
                    accruedLines.append('CATEGORY '+('; '.join(cats)))
                    print >> sys.stderr,' @!@!@!@ For potentialConcept "'+potentialConcept+'", found categories "'+repr(cats)+'".'
                    
                else:
                    accruedLines.append('CATEGORY '+currentLecture)
                
                
                accruedLines.append('SUMMARY ~*'+potentialConcept+'*~') 
                accruedLines.append('/->-'+lCleaned)
                potentialConcept = ''
                currentParaType = ''
                
            else:
                print >> sys.stderr, ' *** Encountered a long para without a protentialConcept treating as a "'+currentParaType+'".'
                if not atLeastOneSummaryTagAdded:
                    accruedLines.append('SUMMARY ~*Overview*~')
                    atLeastOneSummaryTagAdded = True
                    
                notables = ['Denning','Diplock','Atkin','Treitel','McKendrick', 'Bingham', 'Arden', 'Hoffman', 'Steyn', 'Bramwell']
                notableSuffixes = [' MR', ' CJ',' LJ',' J']
                for notable in notables:
                    if notable in lCleaned and notable not in currentSetOfTags:
                        currentSetOfTags.append(notable)
                        madeReplacement = False
                        for suffix in notableSuffixes:
                            thing = notable+suffix
                            if thing in lCleaned: 
                                madeReplacement = True
                                lCleaned = lCleaned.replace(thing, '*'+thing+'*')
                        
                        if not madeReplacement:
                            lCleaned = lCleaned.replace(notable, '*'+notable+'*')
                                
                    
                if currentParaType == 'closerlook':
                    accruedLines.append('/->-_'+ lCleaned+'_')
                else:
                    accruedLines.append('/->-'+lCleaned )
            
        
if len(accruedLines) > 0:
    flushAccruedLinesToFile()
        

