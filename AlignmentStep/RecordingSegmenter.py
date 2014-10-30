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
from utils.Utils import  writeListOfListToTextFile, loadTextFile
from Aligner import Aligner, HTK_MLF_ALIGNED_SUFFIX, PHRASE_ANNOTATION_EXT,\
    openAlignmentInPraat
import sys
from evaluation.WordLevelEvaluator import evalAlignmentError



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
        split into chunks using manually annotated sections from @param pathToSectionAnnotations, and align each  
    
    '''
    def alignOneRecording(self, pathToHtkModel, makamScore, pathToAudioFile, pathToSectionAnnotations, path_TO_OUTPUT, withSynthesis):

        
            makamRecording = MakamRecording(makamScore, pathToAudioFile, pathToSectionAnnotations)
            
            # convert to wav 
            makamRecording.mp3ToWav()
            
            # divide into segments
            makamRecording.divideAudio()
            
            makamRecording.markUsedChunks()
            
            # prepare eval metric:
            numParts = 0;
            listAllAlignmnetErrors = []
            
            for whichChunk in range(len(makamRecording.sectionIndices)):
                sectionIndex =  makamRecording.sectionIndices[whichChunk]
                # section not described in score
                if sectionIndex == 0:
                    continue
                
                lyrics = makamRecording.makamScore.sectionToLyricsMap[sectionIndex-1][1]
                
                # some sections have errors in melodia. so dont use them.
#                 if not makamRecording.isChunkUsed[whichChunk]:
#                     continue
                
                # skip non-vocal sections
                if lyrics == "" or "." in lyrics:
                    continue 
                
                ####=================================
                # run alignment
                currPathToAudioFile = makamRecording.pathToDividedAudioFiles[whichChunk]
                
                
                
                outputHTKPhoneAlignedURI = RecordingSegmenter.alignOneChunk(pathToHtkModel, path_TO_OUTPUT, lyrics, currPathToAudioFile, 0, withSynthesis)
                basenAudioFile = os.path.splitext(currPathToAudioFile)[0]
                phraseAnnoURI = basenAudioFile  + PHRASE_ANNOTATION_EXT
                
                
                currChunkAlignmentErrors = evalAlignmentError(phraseAnnoURI, outputHTKPhoneAlignedURI)
                listAllAlignmnetErrors.extend(currChunkAlignmentErrors)
                print( "error is {1} for {0} ".format(currPathToAudioFile,currChunkAlignmentErrors))  
                
                ### OPTIONAL : open in praat
                praseAnno = os.path.splitext(currPathToAudioFile)[0] + PHRASE_ANNOTATION_EXT
                openAlignmentInPraat(praseAnno, outputHTKPhoneAlignedURI, 0, currPathToAudioFile)
                
                numParts +=1
                # numPArts not needed for now
                
            return listAllAlignmnetErrors


    
    ''' align one audio chunk 
    @param isLyricsFromFile - option to load lyrics from file with ext .txtTur
    if isLyricsFromFile=1, loads lyrics from  
    else lyrics  are the  @param lyrics itself 
    '''

    @staticmethod
    def alignOneChunk( pathToHtkModel, path_TO_OUTPUT, lyrics, currPathToAudioFile, isLyricsFromFile, withSynthesis):
        
        
        if  not(os.path.isdir(path_TO_OUTPUT)):
            os.mkdir(path_TO_OUTPUT);
        
        chunkAligner = Aligner(pathToHtkModel, currPathToAudioFile, lyrics, isLyricsFromFile,  withSynthesis)
    

        baseNameAudioFile = os.path.splitext(os.path.basename(chunkAligner.pathToAudioFile))[0]
        
        
        outputHTKPhoneAlignedURI = os.path.join(path_TO_OUTPUT, baseNameAudioFile) + HTK_MLF_ALIGNED_SUFFIX
      
        chunkAligner.alignAudio(0, path_TO_OUTPUT, outputHTKPhoneAlignedURI)
        
     
        
        
        return outputHTKPhoneAlignedURI
        


if __name__ == '__main__':
       
      
       print 'in recording segmenter main method'
#         ----
        
#         # align all recrodings
#         recrodingDirs = os.walk(".").next()[1]
#         
#         for recordingDir in recrodingDirs:
#             
#             recordingSegmenter.alignRecording(recordingDir, makamScore)