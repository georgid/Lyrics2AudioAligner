# -*- coding: utf-8 -*-
'''
Created on Mar 3, 2014

@author: joro
'''
import os
import codecs

import glob
from SymbTrParser import SymbTrParser

COMPOSITION_NAME = 'muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik'
COMPOSITION_NAME = 'huseyni--sarki--turkaksagi--hicran_oku--sevki_bey'

PATH_TEST_DATASET='/Users/joro/Documents/Phd/UPF/turkish-makam-lyrics-2-audio-test-data/'
PATH_TEST_DATASET = '/Volumes/IZOTOPE/sertan_sarki/'

class MakamScore():
    '''
    classdocs
    '''

    #class const variable. order is important
    # assumes the forth is melodic repetition of second but with different melody
    sectionNamesSequence = ["zemin","nakarat", "meyan","2nakarat"]




    def __init__(self, pathToSymbTrFile, pathToSectionTsvFile):
        '''
        Constructor
        
        '''
        self.compositionName = os.path.splitext(pathToSymbTrFile)[0]
        
        # lyrics divided by sections
        
        self.sectionNames = []
        self._loadSectionsAndLyricsFromSymbTr(pathToSymbTrFile, pathToSectionTsvFile)
        
        
        self.sectionLyrics = self.symbTrParser.sectionLyrics
        # dict
        self.sectionLyricsDict = {MakamScore.sectionNamesSequence[0]:"", MakamScore.sectionNamesSequence[1]:"", MakamScore.sectionNamesSequence[2]:"", MakamScore.sectionNamesSequence[3]:""}
        
        #self.loadLyricsForSections(pathToSymbTrFile)
        
        # pats to individual lyrics files
        self.pathsTolyricSectionFiles = []
        
      
      
    def _loadSectionsAndLyricsFromSymbTr(self, pathToSymbTrFile, pathToSectionTsvFile):
        self.symbTrParser = SymbTrParser(pathToSymbTrFile, pathToSectionTsvFile)
       
        self.symbTrParser.syllablesToWords()
       
        for sectionBoundary in self.symbTrParser.sectionboundaries:
            self.sectionNames.append(sectionBoundary[0])  

        
    '''    
    # @deprecated 
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
                
             
#                 self.sectionLyricsDict.append(lyrics[0])
#                 self.sectionLyricsDict.append(lyrics[1])
#                 self.sectionLyricsDict.append(lyrics[2])
#                 self.sectionLyricsDict.append(lyrics[3])
            
    '''
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
   
    def printSectionsAndLyrics(self):
        for i in range(len(self.sectionNames)):

            print str(self.sectionNames[i]) + ': \n' 

            string_for_output = self.sectionLyrics[i].encode('utf-8','replace')
            print  string_for_output + '  \n\n'
        
        
            
if __name__ == '__main__':

        # only for unit testing purposes
        
        print "in Makam Score"
        
        pathToComposition = os.path.join(PATH_TEST_DATASET, COMPOSITION_NAME)
        os.chdir(pathToComposition)
        pathTotxt = os.path.join(pathToComposition, glob.glob("*.txt")[0])
        pathToSectionTsv =  os.path.join(pathToComposition, glob.glob("*.tsv")[0])
        makamScore = MakamScore(pathTotxt,pathToSectionTsv )
        
        makamScore.printSectionsAndLyrics()
        
#         makamScore.serializeLyricsToFile()
        
