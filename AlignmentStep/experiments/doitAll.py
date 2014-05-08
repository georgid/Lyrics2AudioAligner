'''
Created on Apr 15, 2014
Main for 
@author: joro
'''
from Aligner import PHRASE_ANNOTATION_EXT, openAlignmentInPraat
from RecordingSegmenter import RecordingSegmenter
from evaluation.WordLevelEvaluator import evalPhraseLevelError
from Adapt import PATH_TO_OUTPUT, MODEL_NAME, PATH_TO_CLEAN_ADAPTDATA, adapt,\
    MLLR_EXT, MAP_EXT, NUM_MAP_ITERS
from matplotlib.sphinxext.plot_directive import out_of_date
import os
import sonicVisTextPhnDir2mlf
from doit import PATH_TEST_DATASET
from scipy.odr.odrpack import Model
from utilsLyrics.Tools import getMeanAndStDevError

 # modelURI from adaptation script
MODEL_URI = os.path.join(PATH_TO_OUTPUT, MODEL_NAME + MLLR_EXT + MAP_EXT + str(NUM_MAP_ITERS-1) )
# speech model
MODEL_URI = '/Users/joro/Documents/Phd/UPF/METUdata/model_output/multipleGaussians/hmmdefs9/iter9/hmmdefs'
      



''' lazy mathod on top of doit
NOTE: first run AdaptationStep/Adapt.adapt(). THen URI to model  is constructed directly from there by the global variable. MODEL_NAME
'''
        
def doitForAdaptationFile(pathTodata,  audioName):
        ################### ADAPTATION: ################
        
        pathToAudio =    pathTodata + audioName + '.wav'
        
        
        phraseAnnoURI = pathTodata +  audioName + PHRASE_ANNOTATION_EXT
        
      
        outputHTKPhoneAlignedURI = RecordingSegmenter.alignOneChunk(MODEL_URI, '/tmp/audioTur', "", pathToAudio, 1)
        alignmentErrors  = evalPhraseLevelError(phraseAnnoURI, outputHTKPhoneAlignedURI)
        
        mean, stDev = getMeanAndStDevError(alignmentErrors)
        
        
        print "mean : ", mean, "st dev: " , stDev
        
        
        
           ### OPTIONAL : open in praat
        openAlignmentInPraat(phraseAnnoURI, outputHTKPhoneAlignedURI, 0, pathToAudio)
        
        return mean, stDev  


if __name__ == '__main__':

        #########  MALE ##########################      
        PATH_TEST_DATASET = '/Users/joro/Documents/Phd/UPF/test_data_soloVoice_male/' 

        audioName = 'alf_3_slow1'
        audioName = 'amaury_3_slow1'
        
        audioName = 'nitech_jp_song060_m001_003'
        audioName = 'nitech_jp_song060_m001_007'
  
        audioName = 'GEORGI_20_Koklasam_Saclarini_zemin_from_19.292461_to_32.514873'
        
        audioName = 'este_3_slow1'
        mean, stDev = doitForAdaptationFile(PATH_TEST_DATASET  , audioName)
        


  

#       
#      female  
#     audioName = 'nitech_jp_song070_f001_070'
# 
#        
# #      
 
    
  

################################### test with one chunk of sarki recording ####################################
#     compositionName = 'nihavent--sarki--aksak--koklasam_saclarini--artaki_candan/' 
#     
#     PATH_TO_DATA = '/Users/joro/Documents/Phd/UPF/adaptation_data_soloVoice/20_Koklasam_Saclarini_Synth/' ;
#    
#     audioName ='20_Koklasam_Saclarini_nakarat_from_46_047599_to_59_716561'
#     
#        
#           
#     error = doitForAdaptationFile(PATH_TO_DATA, audioName)
#     
#     print error
