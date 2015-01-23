# -*- coding: utf-8 -*-
'''
Created on Mar 17, 2014

@author: joro
'''
import os
import glob
from utilsLyrics.Tools import getMeanAndStDevError, writeListToTextFile
from Adapt import MAP_EXT, NUM_MAP_ITERS, PATH_TO_OUTPUT, MODEL_NAME
from RecordingSegmenter import RecordingSegmenter, doitForTestPiece
from MakamScore import loadLyrics
from MakamRecording import MakamRecording


PATH_TO_HTK_MODEL = '/Volumes/IZOTOPE/adaptation_data_NOT_CLEAN/syllablingDB/hmmdefs.gmmlrmean_map_2'

PATH_TO_HTK_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/adapted/hts_female_hmmdefs.gmmlrmean_map_2'

PATH_TO_HTK_MODEL ='/Users/joro/Documents/Phd/UPF/METUdata//model_output/adapted/HTS_japan_male.gmmlrmean_map_2'

 # modelURI from adaptation script
MODEL_URI = os.path.join(PATH_TO_OUTPUT, MODEL_NAME +  MAP_EXT + str(NUM_MAP_ITERS) )


   


# PATH_TO_HTK_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/adapted/multipleGauss/hmm4/HTS_japan_female.gmmlrmean_map_2'

# PATH_TO_HTK_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata/model_output/hmmdefs'

# PATH_TO_HTK_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/adapted/syllablingDB.gmmlrmean_map_2'

#PATH_TO_HTK_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/hmmdefs.gmllrmean_gmmlr_4' 

#PATH_TO_NOTCLEAN_ADAPTDATA = '/Users/joro/Documents/Phd/UPF/adaptation_data_NOT_CLEAN/syllablingDB/'
# PATH_TO_NOTCLEAN_ADAPTDATA = '/Users/joro/Documents/Phd/UPF/adaptation_data_NOT_CLEAN/04_Hamiyet_Yuceses_-_Bakmiyor_Cesm-i_Siyah_Feryade/'      
PATH_TO_NOTCLEAN_ADAPTDATA = '/tmp/audio/'

  
# PATH_TEST_DATASET = '/Users/joro/Documents/Phd/UPF/adaptation_data_soloVoice/'





# PATH_TO_OUTPUT_RESULTS = '/tmp/varnam/'
PATH_TO_OUTPUT_RESULTS = '/tmp/audioTur/'

# PATH_TO_OUTPUT_RESULTS = '/Users/joro/Documents/Phd/UPF/FMA2014_tex fullPaper/FigureGenerationScripts/'

'''
whole recording from test symbtr corpus
most important method recordingSegmenter.alignOneRecording  
'''
    

if __name__ == '__main__':

    ##########################doit for one recording ##################################
    
            
#         compositionName = 'nihavent--sarki--aksak--bakmiyor_cesm-i--haci_arif_bey'
#         recordingDir = '04_Hamiyet_Yuceses_-_Bakmiyor_Cesm-i_Siyah_Feryade'
#         
# #         
#         compositionName = 'nihavent--sarki--curcuna--kimseye_etmem--kemani_sarkis_efendi'
#         recordingDir = '03_Bekir_Unluataer_-_Kimseye_Etmem_Sikayet_Aglarim_Ben_Halime'
# #         
#         compositionName = 'nihavent--sarki--aksak--koklasam_saclarini--artaki_candan'
#         recordingDir = '2-15_Nihavend_Aksak_Sarki'
        
        compositionName = 'nihavent--sarki--aksak--gel_guzelim--faiz_kapanci'
        recordingDir = '18_Munir_Nurettin_Selcuk_-_Gel_Guzelim_Camlicaya'  
# 
#         compositionName = 'ussak--sarki--duyek--aksam_oldu_huzunlendim--semahat_ozdenses'
#         recordingDir = '06_Semahat_Ozdenses_-_Aksam_Oldu_Huzunlendim'
# #              
        
        compositionName = 'segah--sarki--curcuna--olmaz_ilac--haci_arif_bey'
        recordingDir = '21_Recep_Birgit_-_Olmaz_Ilac_Sine-i_Sad_Pareme'
        
        compositionName ='muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik'
        recordingDir = '1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde'
        
        compositionName = 'muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik_short'
        
        
        withSynthesis = 0
        
        currAlignmentErrors = doitForTestPiece(compositionName, recordingDir, withSynthesis)
        mean, stDev, median = getMeanAndStDevError(currAlignmentErrors)



    ############################# doit for a list of recordings: MALE  ###############################        
    
        compositionNamesMale = ['nihavent--sarki--aksak--gel_guzelim--faiz_kapanci',
                                'nihavent--sarki--aksak--koklasam_saclarini--artaki_candan',
                                'nihavent--sarki--aksak--koklasam_saclarini--artaki_candan', 
                            'nihavent--sarki--curcuna--kimseye_etmem--kemani_sarkis_efendi',
                             'segah--sarki--curcuna--olmaz_ilac--haci_arif_bey'
                             ] 
                             
                     
                            
                            
        recordingDirsMale = ['18_Munir_Nurettin_Selcuk_-_Gel_Guzelim_Camlicaya',
                             '20_Koklasam_Saclarini', 
                             '2-15_Nihavend_Aksak_Sarki',
                         '03_Bekir_Unluataer_-_Kimseye_Etmem_Sikayet_Aglarim_Ben_Halime', 
                         '21_Recep_Birgit_-_Olmaz_Ilac_Sine-i_Sad_Pareme'
                        ]
                          
                          
  ############################# doit  for a list of recordings : FEMALE #############################
        compositionNamesFemale = ['nihavent--sarki--turkaksagi--nerelerde_kaldin--ismail_hakki_efendi',
                                                        'muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik',
                                                        'nihavent--sarki--aksak--bakmiyor_cesm-i--haci_arif_bey' , 
                                                        'huzzam--sarki--curcuna--kusade_taliim--sevki_bey', 
                                                        'ussak--sarki--duyek--aksam_oldu_huzunlendim--semahat_ozdenses'
                                                        

                      ]                        
        recordingDirsFemale = [
                         '3-12_Nerelerde_Kaldin', 
                         '1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde', 
                         '04_Hamiyet_Yuceses_-_Bakmiyor_Cesm-i_Siyah_Feryade', 
                         '06_Kusade_Talihim',
                         '06_Semahat_Ozdenses_-_Aksam_Oldu_Huzunlendim'
                         
                         ]       
        
        
        
        
        ##### only female #############################
         
#         compositionNames = compositionNamesFemale
#         recordingDirs = recordingDirsFemale
#          

#         ############ only male  
#         compositionNames = compositionNamesMale
#         recordingDirs = recordingDirsMale
#         
        
        
        
        ######### both ##################
        compositionNames = compositionNamesFemale
        recordingDirs = recordingDirsFemale
 
        compositionNames.extend(compositionNamesMale)
        recordingDirs.extend(recordingDirsMale)                  


        #############################
        totalErrors = []
        for compositionName, recordingDir in zip(compositionNames, recordingDirs):
            currAlignmentErrors = doitForTestPiece(compositionName, recordingDir)
            totalErrors.extend(currAlignmentErrors)
          
        
        mean, stDev, median = getMeanAndStDevError(totalErrors)
        print "(", median ,  ",", mean, "," , stDev ,   ")"
        
        writeListToTextFile(totalErrors, None, PATH_TO_OUTPUT_RESULTS  + "maleErrors")
        
