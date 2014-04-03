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
from utils.Utils import mlf2WordAndTsList, writeListOfListToTextFile, loadTextFile
from Aligner import Aligner
from Cython.Compiler.Scanning import Method

PATH_TEST_DATASET='/Users/joro/Documents/Phd/UPF/turkish-makam-lyrics-2-audio-test-data/'

# COMPOSITION_NAME = 'muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik'
# RECORDING_DIR = '1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde'


COMPOSITION_NAME = 'nihavent--sarki--aksak--koklasam_saclarini--artaki_candan'
RECORDING_DIR = '20_Koklasam_Saclarini'
  
COMPOSITION_NAME = 'nihavent--sarki--curcuna--kimseye_etmem--kemani_sarkis_efendi'
RECORDING_DIR = '03_Bekir_Unluataer_-_Kimseye_Etmem_Sikayet_Aglarim_Ben_Halime'
# 
# 
COMPOSITION_NAME = 'segah--sarki--curcuna--olmaz_ilac--haci_arif_bey'
RECORDING_DIR = '21_Recep_Birgit_-_Olmaz_Ilac_Sine-i_Sad_Pareme'
# 
COMPOSITION_NAME = 'nihavent--sarki--turkaksagi--nerelerde_kaldin--ismail_hakki_efendi'
RECORDING_DIR = '3-12_Nerelerde_Kaldin'



class RecordingSegmenter(object):
   
                  
                
    def __init__(self):
        return
    
    
        ##################################################################################
    
    '''
    Loads all lyrics , divides them line-wise and writes new files
    
    '''
    def loadMakamScore(self, pathTotxt, pathToSectionTsv):
        
     # initialize makam lyrics
            makamScore = MakamScore(pathTotxt, pathToSectionTsv)
            
            # individual lyrics line written to separate files. 
            # then these files loaded fro each segment
            # done because might be needed at evaulation
#             makamScore.serializeLyricsToFile()    
            return makamScore              



##################################################################################

    
    ''' align whole recording
    
    '''

    def alignOneRecording(self, makamScore, pathToAudio, pathToSectionAnnotations):
        
           
            
            
            makamRecording = MakamRecording(makamScore, pathToAudio, pathToSectionAnnotations)
            
            # convert to wav 
            makamRecording.mp3ToWav()
            
            # divide into segments
            makamRecording.divideAudio()
            
            for whichChunk in range(len(makamRecording.sectionIndices)):
                sectionIndex =  makamRecording.sectionIndices[whichChunk]
                lyrics = makamRecording.makamScore.sectionToLyricsMap[sectionIndex-1][1]
                
                # skip non-vocal sections
                if lyrics == "" or "." in lyrics:
                    continue 
                
                # run alignment
                baneNameAudioFile = os.path.splitext(makamRecording.pathToDividedAudioFiles[whichChunk])[0]
                
                chunkAligner = Aligner(pathToHtkModel, makamRecording.pathToDividedAudioFiles[whichChunk], lyrics)
                # no output recording name
                chunkAligner.alignAudio( 0)                
        
        
            return 

   
                

    ################################################################
    ''' convenience Method
        prepare recording and audio paths
    '''
            
            
    def alignRecording(self, recordingDir, makamScore ):
        
        pathToComposition = os.path.join(PATH_TEST_DATASET, COMPOSITION_NAME)
    
        pathToRecording = os.path.join(pathToComposition, recordingDir)
    
        os.chdir(pathToRecording)
        pathToSectionAnnotations = os.path.join(pathToRecording, glob.glob('*.sectionAnno.txt')[0]) #             pathToAudio =  os.path.join(pathToRecording, glob.glob('*.wav')[0])
        pathToAudio = os.path.join(pathToRecording, recordingDir) + '.wav'
    # TODO: issue 14
        self.alignOneRecording(makamScore, pathToAudio, pathToSectionAnnotations)



if __name__ == '__main__':
       
      
        pathToHtkModel = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/hmmdefs.gmllrmean_gmmlr_4' 
            
        pathToComposition = os.path.join(PATH_TEST_DATASET, COMPOSITION_NAME)
        os.chdir(pathToComposition)
        pathToSymbTrTxt = os.path.join(pathToComposition, glob.glob("*.txt")[0])
        pathToSectionTsv = os.path.join(pathToComposition, glob.glob("*.sections.tsv")[0])
        
                    # TODO: issue 14
        recordingSegmenter = RecordingSegmenter()
        makamScore =  recordingSegmenter.loadMakamScore(pathToSymbTrTxt, pathToSectionTsv)
        
#        ----- align one rec:  
        recordingSegmenter.alignRecording(RECORDING_DIR, makamScore)
        
#         ----
        
#         # align all recrodings
#         recrodingDirs = os.walk(".").next()[1]
#         
#         for recordingDir in recrodingDirs:
#             
#             recordingSegmenter.alignRecording(recordingDir, makamScore)