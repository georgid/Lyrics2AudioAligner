'''
Created on Apr 15, 2014
Main for 
@author: joro
'''
from Aligner import PHRASE_ANNOTATION_EXT, openAlignmentInPraat
from RecordingSegmenter import RecordingSegmenter
from evaluation.WordLevelEvaluator import evalPhraseLevelError


PATH_TO_HTK_MODEL = '/Volumes/IZOTOPE/adaptation_data_NOT_CLEAN/syllablingDB/hmmdefs.gmmlrmean_map_2'

# PATH_TO_HTK_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata/model_output/hmmdefs'


########## FEMALE
PATH_TO_HTK_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/adapted/hts_female_hmmdefs.gmmlrmean_map_2'
# PATH_TO_HTK_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/adapted/multipleGauss/hmm4/HTS_japan_female.gmmlrmean_map_2'


######## MALE

PATH_TO_HTK_MODEL ='/Users/joro/Documents/Phd/UPF/METUdata//model_output/adapted/HTS_japan_male.gmmlrmean_map_2'

# PATH_TO_HTK_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/adapted/syllablingDB.gmmlrmean_map_2'

#PATH_TO_HTK_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/hmmdefs.gmllrmean_gmmlr_4' 

#PATH_TO_NOTCLEAN_ADAPTDATA = '/Users/joro/Documents/Phd/UPF/adaptation_data_NOT_CLEAN/syllablingDB/'
# PATH_TO_NOTCLEAN_ADAPTDATA = '/Users/joro/Documents/Phd/UPF/adaptation_data_NOT_CLEAN/04_Hamiyet_Yuceses_-_Bakmiyor_Cesm-i_Siyah_Feryade/'      





''' lazy mathod on top of doit
'''
        
def doitForAdaptationFile(pathTodata,  audioName):
        
    
        
        pathToAudio =    pathTodata + audioName + '.wav'
        
        
        phraseAnnoURI = pathTodata +  audioName + PHRASE_ANNOTATION_EXT
        
        
        outputHTKPhoneAlignedURI = RecordingSegmenter.alignOneChunk(PATH_TO_HTK_MODEL, '/tmp/audioTur', "", pathToAudio, 1)

        diff = evalPhraseLevelError(phraseAnnoURI, outputHTKPhoneAlignedURI)
        
           ### OPTIONAL : open in praat
        openAlignmentInPraat(phraseAnnoURI, outputHTKPhoneAlignedURI, 0)
        
        return diff


if __name__ == '__main__':

        #########  test with adaptation data ##########################      
#         audioName = 'este_3_slow1'
#         audioName = 'alf_3_slow1'
#         audioName = 'amaury_3_slow1'
# 
 
    PATH_TO_HTK_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/adapted/HTS_japan_male.gmmlrmean_map_2'
    PATH_TO_HTK_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/adapted/multipleGauss/hmm4/HTS_japan_male.gmmlrmean_map_2'

  
    PATH_TO_CLEAN_ADAPTDATA = '/Users/joro/Documents/Phd/UPF/adaptation_data_soloVoice/04_Hamiyet_Yuceses_-_Bakmiyor_Cesm-i_Siyah_Feryade/'    
    PATH_TO_CLEAN_ADAPTDATA  = '/Users/joro/Documents/Phd/UPF/adaptation_data_soloVoice/syllablingDB/'
    PATH_TO_CLEAN_ADAPTDATA = '/Users/joro/Documents/Phd/UPF/adaptation_data_soloVoice/HTS_japan_male/'
      
#     audioName = 'nitech_jp_song070_f001_070'
    audioName = 'nitech_jp_song060_m001_003'
      
    error = doitForAdaptationFile(PATH_TO_CLEAN_ADAPTDATA, audioName)
     
    print error
#      
    
    ####################### test with recorded clean voice ######################################
    
#     PATH_TO_HTK_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/adapted/HTS_japan_male.gmmlrmean_map_2'
# 
#     
#     PATH_TEST_DATASET = '/Volumes/IZOTOPE/sertan_sarki/' # this is the clean dataset 
#      
#         # these two lines are only for case of GEORGI-reocroded voice
#     compositionName = 'nihavent--sarki--aksak--koklasam_saclarini--artaki_candan/'
#     PATH_TO_CLEAN_ADAPTDATA = PATH_TEST_DATASET + compositionName + 'GEORGI/'; 
#      
#     audioName = 'GEORGI_20_Koklasam_Saclarini_zemin_from_19.292461_to_32.514873'
# # #          audioName = '04_Hamiyet_Yuceses_-_Bakmiyor_Cesm-i_Siyah_Feryade_gazel_1'
# #       
#  
#            
#     error = doitForAdaptationFile(PATH_TO_CLEAN_ADAPTDATA, audioName)
#     audioName = 'GEORGI_20_Koklasam_Saclarini_zemin_from_32.514873_to_46.047599'
#     
#     error2 = doitForAdaptationFile(PATH_TO_CLEAN_ADAPTDATA, audioName)
#           
#     error = (error + error2) / 2
#     print error
