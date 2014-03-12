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
def loadMakamScore(pathTotxt, pathToSectionTsv):
    
 # initialize makam lyrics
        makamScore = MakamScore(pathTotxt, pathToSectionTsv)
        
        # individual lyrics line written to separate files. 
        # then these files loaded fro each segment
        # done because might be needed at evaulation
        makamScore.serializeLyricsToFile()    
        return makamScore


def alignOneRecording(makamScore, pathToAudio, pathToSectionAnnotations):
    
       
        
        
        makamRecording = MakamRecording(makamScore, pathToAudio, pathToSectionAnnotations)
        
        # divide into segments
        makamRecording.divideAudio()
        
        for whichChunk in range(len(makamRecording.sectionIndices)):
            sectionIndex =  makamRecording.sectionIndices[whichChunk]
            lyrics = makamRecording.makamScore.sectionToLyricsMap[sectionIndex-1][1]
            
            # skip non-vocal sections
            if lyrics == "":
                continue 
            
            # run alignment
            baneNameAudioFile = os.path.splitext(makamRecording.pathToDividedAudioFiles[whichChunk])[0]
    #         pathTolyricSectionFile= makamRecording.makamScore.compositionName + "_" +  makamRecording.sectionNamesSequence[0]  + ".txtTur"
             
    #         commandWithArgs = [pathToAlignmentTool, baneNameAudioFile, lyrics, baneNameAudioFile + ".phone-level.output"  ]    
    #         pipe = subprocess.Popen(commandWithArgs)
    #         print "executing command: ", commandWithArgs
    
            pipe = subprocess.Popen([pathToAlignmentTool, baneNameAudioFile, lyrics, baneNameAudioFile + ".phone-level.output"  ])
            
            
        
    
    
        return


if __name__ == '__main__':
        pathToComposition = os.path.join(PATH_TEST_DATASET, COMPOSITION_NAME)
        os.chdir(pathToComposition)
        pathToTxt = os.path.join(pathToComposition, glob.glob("*.txt")[0])
        pathToSectionTsv = os.path.join(pathToComposition, glob.glob("*.sections.tsv")[0])
        
        makamScore =  loadMakamScore(pathToTxt, pathToSectionTsv)
        
#         ----
        
        # align recrodings
        recrodingDirs = os.walk(".").next()[1]
        
        for recordingDir in recrodingDirs:
            pathToRecording = os.path.join(pathToComposition, recordingDir)
            os.chdir(pathToRecording)
            pathToSectionAnnotations = os.path.join( pathToRecording, glob.glob('*.sectionAnno.txt')[0])
#             pathToAudio =  os.path.join(pathToRecording, glob.glob('*.wav')[0])
            
            pathToAudio = '/Users/joro/Documents/Phd/UPF/turkish-makam-lyrics-2-audio-test-data/muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde.wav'
            alignOneRecording(makamScore, pathToAudio, pathToSectionAnnotations )