'''
Created on Mar 19, 2014

used to store model variables as well
@author: joro
'''

import os
import subprocess
import shutil
from sonicVisTextPhnDir2mlf import sonicVisTextPhnDir2mlf
from multipleGauss.toMultipleGaussians import *

#  adaptation step. MLLR-  HTK Book page 47, MAP - page 160
# HERest is explained in page 138

URI_BUILD_SCRIPT = 'buildAdaptedModel.sh'

# SPEECH MODEL 
PATH_TO_INPUT_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata/model_output/multipleGaussians/hmmdefs9/iter9/hmmdefs'

#PATH_TO_INPUT_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/hmmdefs'


PATH_TO_SCRIPTS = '/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/'
PATH_TO_CONFIG = PATH_TO_SCRIPTS + 'input_files//config_singing'
PATH_TO_WAV_CONFIG = PATH_TO_SCRIPTS + 'input_files//wav_config_singing'


HMM_LIST = PATH_TO_SCRIPTS + 'interim_files/monophones1'

PATH_TO_OUTPUT='/Users/joro/Documents/Phd/UPF/METUdata//model_output/multipleGaussians/adapted/'

PATH_TO_CLEAN_ADAPTDATA = '/Users/joro/Documents/Phd/UPF/adaptation_data_soloVoice/'

PATH_TO_DUMMY_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/multipleGaussians/dummy'

MODEL_NOISE_URI  = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/multipleGaussians/NOISE//hmmdefs49/iter1/hmmdefs'


######## delete all before these variables

# # multigauss  case:
# PATH_TO_OUTPUT = '/Users/joro/Documents/Phd/UPF/METUdata//model_output/adapted/multipleGauss/hmm9/'
# PATH_TO_INPUT_MODEL = '/Users/joro/Documents/Phd/UPF/METUdata/model_output/multipleGaussians/hmmdefs9/iter9/hmmdefs'


    # modelName same as pathToAdaptData
# MODEL_NAME = 'syllablingDB'
MODEL_NAME = 'HTS_japan_female'
# MODEL_NAME = 'HTS_japan_male'
# MODEL_NAME = 'kani_karaca-all_VOCALS'

# MODEL_NAME = 'kani_karaca-all'
# MODEL_NAME = 'kani_karaca-cargah-tevsih'

# MODEL_NAME = '20_Koklasam_Saclarini'

MLLR_EXT = '.gmmlrmean'
MAP_EXT = '_map_'
NUM_MAP_ITERS = 4

'''
takes all .wav files in given dir
'''

def adapt( pathAdaptationData,  pathToAllMlf, pathToAdaptedOutput, modelName):
    
     #######################################################
    # GMMLR adaptation
    ######################################################
    
    adaptedOut = PATH_TO_INPUT_MODEL # instead of the next line
    
#     adaptedOut = os.path.join(pathToAdaptedOutput, modelName + MLLR_EXT)
 
     
#      // find build adaptedmodel
    pathToBuildScript = os.path.abspath(URI_BUILD_SCRIPT)  # @IndentOk
 
     # HERest is explained in page 138
    pipe = subprocess.Popen([pathToBuildScript, pathAdaptationData,  pathToAllMlf, pathToAdaptedOutput, adaptedOut, PATH_TO_INPUT_MODEL ])
    pipe.wait()
         
    #stop here if adaptation needed only once
#     model_in = adaptedOut
#     for i in range (3):
#             print "Adapted model: iteration" + str(i) + "\n" 
#             adaptedOut = PATH_TO_INPUT_MODEL  + '_' + str(i+2)
#             pipe = subprocess.Popen([pathToBuildScript, pathAdaptationData, adaptedDict, pathToAllMlf, pathToAdaptedOutput, adaptedOut, model_in ])
#             pipe.wait()
#             # read the result to a string
# #             result_str = pipe.stdout.read()
#             
#             model_in = adaptedOut
    
    ##############################################
    # MAP Adaptation. See HTK page 160
    ##############################################
    
    pathToModelPrevStep = adaptedOut
    outModelName = os.path.join(pathToAdaptedOutput, modelName )    
    

    
    for i in range (NUM_MAP_ITERS):
        pathToCurrMAPModel =  outModelName + MAP_EXT + str(i+1)
        shutil.copy2(pathToModelPrevStep, pathToCurrMAPModel )
            
        pathToHTKHRest = '/usr/local/bin/HERest'
        WAVS = '/tmp/codetrain_mfc.scp'
            
        command = [pathToHTKHRest, '-T', '1', '-C' , PATH_TO_CONFIG, '-S', WAVS, '-I', pathToAllMlf, '-H', pathToCurrMAPModel, '-H', PATH_TO_DUMMY_MODEL, '-H',  MODEL_NOISE_URI, '-u', 'pmvw',  HMM_LIST  ] 
        
        logName =  'log' + MAP_EXT + str(i+1)
        currLogHandle = open(logName, 'w')
        currLogHandle.flush()
        
        pipe = subprocess.Popen(command, stdout=currLogHandle)
        pipe.wait()
        
        pathToModelPrevStep = pathToCurrMAPModel
        
      
        
    
      # visualization
    listLogLiks = []
    listLogLiks = parseLogs(NUM_MAP_ITERS)
    plotList(listLogLiks)
        
    print 'model built: ', pathToModelPrevStep
    return     pathToModelPrevStep   
    
    
    
def parseLogs(NUM_MAP_ITERS):
    listLogs = []
    
    for i in range(NUM_MAP_ITERS): 
        logName =  'log' + MAP_EXT + str(i+1)
              # parse Log: 
        log = parseLogLik(logName)
        listLogs.append(log)
        
   
    return listLogs  

if __name__ == '__main__':
    

    
   # pathAdaptationData = '/Users/joro/Documents/Phd/UPF/adaptation_data_NOT_CLEAN/HTS_japan_female'

    pathAdaptationData = os.path.join(PATH_TO_CLEAN_ADAPTDATA, MODEL_NAME)
#     pathAdaptationData = '/Users/joro/Documents/Phd/UPF/adaptation_data_NOT_CLEAN/syllablingDB'
    
#     adaptedDict = os.path.join(pathAdaptationData,'all_pronunciation_dict.adapted' )
    
    pathToAllMlf=  os.path.join(pathAdaptationData, 'all.phn.mlf')
    
    
    #######################
#     business logic:
    
    # phoneAnno to pathToAllMlf
    sonicVisTextPhnDir2mlf(pathAdaptationData, pathToAllMlf)
    
#     pathToAllMlf=  os.path.join(pathAdaptationData, 'all.phn.mlf')
    adapt(pathAdaptationData,  pathToAllMlf, PATH_TO_OUTPUT, MODEL_NAME)
    
   
            
            