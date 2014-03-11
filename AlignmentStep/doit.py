# -*- coding: utf-8 -*-
'''
Created on Mar 3, 2014

@author: joro
'''

from MakamScore import MakamScore
from MakamRecording import MakamRecording 
import subprocess
import os
import glob

PATH_TEST_DATASET='/Users/joro/Documents/Phd/UPF/turkish-makam-lyrics-2-audio-test-data/'
pathToAlignmentTool = os.path.abspath('doForceAligment.sh')
COMPOSITION_NAME = 'muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik'
# COMPOSITION_NAME = 'nihavent--sarki--aksak--gel_guzelim--faiz_kapanci'
# COMPOSITION_NAME = 'nihavent--sarki--aksak--koklasam_saclarini--artaki_candan'
# COMPOSITION_NAME='hicaz--sarki--aksak--gulsen-i_husnune--rifat_bey'

'''
Loads all lyrics , divides them line-wise and writes new files

'''
def dividebyLineAllLyrics(pathTotxtTur):
    
 # initialize makam lyrics
        makamScore = MakamScore(pathTotxtTur)
        
        # individual lyrics line written to separate files. 
        # then these files loaded fro each segment
        # done because might be needed at evaulation
        makamScore.serializeLyricsToFile()    
        return makamScore


def alignOneRecording(makamScore, pathToAudio, pathToSectionAnnotations):
    
       
        
        
        makamRecording = MakamRecording(makamScore, pathToAudio, pathToSectionAnnotations)
        
        # divide into segments
        makamRecording.assignSectionLyrics()
        makamRecording.divideAudio()
        
        lyrics = makamRecording.sectionLyricsMap[0]
        
        # run alignment
        baneNameAudioFile = os.path.splitext(makamRecording.pathToDividedAudioFiles[0])[0]
        pathTolyricSectionFile= makamRecording.makamScore.compositionName + "_" +  makamRecording.sectionNamesSequence[0]  + ".txtTur"
         
        commandWithArgs = [pathToAlignmentTool, baneNameAudioFile, pathTolyricSectionFile, baneNameAudioFile + ".phone-level.output"  ]    
        pipe = subprocess.Popen(commandWithArgs)
#         pipe = subprocess.Popen([pathToAlignmentTool, baneNameAudioFile, lyrics, baneNameAudioFile + ".phone-level.output"  ])
        
#         print "executing command: ", commandWithArgs
        
        
    
    
        return


if __name__ == '__main__':
        pathToComposition = os.path.join(PATH_TEST_DATASET, COMPOSITION_NAME)
        os.chdir(pathToComposition)
        pathTotxtTur = os.path.join(pathToComposition, glob.glob("*.txtTur")[0])
        
        makamScore =  dividebyLineAllLyrics(pathTotxtTur)
        
#         ----
        
        # align recrodings
        recrodingDirs = os.walk(".").next()[1]
        
        for recordingDir in recrodingDirs:
            pathToRecording = os.path.join(pathToComposition, recordingDir)
            
            pathToSectionAnnotations = os.path.join(pathToRecording,  recordingDir + '.sectionAnno.txt')
            pathToAudio =   os.path.join(pathToRecording,  recordingDir  + '.wav')
    
            alignOneRecording(makamScore, pathToAudio, pathToSectionAnnotations )