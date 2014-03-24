# -*- coding: utf-8 -*-
'''
Created on Mar 17, 2014

@author: joro
'''
from Aligner import Aligner

if __name__ == '__main__':


        pathToHtkModel = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/hmmdefs.gmllrmean_gmmlr_4_map_2' 
        
        pathToAudioFile ='/Volumes/IZOTOPE/adaptation_data_NOT_CLEAN/kani_karaca-cargah_tevsih_11.wav'
        
#         pathToAudioFile ='/Volumes/IZOTOPE/adaptation_data_NOT_CLEAN/kani_karaca-cargah_tevsih_12.wav'
        
        
        outputHTKPhoneAligned = '/Volumes/IZOTOPE/adaptation_data_NOT_CLEAN/kani_karaca-cargah_tevsih_12_model_4_map_1.phonemeAligned'

#         outputHTKPhoneAligned = '/Volumes/IZOTOPE/adaptation_data_NOT_CLEAN/kani_karaca-cargah_tevsih_12_model_4_map_2.phonemeAligned'

        
        lyrics = u'kudumün ra rahmet-i zevk u Zevk u'
#         lyrics = u'safadır ya ya Resul Allah Allah'
 
        aligner = Aligner(pathToHtkModel, pathToAudioFile, lyrics) 

        aligner.alignAudio(  0, outputHTKPhoneAligned)
#         aligner.alignAudio( 35.81, outputHTKPhoneAligned)
        