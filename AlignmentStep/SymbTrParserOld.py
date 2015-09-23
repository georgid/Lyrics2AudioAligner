# -*- coding: utf-8 -*-
'''
Created on Mar 10, 2014
 contains a class 
 
@author: joro
'''
import codecs
import os
import sys

parentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0]) ), os.path.pardir)) 
pathUtils = os.path.join(parentDir, 'utilsLyrics') 
# pathUtils = '/Users/joro/Documents/Phd/UPF/voxforge/myScripts/utilsLyrics'

if not pathUtils in sys.path:
    sys.path.append(pathUtils )

from Utilz import  loadTextFile

pathAlignmentDur = os.path.join(parentDir, 'AlignmentDuration')
if not pathAlignmentDur in sys.path:
    sys.path.append(pathAlignmentDur)
from _SymbTrParserBase import _SymbTrParserBase

# utils_ = imp.load_source('Utils', pathUtils  )




'''
Parses lyrics from symbTr v 1.0. Sections from tsv file
TODO: take only section names from tsv file. parse sections from symbTr double spaces 
'''
class SymbTrParserOld(_SymbTrParserBase):
  
    
    def __init__(self, pathToSymbTrFile, pathToSectionFile):
        '''
        Constructor
        '''
        
        _SymbTrParserBase.__init__(self, pathToSymbTrFile, pathToSectionFile)
        
   
   ##################################################################################
     
    '''
    required implementation from _SymbTrBase.  
     approach unaware of syllable-identity. 
    '''
    def _loadSyllables(self, pathToSymbTrFile):
    
        allLines = loadTextFile(pathToSymbTrFile)
        
        # skip first line
        
        for line in allLines[1:]:
            line = line.replace(os.linesep,'') # remove end line in a os-independent way 
            line = line.replace('\r','') 
            
            tokens = line.split("\t")
            
            if len(tokens) == 12:
                    # TUK ZABIVA. 
                    if tokens[11] != '.' and tokens[11] != '. ' and tokens[11] != '.  ' and tokens[11] != 'SAZ' and tokens[11] != 'SAZ ' and tokens[11] != 'SAZ  ' and tokens[11] != u'ARANA\u011eME' and tokens[11] != u'ARANA\u011eME ' and  tokens[11] != u'ARANA\u011eME  ' and  tokens[11] != u'ARANA\\\\u011eME' and  tokens[11] != u'ARANAGME'   :   
        #           note number and syllable
                        text = tokens[11].replace('_',' ')
                        tupleSyllable = int(tokens[0]), text
                    
                        self.listSyllables.append(tupleSyllable)
            
     

       
       
     ##################################################################################
   
    '''
    converts syllables to words using " " at end of syllable from SymbTr 
    at the same time assigns them into sections.
    '''  
    def syllablesToLyrics(self):
        
        indexSyllable = 0
        for currSectionBoundary in self.sectionboundaries:
            
            currEndNoteNumber = currSectionBoundary[2]
            currSectionLyrics = ""
            
        
            while (indexSyllable <= len(self.listSyllables)-1 # sanity check
                    and 
                    self.listSyllables[indexSyllable][0] <= currEndNoteNumber ): # while note number associated with syllable is less than last note number in section 
                        currSectionLyrics = currSectionLyrics + self.listSyllables[indexSyllable][1]
                        indexSyllable += 1
            
            # double empty space marks section end, but we dont use it for now             
            currSectionLyrics = currSectionLyrics.strip()
            # record lyrics
            self.sectionLyrics.append(currSectionLyrics)
        
    

 ##################################################################################

if __name__ == "__main__":
    pathTxt=  '/Users/joro/Documents/Phd/UPF/turkish-makam-lyrics-2-audio-test-data/nihavent--sarki--aksak--bakmiyor_cesm-i--haci_arif_bey/nihavent--sarki--aksak--bakmiyor_cesm-i--haci_arif_bey.txt'
    pathTsv= '/Users/joro/Documents/Phd/UPF/turkish-makam-lyrics-2-audio-test-data/nihavent--sarki--aksak--bakmiyor_cesm-i--haci_arif_bey/nihavent--sarki--aksak--bakmiyor_cesm-i--haci_arif_bey.sections.tsv'
     
    symbTrParser = SymbTrParserOld(pathTxt, pathTsv)
    symbTrParser.syllablesToLyrics()
