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
from Aligner import Aligner, HTK_MLF_ALIGNED_SUFFIX, PHRASE_ANNOTATION_EXT,\
    openAlignmentInPraat
from evaluation.WordLevelEvaluator import evalPhraseLevelError



# 
# COMPOSITION_NAME = 'nihavent--sarki--aksak--koklasam_saclarini--artaki_candan'
# RECORDING_DIR = '20_Koklasam_Saclarini'
#   
# COMPOSITION_NAME = 'nihavent--sarki--curcuna--kimseye_etmem--kemani_sarkis_efendi'
# RECORDING_DIR = '03_Bekir_Unluataer_-_Kimseye_Etmem_Sikayet_Aglarim_Ben_Halime'
# # 
# # 
# COMPOSITION_NAME = 'segah--sarki--curcuna--olmaz_ilac--haci_arif_bey'
# RECORDING_DIR = '21_Recep_Birgit_-_Olmaz_Ilac_Sine-i_Sad_Pareme'
# # 
# COMPOSITION_NAME = 'nihavent--sarki--turkaksagi--nerelerde_kaldin--ismail_hakki_efendi'
# RECORDING_DIR = '3-12_Nerelerde_Kaldin'

OUTPUT_PATH = '/tmp/testAudio'

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

        
    ''' align one recording from symbTr
        split into chunk and align each  
    
    '''
    def alignOneRecording(self, pathToHtkModel, makamScore, pathToAudioFile, pathToSectionAnnotations, path_TO_OUTPUT):

        
            makamRecording = MakamRecording(makamScore, pathToAudioFile, pathToSectionAnnotations)
            
            # convert to wav 
            makamRecording.mp3ToWav()
            
            # divide into segments
            makamRecording.divideAudio()
            
            # prepare eval metric:
            totalError = 0; 
            numParts = 0;
            
            for whichChunk in range(len(makamRecording.sectionIndices)):
                sectionIndex =  makamRecording.sectionIndices[whichChunk]
                lyrics = makamRecording.makamScore.sectionToLyricsMap[sectionIndex-1][1]
                
                # skip non-vocal sections
                if lyrics == "" or "." in lyrics:
                    continue 
                
                ####=================================
                # run alignment
                currPathToAudioFile = makamRecording.pathToDividedAudioFiles[whichChunk]
                
                
                
                outputHTKPhoneAlignedURI = RecordingSegmenter.alignOneChunk(pathToHtkModel, path_TO_OUTPUT, lyrics, currPathToAudioFile, 0)
                basenAudioFile = os.path.splitext(currPathToAudioFile)[0]
                phraseAnnoURI = basenAudioFile  + PHRASE_ANNOTATION_EXT
                
                diff = 0
                diff = evalPhraseLevelError(phraseAnnoURI, outputHTKPhoneAlignedURI)
                print( "error is {1} for {0} ".format(currPathToAudioFile,diff))  
                
                ### OPTIONAL : open in praat
                praseAnno = os.path.splitext(currPathToAudioFile)[0] + PHRASE_ANNOTATION_EXT
                openAlignmentInPraat(praseAnno, outputHTKPhoneAlignedURI, 0, currPathToAudioFile)
                
                totalError += diff
                numParts +=1
                
            return totalError / numParts


    
    ''' align one audio chunk 
    @param lyricsFromFile - option to load lyrics from file, or from @param lyrics
    '''

    @staticmethod
    def alignOneChunk( pathToHtkModel, path_TO_OUTPUT, lyrics, currPathToAudioFile, lyricsFromFile):
        
        chunkAligner = Aligner(pathToHtkModel, currPathToAudioFile, lyrics, lyricsFromFile)
    

        baseNameAudioFile = os.path.splitext(os.path.basename(chunkAligner.pathToAudioFile))[0]
        
        
        outputHTKPhoneAlignedURI = os.path.join(path_TO_OUTPUT, baseNameAudioFile) + HTK_MLF_ALIGNED_SUFFIX
#         if (not(os.path.isfile(outputHTKPhoneAlignedURI)) ):
        chunkAligner.alignAudio(0, path_TO_OUTPUT, outputHTKPhoneAlignedURI)
        
     
        
        
        return outputHTKPhoneAlignedURI
        


if __name__ == '__main__':
       
      
       print 'blah'
#         ----
        
#         # align all recrodings
#         recrodingDirs = os.walk(".").next()[1]
#         
#         for recordingDir in recrodingDirs:
#             
#             recordingSegmenter.alignRecording(recordingDir, makamScore)