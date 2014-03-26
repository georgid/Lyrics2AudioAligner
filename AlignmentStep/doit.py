# -*- coding: utf-8 -*-
'''
Created on Mar 17, 2014

@author: joro
'''
from Aligner import Aligner, openAlignmentInPraat

if __name__ == '__main__':


        pathToHtkModel = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/hmmdefs'

#         pathToHtkModel = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/hmmdefs.gmllrmean_gmmlr_4_map_2' 
        
        pathToAudioFile ='/Volumes/IZOTOPE/adaptation_data_NOT_CLEAN/kani_karaca-cargah_tevsih_11.wav'
        
        pathToAudioFile ='/Volumes/IZOTOPE/adaptation_data_NOT_CLEAN/kani_karaca-cargah_tevsih_12.wav'
        
        pathToAudioFile ='/Volumes/IZOTOPE/adaptation_data_NOT_CLEAN/kani_karaca-cargah_tevsih.wav'
        
        outputHTKPhoneAlignedURI = '/Volumes/IZOTOPE/adaptation_data_NOT_CLEAN/kani_karaca-cargah_tevsih_12_model_4_map_1.phonemeAligned'
        
        outputHTKPhoneAlignedURI = '/tmp/test.phonemeAligned'

#         outputHTKPhoneAlignedURI = '/Volumes/IZOTOPE/adaptation_data_NOT_CLEAN/kani_karaca-cargah_tevsih_12_model_4_map_2.phonemeAligned'

        
#         lyrics = u'kudumün ra rahmet-i zevk u Zevk u'
        lyrics = u'safadır ya ya Resul Allah Allah'
 
        aligner = Aligner(pathToHtkModel, pathToAudioFile, lyrics) 
        
        timeShift = 35.81
        timeShift =  0
#         aligner.alignAudio(  timeShift, outputHTKPhoneAligned)
        aligner.alignAudio( timeShift, outputHTKPhoneAlignedURI)
        
        # visualize result.
        wordAnnoURI = '/Volumes/IZOTOPE/adaptation_data_soloVoice/kani_karaca-cargah-tevsih/kani_karaca-cargah_tevsih.TextGrid'
        openAlignmentInPraat(wordAnnoURI, outputHTKPhoneAlignedURI, timeShift)
        