'''
Created on Feb 20, 2014

@author: joro
'''

import os
import sys
from Adapt import PATH_TO_CONFIG, PATH_TO_SCRIPTS, HMM_LIST
import subprocess

def combineTxtIntoPrompts(pathToDirWithTxt, pathForOutput):
    # get all files in .txt
    
    outputFileHanlde = open(pathForOutput, 'w')
    
    for root, dirs, files in os.walk(pathToDirWithTxt):
        
        for file in files:
            if file.endswith(".txt") and "-" in file:
                fullFileName = os.path.join(root, file)
                fileHandle = open(fullFileName, 'r')
                fileContents = fileHandle.read()
                fileContents = fileContents.rstrip()
                outputOneFile = os.path.splitext(file)[0] + " " + fileContents + "\n"
                outputFileHanlde.write(outputOneFile)
                
    fileHandle.close()
    outputFileHanlde.close()
    return 



'''
reestimate model @numReestimIters
writes output to log
'''

def callHRestNTimes(toNumGaussians, numReestimIters, outputModelFolder, inputModel, phoneLevelAnno_uri, codeTrainURI, hmmlistURI):
   
    for i in range(numReestimIters):
        
        logName = 'log_numGauss_' + str(toNumGaussians) + '_iter' + str(i) + '.txt'
        currLogHandle = open(logName, 'w')
        currLogHandle.flush()
        outputModeSubFolder = outputModelFolder + '/iter' + str(i)
        
        # create dir
        if not os.path.isdir(outputModeSubFolder):
            os.mkdir(outputModeSubFolder)
        # HERest
        commandHErest = ['/usr/local/bin/HERest', '-A', '-D', '-T', '1', '-C', PATH_TO_CONFIG, '-I', phoneLevelAnno_uri, '-t', 
            '250.0', '150.0', '1000.0', '-S', codeTrainURI, '-H', PATH_TO_SCRIPTS + "/interim_files/hmm0/macros", '-H', inputModel,  '-M', outputModeSubFolder, hmmlistURI]
#         pipe2 = subprocess.Popen(commandHErest, stdout=currLogHandle)
        pipe2 = subprocess.Popen(commandHErest)

        pipe2.wait()
        currLogHandle.close()
        
        #        update the model name for next iteration 
        inputModel = os.path.join(outputModeSubFolder, 'hmmdefs')
    
    return inputModel

    
if __name__ == '__main__':
    combineTxtIntoPrompts(sys.argv[1],sys.argv[2])