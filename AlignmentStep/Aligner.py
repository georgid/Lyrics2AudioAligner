'''
Created on Mar 17, 2014

@author: joro
'''
import os
import subprocess
from utils.Utils import mlf2WordAndTsList, writeListToTextFile


PHONEME_ALIGNED_SUFFIX= ".phonemeAligned"
PATH_TO_ALIGNMENT_TOOL = os.path.abspath('doForceAligment.sh')
WORD_ALIGNED_SUFFIX= ".wordAligned"



class Aligner():
    '''
    classdocs
    '''


    def __init__(self, pathToAudioFile, lyrics):
        self.pathToAudioFile = pathToAudioFile
        self.lyrics = lyrics
    
     ##################################################################################

    '''
    only one audio file and lyrics provided
    @param timeShift: add to start of timstamps (needed tog get real audio timestamp if audio is part of a bigger recording)
    '''
    
    def alignAudio(self, timeShift, outputHTKPhoneAligned =''):
    #     lyrics = loadTextFile(pathToLyricsFile)
    
    
        baseNameAudioFile = os.path.splitext(self.pathToAudioFile)[0]
        
        if outputHTKPhoneAligned =='':
            outputHTKPhoneAligned = baseNameAudioFile + PHONEME_ALIGNED_SUFFIX
        pipe = subprocess.Popen([PATH_TO_ALIGNMENT_TOOL, baseNameAudioFile , self.lyrics, outputHTKPhoneAligned  ])
                
                
        baseNameOutput = os.path.splitext(outputHTKPhoneAligned)[0]
        prepareOutputForPraat(baseNameOutput, timeShift)
    
    
    
    '''
parse output in HTK's mlf output format ; load into list; 
convert from phoneme to word level alignment
serialize into table format easy to load from praat   

'''    
def prepareOutputForPraat(baneNameAudioFile, timeShift):
    #TODO: load time shift
   
    
    listTsAndWords = mlf2WordAndTsList(baneNameAudioFile + PHONEME_ALIGNED_SUFFIX)
    
    for index in range(len(listTsAndWords)):
        listTsAndWords[index][0] = listTsAndWords[index][0] + timeShift
        
    writeListToTextFile(listTsAndWords, 'startTs word\n', baneNameAudioFile + WORD_ALIGNED_SUFFIX)
    print 'word level alignment written to file:  baneNameAudioFile + WORD_ALIGNED_SUFFIX'
    
