# -*- coding: utf-8 -*-
'''
Created on Mar 17, 2014

@author: joro
'''
from Aligner import Aligner, openAlignmentInPraat, HTK_MLF_ALIGNED_SUFFIX


PATH_TO_SYLLABLING = '/Users/joro/Documents/Phd/UPF/adaptation_data_NOT_CLEAN/syllablingDB/'

        
#         pathToHtkModel = '/Volumes/IZOTOPE/adaptation_data_NOT_CLEAN/syllablingDB/hmmdefs.gmmlrmean_map_2'
pathToHtkModel = '/Users/joro/Documents/Phd/UPF/adaptation_data_NOT_CLEAN/syllablingDB/hmmdefs.gmmlrmean_map_2'
#         pathToHtkModel = '/Users/joro/Documents/Phd/UPF/METUdata/model_output/hmmdefs'


'''
align one file
'''
def doit(pathToHtkModel, pathToAudioFile,  outputHTKPhoneAlignedURI,  wordAnnoURI ):
        
        lyrics = ""
        aligner = Aligner(pathToHtkModel, pathToAudioFile, lyrics, 1) 
        
        timeShift = 35.81
        timeShift =  0
#         aligner.alignAudio(  timeShift, outputHTKPhoneAligned)
        aligner.alignAudio( timeShift, outputHTKPhoneAlignedURI)
        
       
        openAlignmentInPraat(wordAnnoURI, outputHTKPhoneAlignedURI, timeShift)

''' lazy mathod on top of doit
'''
        
def doitForSyllablingFile(audioName):


        pathToAudio = PATH_TO_SYLLABLING + audioName + '.wav'
        pathToOutput =  PATH_TO_SYLLABLING + audioName + HTK_MLF_ALIGNED_SUFFIX
        
        wordAnnoURI = PATH_TO_SYLLABLING +  audioName + '.TextGrid'
        
        doit(pathToHtkModel, pathToAudio , pathToOutput, wordAnnoURI ) 

if __name__ == '__main__':
        
        audioName = 'alf_3_slow1'
        audioName = 'este_3_slow1'
        audioName = 'amaury_3_slow1'

        
        
        doitForSyllablingFile(audioName)
                
#         pathToHtkModel = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/hmmdefs'
# 
# #         pathToHtkModel = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/hmmdefs.gmllrmean_gmmlr_4_map_2' 
#         
#         pathToAudioFile ='/Volumes/IZOTOPE/adaptation_data_NOT_CLEAN/kani_karaca-cargah_tevsih_11.wav'
#         
#         pathToAudioFile ='/Volumes/IZOTOPE/adaptation_data_NOT_CLEAN/kani_karaca-cargah_tevsih_12.wav'
#         
#         pathToAudioFile ='/Volumes/IZOTOPE/adaptation_data_NOT_CLEAN/kani_karaca-cargah_tevsih.wav'
#         
#         outputHTKPhoneAlignedURI = '/Volumes/IZOTOPE/adaptation_data_NOT_CLEAN/kani_karaca-cargah_tevsih_12_model_4_map_1.phonemeAligned'
#         
#         outputHTKPhoneAlignedURI = '/tmp/test.phonemeAligned'
# 
# #         outputHTKPhoneAlignedURI = '/Volumes/IZOTOPE/adaptation_data_NOT_CLEAN/kani_karaca-cargah_tevsih_12_model_4_map_2.phonemeAligned'
# 
#         
# #         lyrics = u'kudumün ra rahmet-i zevk u Zevk u'
#         lyrics = u'safadır ya ya Resul Allah Allah'
#  
#     
        