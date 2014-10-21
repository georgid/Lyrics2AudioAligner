# -*- coding: utf-8 -*-
'''
contains a class
Created on Mar 3, 2014

@author: joro
'''


import os
import sys
import imp
parentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0]) ), os.path.pardir)) 
# /Users/joro/Documents/Phd/UPF/voxforge/myScripts/utilsLyrics

utils_ = imp.load_source('Utils', os.path.join(parentDir, 'utilsLyrics')  )



import codecs

import glob
from SymbTrParser import SymbTrParser
from Phonetizer import Phonetizer
from Phoneme import Phoneme
# from utils.Utils import writeListToTextFile


# 
# COMPOSITION_NAME = 'muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik'
# COMPOSITION_NAME = 'huseyni--sarki--turkaksagi--hicran_oku--sevki_bey'
# 
# PATH_TEST_DATASET='/Users/joro/Documents/Phd/UPF/turkish-makam-lyrics-2-audio-test-data/'
# PATH_TEST_DATASET = '/Volumes/IZOTOPE/sertan_sarki/'

class MakamScore():
    '''
    classdocs
    '''


##################################################################################

    def __init__(self, pathToSymbTrFile, pathToSectionTsvFile):
        '''
        Constructor
        
        '''
        self.compositionName = os.path.splitext(pathToSymbTrFile)[0]
        
        ''' lyrics divided into sectons.
        # e.g. "nakarat" : [ word1 word2 ] '''
        self.sectionToLyricsMap = []
        
        self._loadSectionsAndSyllablesFromSymbTr(pathToSymbTrFile, pathToSectionTsvFile)
        
        
        # pats to individual ..txt lyrics files. 
        self.pathsTolyricSectionFiles = []
        
      
  ##################################################################################
    '''
    parses symbTr file. Reads lyrics, 
    reads section names
    groups together section names and lyrics 
    '''
    def _loadSectionsAndSyllablesFromSymbTr(self, pathToSymbTrFile, pathToSectionTsvFile):
        symbTrParser = SymbTrParser(pathToSymbTrFile)
       
        symbTrParser._loadSectionBoundaries(pathToSectionTsvFile)
        
        wordsAllSections = symbTrParser.syllables2Words()
        
        # for each section part
        for currSectionBoundary,currSectionLyrics in zip(symbTrParser.sectionboundaries, wordsAllSections):
            tupleSectionNameAndLyrics =  currSectionBoundary[0], currSectionLyrics  
            self.sectionToLyricsMap.append(tupleSectionNameAndLyrics)
            
    def getLyricsForSection(self,sectionNumber):
        return self.sectionToLyricsMap[sectionNumber][1]
 
  
   ##################################################################################
    def printSectionsAndLyrics(self):
        '''
        utility method to print all lyrics that are read from symbTr
        '''
        for currSection in self.sectionToLyricsMap:
    
            print '\n' + str(currSection[0]) + ':'
            
            for word in  currSection[1]:
                print word.__str__().encode('utf-8','replace')
    #             string_for_output = currSection[1].encode('utf-8','replace')
        

    def serializePhonemesForSection(self, whichSection, outputFileName):
        '''
        list of all phonemes. print to file @param outputFileName
        '''    
        words = self.getLyricsForSection(whichSection)
        
        listPhonemes =  []
        phonemeSil = Phoneme("sil"); phonemeSil.setDuration('1')
        listPhonemes.append(phonemeSil)
        
        for word_ in words:
            for syllable_ in word_.syllables:
                syllable_.expandToPhonemes()
                listPhonemes.extend(syllable_.phonemes )
        
        listPhonemes.append(phonemeSil)    

        
        utils_.writeListToTextFile(listPhonemes, None,  outputFileName )
        return listPhonemes
    
    def _calcPhonemeDurations(self, whichSection):
        words = self.getLyricsForSection(whichSection)
        for word_ in words:
            for syllable in word_.syllables:
                syllable.calcPhonemeDurations()
        
        
    def getIndicesPhonemes(self, whichSection ):
        '''
        getIndices of word begins in phoneme list expanded with states used in DTW alignment
        '''
        words = self.getLyricsForSection(whichSection)
        
#       consists of tuples startIndices and word identities
        indicesBeginWords = []
        
        NUMSTATES_SIL = 3
        NUMSTATES_PHONEME = 3
        
        # start with sil, +1 to satisfy indexing in matlab
        currBeginIndex = NUMSTATES_SIL + 1
         
        
        for word_ in words:
            
#             indicesBeginWords.append( (currBeginIndex, word_.text) )
            indicesBeginWords.append(currBeginIndex )
            # sp has one state only
            currBeginIndex  = currBeginIndex + NUMSTATES_PHONEME * (word_.getNumPhonemes() - 1) + 1
        # last word sil
        indicesBeginWords.append(currBeginIndex )
        
        return  indicesBeginWords
    
    
    
    
              
            
    
    def getIndicesPhonemes_durations(self, whichSection):
        ''' same as getIndicesPhonemes but with durations.
        Assume phoneme.Durations are calculated.  
        '''
        
        self._calcPhonemeDurations(whichSection)
        
        words = self.getLyricsForSection(whichSection)
        
#       consists of tuples startIndices and word identities
        indicesBeginWords = []
        
        NUMSTATES_SIL = 3
        NUMSTATES_PHONEME = 3
        
        currBeginIndex = NUMSTATES_SIL + 1
         
        
        for word_ in words:
            
#             indicesBeginWords.append( (currBeginIndex, word_.text) )
            indicesBeginWords.append( currBeginIndex )

            wordTotalDur = 0 
            for syllable_ in word_.syllables:
                for phoneme_ in syllable_.phonemes:
                    currDuration = NUMSTATES_PHONEME * phoneme_.getDuration()
                    wordTotalDur = wordTotalDur + currDuration  
            
            currBeginIndex  = currBeginIndex + wordTotalDur
        
        # last word sil
        indicesBeginWords.append( currBeginIndex )

        
        return  indicesBeginWords
 
 
#        end of class

           
                    
def serializeIndices( makamScore, whichSection, withDurations, URI_IndicesFile):
    '''
    helper method
    '''
    if withDurations:
           indices =  makamScore.getIndicesPhonemes_durations(whichSection)
             
    else:
 
           indices = makamScore.getIndicesPhonemes(whichSection)
        
    utils_.writeListToTextFile(indices, None,  URI_IndicesFile ) 


        
def parseScoreAndSerialize(pathToComposition, whichSection, withDurations):
        '''
        Main method for  DTW in matlab
        prints sequence of phonemes, sequence of durarions. indices of word start positions 
        '''
        
        os.chdir(pathToComposition)
        pathTotxt = os.path.join(pathToComposition, glob.glob("*.txt")[0])
        pathToSectionTsv =  os.path.join(pathToComposition, glob.glob("*.tsv")[0])
        makamScore = MakamScore(pathTotxt, pathToSectionTsv )
        
        # 1. phoneme IDs
        listPhonemes = makamScore.serializePhonemesForSection(whichSection, '/tmp/test.phn')
        listDurations = []
        
        # 2. phoneme Durations
        makamScore._calcPhonemeDurations(whichSection)

        for phoneme_ in listPhonemes :
            listDurations.append(phoneme_.duration)
        utils_.writeListToTextFile(listDurations, None, '/tmp/test.durations')
        
        # 3. indices
        serializeIndices(makamScore, whichSection, withDurations, '/tmp/test.indices')
        
#       just for information   
        makamScore.printSectionsAndLyrics()

                                 
         


    
     ##################################################################################
def main(pathToComposition):
        
        os.chdir(pathToComposition)
        pathTotxt = os.path.join(pathToComposition, glob.glob("*.txt")[0])
        pathToSectionTsv =  os.path.join(pathToComposition, glob.glob("*.sections.tsv")[0])
        
        makamScore = MakamScore(pathTotxt, pathToSectionTsv )
        
        makamScore.printSectionsAndLyrics()
        # is this needed? 
        
        
def mainDTWMatlab():
        if len(sys.argv) != 4:
            print ("usage: {} <dir of symbtTr.txt and symbTr.tsv> <whichSectionNumber> <hasDurations?>".format(sys.argv[0]) )
            sys.exit();

        parseScoreAndSerialize(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))        
      

          
             
if __name__ == '__main__':

        # only for unit testing purposes
        
        print "in Makam Score"
        
        if len(sys.argv) != 2:
            print ("usage: {} <path to symbtTr.txt and symbTr.tsv>".format(sys.argv[0]) )
            sys.exit();
          
        main(sys.argv[1])
          
      
         