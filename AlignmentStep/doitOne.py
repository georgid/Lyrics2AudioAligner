'''
Created on Apr 15, 2014
With .txtTur file given
@author: joro
'''
import glob
from macpath import splitext
import os
import sys


parentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0]) ), os.path.pardir)) 

pathAdapt = os.path.join(parentDir, 'AdaptationStep')
sys.path.append(pathAdapt)


from Adapt import PATH_TO_OUTPUT, MODEL_NAME, PATH_TO_CLEAN_ADAPTDATA, adapt, \
    MLLR_EXT, MAP_EXT, NUM_MAP_ITERS
from Aligner import PHRASE_ANNOTATION_EXT, openAlignmentInPraat, Aligner


pathEvaluation = os.path.join(parentDir, 'AlignmentEvaluation')
sys.path.append(pathEvaluation)
from WordLevelEvaluator import evalAlignmentError

pathAlignmentDur = os.path.join(parentDir, 'AlignmentDuration')
sys.path.append(pathAlignmentDur)
from doitOneChunk import loadLyrics, visualiseInPraat
from Constants import AUDIO_EXTENSION

pathUtils = os.path.join(parentDir, 'utilsLyrics')
sys.path.append(pathUtils )
from Utilz import getMeanAndStDevError

 # modelURI from adaptation script
MODEL_URI = os.path.join(PATH_TO_OUTPUT, MODEL_NAME  + MAP_EXT + str(NUM_MAP_ITERS) )

MODEL_URI = os.path.join(PATH_TO_OUTPUT, MODEL_NAME +  MAP_EXT + '3' )

# speech model
MODEL_URI = '/Users/joro/Documents/Phd/UPF/METUdata/model_output/multipleGaussians/hmmdefs9/iter9/hmmdefs'
      



''' lazy mathod on top of doit
NOTE: first run AdaptationStep/Adapt.adapt(). THen URI to model  is constructed directly from there by the global variable. MODEL_NAME
'''
        
def main(argv):
        
       
        if len(argv) != 4:
            print ("usage: {}  <pathToComposition> <whichSection> <URI_recording_no_ext>".format(argv[0]) )
            sys.exit();
    
    
        URIrecordingNOExt = '/Users/joro/Documents/Phd/UPF/adaptation_data_soloVoice/ISTANBUL/goekhan/02_Gel_3_zemin'
        URIrecordingNOExt = argv[3]
        URIrecordingWav = URIrecordingNOExt  + AUDIO_EXTENSION
                
        pathToComposition = '/Users/joro/Documents/Phd/UPF/adaptation_data_soloVoice/nihavent--sarki--aksak--gel_guzelim--faiz_kapanci/'
        pathToComposition = argv[1]
    
        whichSection = 3
        whichSection = int(argv[2])
        
        lyrics = loadLyrics(pathToComposition, whichSection)
        
        withSynthesis = 0
      
        URIrecordingAnno = URIrecordingNOExt + PHRASE_ANNOTATION_EXT
        
        outputHTKPhoneAlignedURI = Aligner.alignOnechunk(MODEL_URI, URIrecordingWav, lyrics,  URIrecordingAnno,  '/tmp/', withSynthesis)
        EVALLEVEL = 2
        
        alignmentErrors  = evalAlignmentError(URIrecordingAnno, outputHTKPhoneAlignedURI, EVALLEVEL)
        
        mean, stDev, median = getMeanAndStDevError(alignmentErrors)
        
        print "(", mean, ",", stDev, ")"
        
        
           ### OPTIONAL : open in praat
        visualiseInPraat(URIrecordingNOExt, outputHTKPhoneAlignedURI, True, [])

        
        return mean, stDev, alignmentErrors


if __name__ == '__main__':
    main(sys.argv)
    
        #########  MALE all ##########################      
#         PATH_TEST_DATASET = '/Users/joro/Documents/Phd/UPF/test_data_soloVoice_male/' 
#          
#          
#        
#         audioName1 = 'amaury_3_slow1'
#         audioName2 = 'alf_3_slow1'
#         audioName3 = 'este_3_slow1'
#          
#         audioName4 = 'nitech_jp_song060_m001_003'
#         audioName5 = 'nitech_jp_song060_m001_007'
#          
#         audioName6 = 'GEORGI_20_Koklasam_Saclarini_zemin_from_19.292461_to_32.514873'
#         audioName7 = '1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde_zemin_from_0_143205_to_38_756510'
#          
#         audioNames = [audioName1, audioName2, audioName3, audioName4, audioName5, audioName6, audioName7]
#          
#         totalAlignementError = []
#          
# #         mean, stDev, alignmentErrors = main(PATH_TEST_DATASET  , audioName7)
#          
#         for i in range(7):
#             mean, stDev, alignmentErrors = main(PATH_TEST_DATASET  , audioNames[i])
#             totalAlignementError.extend(alignmentErrors)
#  
# #         total statistics:    
#         totalMean, totalStDev =  getMeanAndStDevError(totalAlignementError)  
#         print "(", totalMean, ",", totalStDev, ")" 


############# MALE ALL FILES OF KANI iN A GIVEN DIR: 

#         PATH_TEST_DATASET = '/Users/joro/Documents/Phd/UPF/test_data_soloVoice_kani_karaca-cargah_tevsih/'
#         
#         os.chdir(PATH_TEST_DATASET)
#         
#         totalAlignementError = []
#         for fileN in glob.glob("*.wav"):
#             baseName = splitext(fileN)[0]
#             mean, stDev, alignmentErrors = main(PATH_TEST_DATASET  , baseName)
#             totalAlignementError.extend(alignmentErrors)
#         
#         totalMean, totalStDev =  getMeanAndStDevError(totalAlignementError)  
#         print "(", totalMean, ",", totalStDev, ")" 



################################### test with one chunk of sarki recording. Use lazy function ####################################

#     PATH_TEST_DATASET = '/Users/joro/Documents/Phd/UPF/test_data_synthesis'
# 
#     compositionName = 'nihavent--sarki--aksak--bakmiyor_cesm-i--haci_arif_bey'
#     recordingDir = '04_Hamiyet_Yuceses_-_Bakmiyor_Cesm-i_Siyah_Feryade'
# 
#     
#         
#            
#     error = main(PATH_TEST_DATASET, recordingDir)
#      
#     print error
