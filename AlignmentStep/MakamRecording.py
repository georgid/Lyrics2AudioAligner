# -*- coding: utf-8 -*-
'''
Created on Mar 3, 2014

@author: joro
'''
from MakamScore import MakamScore
import subprocess
import os

pathToSox = "/usr/local/bin/sox"
    
class MakamRecording:

    '''
    classdocs
    '''
    '''
    The size of self.sectionNames, self.beginTs, self.endTs, self.sectionIndices should be same
    
    '''

        
    def __init__(self, makamScore, pathToAudioFile, pathToLinkedSectionsFile):
       
       # the score of the piece
        self.makamScore = makamScore
        
        self.pathToAudiofile = pathToAudioFile
        self.pathToDividedAudioFiles= []
        
        
        # section timestamps,
        self.beginTs=[]
        self.endTs = []  
        
        self.sectionNamesSequence = []
        
        self.sectionIndices = []
        
        self._loadsectionTimeStamps( pathToLinkedSectionsFile)

        '''
        assigns a pointer (number) to each section Name from score
        '''
        
    
        return
    

    ##################################################################################

    ''' 
    @deprecated: 
    Handles the Division into sections. If 4 section names given for MakamScore, assumes the forth (nakarat) is melodic repetition of second but with different lyrics (2nakarat)  
    
    '''
    def assignSectionLyrics(self):
        
       # TODO: write cheker for score 
        
        flagMeyan = False

       # check section names and get lyrics from score. use index to map to Ts index
        for index in range(len(self.sectionNamesSequence)):
            
            
            currSectionName = self.sectionNamesSequence[index]
            # remove 2 or 3 suffix
            if str(currSectionName).endswith('2') or str(currSectionName).endswith('3'):
                currSectionName = currSectionName[0:-1]
            # if meyan is gone, put 2 to signify  it is second nakarat (with different lyrics). Assumption: there is no third verse and third nakarat
            if flagMeyan and currSectionName==MakamScore.sectionNamesSequence[1] and len(MakamScore.sectionNamesSequence)==4 :
                currSectionName='2' + currSectionName    
                
            if currSectionName in MakamScore.sectionNamesSequence:
                self.sectionIndices[index] =   self.makamScore.sectionLyricsDict[currSectionName]
                if currSectionName == MakamScore.sectionNamesSequence[2]:
                    flagMeyan = True
            else:
                print "unknown section name: %s " ,  (currSectionName)
                self.sectionIndices[index] = ""
                
            
        return
            
        
        
       ##################################################################################
      
    ## loads timestamps from file .sectionAnno
    def _loadsectionTimeStamps(self, pathToLinkedSectionsFile):
        
        # U means cross-platform  end-line character
        sectionsFileHandle = open(pathToLinkedSectionsFile, 'rU')
        
        # skip first line
#         next(sectionsFileHandle)
        
        for line in sectionsFileHandle:
            tokens =  line.split()
            
            self.beginTs.append(tokens[0])
            self.endTs.append(tokens[1])
            self.sectionNamesSequence.append(tokens[2])
            
            # WORKAROUND for section mapping. read mapping index from 4th field in .annotations file
            self.sectionIndices.append(int(tokens[3]))
            
        # divide into columns
        
        sectionsFileHandle.close()
        
        return
    
       ##################################################################################

        # for given audio and ts divide audio into audio segments
    def divideAudio(self):
            
            for i in range(len(self.sectionNamesSequence)):
                
                filePathAndExt = os.path.splitext(self.pathToAudiofile)
                filePathDividedAudio = filePathAndExt[0] + '_' + self.sectionNamesSequence[i] + '_from_' + self.beginTs[i] + '_to_' + self.endTs[i] + filePathAndExt[1] 
                
                self.pathToDividedAudioFiles.append(filePathDividedAudio)
                # make sure  sox (sox.sourceforge.net) is installed and call it  here with subprocess
                sectionDuration = float(self.endTs[i])-float(self.beginTs[i])
                self.pathToAudiofile = '/Users/joro/Documents/Phd/UPF/turkish-makam-lyrics-2-audio-test-data/muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde.wav'
                pipe = subprocess.Popen([pathToSox, self.pathToAudiofile, filePathDividedAudio, 'trim', self.beginTs[i], str(sectionDuration)   ])
               
            return
    
    
if __name__ == '__main__':
        # only for unit testing purposes
        print "in Makam Recording"
 
        