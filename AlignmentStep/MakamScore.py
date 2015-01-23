# -*- coding: utf-8 -*-
'''
contains a class
Created on Mar 3, 2014

@author: joro
'''
import os
import codecs

import glob
from SymbTrParser import SymbTrParser
import sys
# 
# COMPOSITION_NAME = 'muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik'
# COMPOSITION_NAME = 'huseyni--sarki--turkaksagi--hicran_oku--sevki_bey'
# 
# PATH_TEST_DATASET='/Users/joro/Documents/Phd/UPF/turkish-makam-lyrics-2-audio-test-data/'
# PATH_TEST_DATASET = '/Volumes/IZOTOPE/sertan_sarki/'



parentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0]) ), os.path.pardir)) 
pathUtils = os.path.join(parentDir, 'utilsLyrics')

sys.path.append(pathUtils )


class MakamScore():
    '''
    classdocs
    '''

    #class const variable. order is important
    # assumes the forth is melodic repetition of second but with different melody



##################################################################################

    def __init__(self, pathToSymbTrFile, pathToSectionTsvFile):
        '''
        Constructor
        
        '''
        self.compositionName = os.path.splitext(pathToSymbTrFile)[0]
        
        # lyrics divided by sections
        
        self.sectionToLyricsMap = []
        self._loadSectionsAndLyricsFromSymbTr(pathToSymbTrFile, pathToSectionTsvFile)
        
        
        '''
        @deprecated: 
        '''
#         self.sectionLyricsDict = {MakamScore.sectionNamesSequence[0]:"", MakamScore.sectionNamesSequence[1]:"", MakamScore.sectionNamesSequence[2]:"", MakamScore.sectionNamesSequence[3]:""}
        
        #self.loadLyricsForSections(pathToSymbTrFile)
        
        # pats to individual ..txt lyrics files. 
        self.pathsTolyricSectionFiles = []
        
      
  ##################################################################################
    '''
    parses symbTr file. Reads lyrics, 
    reads section names
    groups together section names and lyrics 
    '''
    def _loadSectionsAndLyricsFromSymbTr(self, pathToSymbTrFile, pathToSectionTsvFile):
        symbTrParser = SymbTrParser(pathToSymbTrFile, pathToSectionTsvFile)
       
        symbTrParser.syllablesToLyrics()
        
        # for each section part
        for currSectionBoundary,currSectionLyrics in zip(symbTrParser.sectionboundaries, symbTrParser.sectionLyrics):
            tupleSectionNameAndLyrics =  currSectionBoundary[0], currSectionLyrics  
            self.sectionToLyricsMap.append(tupleSectionNameAndLyrics)
 
    ##################################################################################
    
    '''    
    @deprecated with old self.sectionLyricsDict
             # NOTE: Each section shoud be in a new line. Ideally copy paste from score.pdf to a textFile.
    # assigns strophes(lyrical lines) to sections:  
    # assumes strophes are 4 in pathTo.txtdivided file. Checks repeating labels in pathToLinkedSectionsFile   
    '''
    def loadLyricsForSections(self, pathToTxtTurFile):
            txtTurFileHandle =  codecs.open(pathToTxtTurFile, 'r', 'utf-8')

            lyrics = txtTurFileHandle.readlines()
            if len(lyrics) != 4:
                print "num of lyrics lines in file % is not 4"
                return
            else:
                # put in dictionary the lyrics
                for i in range(4):
                    self.sectionLyricsDict[MakamScore.sectionNamesSequence[i]]=lyrics[i]
                
             
     ##################################################################################
       
    '''
    @deprecated:  with old self.sectionLyricsDict. TODO: rewrite
    put each section in a separate .txtTur file
    An optional method. Now doit.alignOneRecroding() does not need to print lyrics txtTur for each section 
    '''        
    def serializeLyricsToFile(self):
        for key, value in self.sectionLyricsDict.iteritems():
            # form name
            pathTolyricSectionFile=self.compositionName + "_" + key + ".txtTur"
            
            #write path in object variables
            self.pathsTolyricSectionFiles.append( pathTolyricSectionFile)
            
            outputFileHandle = codecs.open(pathTolyricSectionFile, 'w', 'utf-8')
            outputFileHandle.write(value)
            outputFileHandle.close()

            print "file %s written", (pathTolyricSectionFile)

   ##################################################################################
    '''
    utility method to print class fields
    '''
    def printSectionsAndLyrics(self):
        for currSection in self.sectionToLyricsMap:

            print str(currSection[0]) + ': \n' 

            string_for_output = currSection[1].encode('utf-8','replace')
            print  string_for_output + '  \n\n'
        
        
    def getLyricsForSection(self,sectionNumber):
        '''
        convenience getter
        '''
        #python indexing starts from zero
        sectionNumber = sectionNumber - 1
        return self.sectionToLyricsMap[sectionNumber][1]
    
     ##################################################################################


def loadLyrics(pathToComposition, whichSection):

#     expand phoneme list from transcript
    os.chdir(pathToComposition)
    pathTotxt = os.path.join(pathToComposition, glob.glob("*.txt")[0])
#     pathToSectionTsv = os.path.join(pathToComposition, glob.glob("*.sections.txt")[0])
    pathToSectionTsv =  os.path.join(pathToComposition, glob.glob("*sections.json")[0])
    makamScore = MakamScore(pathTotxt, pathToSectionTsv )
    
    # phoneme IDs
    lyrics = makamScore.getLyricsForSection(whichSection)
    return makamScore 
        
       
if __name__ == '__main__':

        # only for unit testing purposes
        print "in Makam Score"
        
        if len(sys.argv) != 2:
            print ("usage: {} <path to composition> ".format(sys.argv[0]) )
            sys.exit();
        
        lyrics, makamScore = loadLyrics(sys.argv[1], whichSection=1)
