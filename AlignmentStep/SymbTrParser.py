# -*- coding: utf-8 -*-
'''
contains SymbTr Parser class 
 
@author: joro
'''
import codecs
import os
import sys
from Word import Word
from Syllable import Syllable
import imp

parentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0]) ), os.path.pardir)) 
pathUtils = os.path.join(parentDir, 'utilsLyrics') 
# pathUtils = '/Users/joro/Documents/Phd/UPF/voxforge/myScripts/utilsLyrics'

# utils_ = imp.load_source('Utils', pathUtils  )

sys.path.append(pathUtils )

from Utilz import  loadTextFile


class SymbTrParser(object):
    '''
    Parses lyrics from symbTr v 1.0 and Sections from tsv file
    a list of syllables is parsed. 
    Then concatenated into words if needed 
    TODO: take only section names from tsv file. parse sections from symbTr double spaces 
    '''
#     16 for 16th note
    MINIMAL_DURATION_UNIT = 16
    
    def __init__(self, pathToSymbTrFile):
        '''
        Constructor
        '''
        # list of Syllable(s)
        self.listSyllables =[]
        self._loadSyllables( pathToSymbTrFile)


        # section boundaries.                 #  triples of sectin name, start note, end note 
        self.sectionboundaries = []
        
        
   
    
   
   
   ##################################################################################
     
    '''
    load syllables from symbTr file. calculate syllable duration from the associated notes 
    '''
    def _loadSyllables(self, pathToSymbTrFile):
             
        allLines = loadTextFile(pathToSymbTrFile)
        
        currSyllable = None
        syllTotalDuration = None
        
        # skip first line. 
        for  i in range( 1, len(allLines) ):
            
            line = allLines[i]
            line = line.replace(os.linesep,'') # remove end line in an os-independent way 
            line = line.replace('\r','') 
            
            tokens = line.split("\t")
            if len(tokens) != 12:
                print "TOKENS ARE 11, no syllable ";  sys.exit()

            currDuration = float(tokens[6]) / float(tokens[7]) * SymbTrParser.MINIMAL_DURATION_UNIT
            currTxtToken = tokens[11]
                
            # no syllalbe
            if  currTxtToken.startswith('.') or currTxtToken.startswith('SAZ') or currTxtToken.startswith(u'ARANA\u011eME') or currTxtToken.startswith(u'ARANAGME')  :
                 continue
            
            # start of a new syllalbe
            elif currTxtToken != '':

                if not(currSyllable is None) and not(syllTotalDuration is None):
                # save last syllable and duration 
                     currSyllable.duration = syllTotalDuration
                     self.listSyllables.append(currSyllable)
                
                # init next syllable. 
                currSyllable = Syllable(tokens[11], tokens[0])
                # init duration.
                syllTotalDuration = currDuration
        
            # no lyrics at note, so still  same syllable notes
            else:
                syllTotalDuration = syllTotalDuration + currDuration
            
        # store last
        currSyllable.duration = syllTotalDuration
        self.listSyllables.append(currSyllable)
            
            
             
              
            
                    
#                         self.listSyllables.append(tupleSyllable)
            
     
   ##################################################################################

    def _loadSectionBoundaries(self, pathToTsvFile):
            
            allLines = loadTextFile(pathToTsvFile)

            for line in allLines[1:]:
                #  triples of sectin name, start note number, end note number 
                tokens = line.strip().split("\t")
                tmpTriplet = tokens[0], int(tokens[1]), int(tokens[2]) 
                self.sectionboundaries.append(tmpTriplet)
       
       
     ##################################################################################
   
     
     
    def syllables2Words(self): 
        """
        construct words from syllables for all  sections
        """  
        wordsAllSections = []
        words = []
              
        for currSectionBoundary in self.sectionboundaries:
            
            # double empty space marks section end, but we dont use it for now             
            words = self.syllable2WordOneSection(currSectionBoundary[1], currSectionBoundary[2])
            
            # store lyrics
            wordsAllSections.append(words)
            
        return wordsAllSections
          

# begin index does not update, because no change in aranagme. 
    def syllable2WordOneSection(self, startNoteNumber, endNoteNumber):
        """
             combine syllables into listWords. use Word and Syllable classes. 
                for one section only .
                add syllables until noteNumber of current Syllable reaches  @param endNoteNumber 
            @param beginIndex - beginning current index syllable
        """
        syllablesInCurrWord  = []
        listWords = []
        
        beginIndex = self._findSyllableIndex(startNoteNumber)
        # wrong noteNumber for section begin or no lyrics in section
        if (beginIndex == -1):
            return listWords
        
        
        while (beginIndex <= len(self.listSyllables)-1 # sanity check
                    and self.listSyllables[beginIndex].noteNum <= endNoteNumber ): # while note number associated with syllable is less than last note number in section 
                    
                        currSyllable = self.listSyllables[beginIndex]
                        # construct new word at whitespace
                        if currSyllable.text[-1].isspace():
                            
                            # dont need whitespaces in sllables
                            currSyllable.text = currSyllable.text.rstrip()
                            
                            currSyllable.setHasShortPauseAtEnd(True)
                            
                            syllablesInCurrWord.append(currSyllable)
                        
                            word = Word(syllablesInCurrWord)
                            listWords.append(word)
                            
                            #restart counting
                            syllablesInCurrWord = []

                        else:
                            syllablesInCurrWord.append(currSyllable)
                            
                            
                        beginIndex = beginIndex + 1
                        
        return listWords
        
    def _findSyllableIndex(self, noteNumberQuery):
        '''
        find which syllable has  given note number. use bunary search
        '''
        lo = 0
        high = len(self.listSyllables)
        
        while lo<high:
            mid = (lo+high)//2
            noteNum = self.listSyllables[mid].noteNum
            if noteNumberQuery < noteNum:
                high = mid
            elif noteNumberQuery > noteNum:
                lo = mid + 1
            else:
                return mid
        # no such number in list 
      
        return -1
             
            
        
        
# begin index does not update, because no change in aranagme. 
    def syllable2WordOneSectionOld(self, beginIndex, endNoteNumber):
        """    
            @deprecated: 
             combine syllables into listWords. use Word and Syllable classes. 
                for one section only .
                add syllables until noteNumber of current Syllable reaches  @param endNoteNumber 
            @param beginIndex - beginning current index syllable
            @return beginIndex - final current index syllable
        """
        syllablesInCurrWord  = []
        listWords = []
        
        beginSyllable = self.listSyllables[beginIndex]
        while (beginIndex <= len(self.listSyllables)-1 # sanity check
                    and beginSyllable.noteNum <= endNoteNumber ): # while note number associated with syllable is less than last note number in section 
                    
                        currSyllable = self.listSyllables[beginIndex]
    
                            
                        
                        # construct new word at whitespace
                        if currSyllable.text[-1].isspace():
                            
                            # dont need whitespaces in sllables
                            currSyllable.text = currSyllable.text.rstrip()
                            syllablesInCurrWord.append(currSyllable)
                        
                            word = Word(syllablesInCurrWord)
                            listWords.append(word)
                            
                            #restart counting
                            syllablesInCurrWord = []

                        else:
                            syllablesInCurrWord.append(currSyllable)
                            
                        beginIndex = beginIndex + 1
                        
        return listWords, beginIndex
        
     

    

#################################################################################

if __name__ == "__main__":
    pathTxt=  '/Volumes/IZOTOPE/sertan_sarki/muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik/muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik.txt'
    pathTsv= '/Volumes/IZOTOPE/sertan_sarki/muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik/muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik.sections.tsv'    
    
    pathTxt=  '/Users/joro/Documents/Phd/UPF/adaptation_data_soloVoice/ISTANBUL/safiye/segah--sarki--curcuna--olmaz_ilac--haci_arif_bey.txt'
    pathTsv= '/Users/joro/Documents/Phd/UPF/adaptation_data_soloVoice/segah--sarki--curcuna--olmaz_ilac--haci_arif_bey/segah--sarki--curcuna--olmaz_ilac--haci_arif_bey.sections.tsv'
    
    symbTrParser = SymbTrParser(pathTxt)
    symbTrParser._loadSectionBoundaries( pathTsv)
    
#     symbTrParser.syllablesToWords()
    
    
    wordsAllSections = symbTrParser.syllables2Words()
    print "DONE. otivam da si miq zybite"
