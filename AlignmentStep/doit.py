# -*- coding: utf-8 -*-
'''
Created on Mar 17, 2014

@author: joro
'''
from Aligner import Aligner, openAlignmentInPraat, HTK_MLF_ALIGNED_SUFFIX,\
    PHRASE_ANNOTATION_EXT
from evaluation.WordLevelEvaluator import evalPhraseLevelError
import os
import glob
from RecordingSegmenter import RecordingSegmenter



PATH_TO_HTK_MODEL = '/Volumes/IZOTOPE/adaptation_data_NOT_CLEAN/syllablingDB/hmmdefs.gmmlrmean_map_2'

PATH_TO_HTK_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/adapted/hts_female_hmmdefs.gmmlrmean_map_2'

PATH_TO_HTK_MODEL ='/Users/joro/Documents/Phd/UPF/METUdata//model_output/adapted/HTS_japan_male.gmmlrmean_map_2'





# PATH_TO_HTK_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/adapted/multipleGauss/hmm4/HTS_japan_female.gmmlrmean_map_2'

# PATH_TO_HTK_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata/model_output/hmmdefs'

# PATH_TO_HTK_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/adapted/syllablingDB.gmmlrmean_map_2'

#PATH_TO_HTK_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/hmmdefs.gmllrmean_gmmlr_4' 

#PATH_TO_NOTCLEAN_ADAPTDATA = '/Users/joro/Documents/Phd/UPF/adaptation_data_NOT_CLEAN/syllablingDB/'
# PATH_TO_NOTCLEAN_ADAPTDATA = '/Users/joro/Documents/Phd/UPF/adaptation_data_NOT_CLEAN/04_Hamiyet_Yuceses_-_Bakmiyor_Cesm-i_Siyah_Feryade/'      
PATH_TO_NOTCLEAN_ADAPTDATA = '/tmp/audio/'

PATH_TEST_DATASET = '/Users/joro/Documents/Phd/UPF/sertan_sarki_5songs_peaksSynthesis/'    
PATH_TEST_DATASET = '/Volumes/IZOTOPE/sertan_sarki/'    

          



'''
whole recording from test symbtr corpus
most important method recordingSegmenter.alignOneRecording  
'''
    
def doitForTestPiece(compositionName, recordingDir):
    
        
   
    ####### prepare composition! ############
        
        pathToComposition = os.path.join(PATH_TEST_DATASET, compositionName)
        os.chdir(pathToComposition)
        pathToSymbTrTxt = os.path.join(pathToComposition, glob.glob("*.txt")[0])
        pathToSectionTsv = os.path.join(pathToComposition, glob.glob("*.sections.tsv")[0])
        
                    # TODO: issue 14
        recordingSegmenter = RecordingSegmenter()
        makamScore =  recordingSegmenter.loadMakamScore(pathToSymbTrTxt, pathToSectionTsv)
        print "makam scre loaded"
        
        ###########        ----- align one recording
        
        pathToRecording = os.path.join(pathToComposition, recordingDir)
    
        os.chdir(pathToRecording)
        pathToSectionAnnotations = os.path.join(pathToRecording, glob.glob('*.sectionAnno.txt')[0]) #             pathToAudio =  os.path.join(pathToRecording, glob.glob('*.wav')[0])
        pathToAudio = os.path.join(pathToRecording, recordingDir) + '.wav'
        
        # TODO: issue 14
        totalError = recordingSegmenter.alignOneRecording(PATH_TO_HTK_MODEL, makamScore, pathToAudio, pathToSectionAnnotations, '/tmp/audioTur')
        print("total error for song {0} is {1}".format(recordingDir,totalError ))
        


if __name__ == '__main__':

    ############################# doit for recording ###############################        
#         
#         
       
        compositionName = 'segah--sarki--curcuna--olmaz_ilac--haci_arif_bey'
        recordingDir = '21_Recep_Birgit_-_Olmaz_Ilac_Sine-i_Sad_Pareme'
           
#         compositionName = 'nihavent--sarki--turkaksagi--nerelerde_kaldin--ismail_hakki_efendi'
#         recordingDir = '3-12_Nerelerde_Kaldin'
#         
        compositionName = 'nihavent--sarki--curcuna--kimseye_etmem--kemani_sarkis_efendi'
        recordingDir = '03_Bekir_Unluataer_-_Kimseye_Etmem_Sikayet_Aglarim_Ben_Halime'

#         compositionName = 'muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik'
#         recordingDir = '1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde'

        compositionName = 'nihavent--sarki--aksak--koklasam_saclarini--artaki_candan'
        recordingDir = '20_Koklasam_Saclarini'
         
# #                  
        doitForTestPiece(compositionName, recordingDir)

#         
# #         lyrics = u'kudumün ra rahmet-i zevk u Zevk u'
#         lyrics = u'safadır ya ya Resul Allah Allah'
#  
#     
        