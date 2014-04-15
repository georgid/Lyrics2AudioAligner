'''
Created on Apr 14, 2014

@author: joro
'''
import os
import multipleGauss
import subprocess
from listWavFiles import listWavFiles
import shutil

INPUT_HTK_MODEL ='/Users/joro/Documents/Phd/UPF/METUdata/model_output/hmmdefs'
OUTPUTMODELPATH='/Users/joro/Documents/Phd/UPF/METUdata/model_output/multipleGaussians/'


PATH_TO_SCRIPTS = '/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/'
PATH_TO_CONFIG = PATH_TO_SCRIPTS + 'input_files//config'
HMM_LIST = PATH_TO_SCRIPTS + 'interim_files/monophones1'


TRAIN_DIR_WAV='/Users/joro/Documents/Phd/UPF/METUdata/speech-text-all-georgi'


def increaseNumGaussians(maxNumGaussians):
    
    

    
    inputModelURINextNumGauss = INPUT_HTK_MODEL
    
    for toNumGaussians in range(2,maxNumGaussians):
        outputModelFolder = os.path.join(OUTPUTMODELPATH, 'hmmdefs' + str(toNumGaussians) )
        
        if not os.path.isdir(outputModelFolder):
            os.mkdir(outputModelFolder)
        
        # create codetrain list
        HHedScript = os.path.join( os.path.abspath('.'), 'increaseNumGaussiansTo' + str(toNumGaussians)  + '.cmd' )
        command = [ '/usr/local/bin/HHEd', '-H' , inputModelURINextNumGauss, '-M', outputModelFolder , HHedScript, HMM_LIST]
    
        pipe = subprocess.Popen(command)
        pipe.wait()
        
        inputModel = outputModelFolder + '/hmmdefs'
        
        # repeat HRest 3 times
        for i in range (3):
             
            outputModeSubFolder =  outputModelFolder + '/iter'  + str(i)    
            if not os.path.isdir(outputModeSubFolder):
                 os.mkdir(outputModeSubFolder)
            
            commandHErest = ['/usr/local/bin/HERest', '-A', '-D', '-T', '1', '-C', PATH_TO_CONFIG, '-I', PATH_TO_SCRIPTS + 'interim_files/phones0.mlf', '-t', \
                            '250.0', '150.0', '1000.0', '-S', '/tmp/train.scp',  '-H', inputModel ,  '-M', outputModeSubFolder, HMM_LIST]
            
    
            pipe2 =  subprocess.Popen(commandHErest)
            pipe2.wait()
             
            #        rename the model to hmmdefs + NumIteration
            inputModel = os.path.join(outputModeSubFolder , 'hmmdefs')
        
        # next num gaussians
        inputModelURINextNumGauss = inputModel
        

# increase number of Gaussians: 


# reestimate
    
    


if __name__ == '__main__':
    
# generate /tmp/train.scp
    listWavFiles( TRAIN_DIR_WAV  , '/tmp/blah', '/tmp/train.scp')
    
    increaseNumGaussians(5)