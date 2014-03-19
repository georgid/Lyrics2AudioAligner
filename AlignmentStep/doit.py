# -*- coding: utf-8 -*-
'''
Created on Mar 17, 2014

@author: joro
'''
from Aligner import Aligner

if __name__ == '__main__':

        pathToAudioFile ='/Volumes/IZOTOPE/adaptation_data/kani_karaca-cargah_tevsih_11.wav'
#         outputHTKPhoneAligned = '/Volumes/IZOTOPE/adaptation_data/kani_karaca-cargah_tevsih_12_noAdapted.phonemeAligned'
        
        outputHTKPhoneAligned = '/Volumes/IZOTOPE/adaptation_data/kani_karaca-cargah_tevsih_11.phonemeAligned'
        
        lyrics = u'kudumün ra rahmet-i zevk u zevk u'
#         lyrics = u'safadır ya ya Resul Allah Allah'
 
        aligner = Aligner(pathToAudioFile, lyrics) 

        aligner.alignAudio(  0, outputHTKPhoneAligned)
#         aligner.alignAudio( 35.81, outputHTKPhoneAligned)
        