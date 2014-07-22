# -*- coding: utf-8 -*-
'''
Created on Apr 14, 2014

@author: joro
'''
import os
import multipleGauss
import subprocess
import shutil
from Tools import *
from matplotlib.pyplot import *
from utilsLyrics.Tools import listWavFiles, plotList
from combineTxtIntoPrompts import callHRestNTimes
from test.sortperf import doit

INPUT_HTK_MODEL ='/Users/joro/Documents/Phd/UPF/METUdata/model_output/hmmdefs'
OUTPUTMODELPATH='/Users/joro/Documents/Phd/UPF/METUdata/model_output/multipleGaussians/'


PATH_TO_SCRIPTS = '/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/'
PATH_TO_CONFIG = PATH_TO_SCRIPTS + 'input_files//config'
HMM_LIST = PATH_TO_SCRIPTS + 'interim_files/monophones1'


TRAIN_DIR_WAV='/Users/joro/Documents/Phd/UPF/METUdata/speech-text-all-georgi'

'''
increase num Gaussins from current to 
@parameter maxNumGaussians
'''
def increaseNumGaussians(maxNumGaussians):
    
    
    inputModelURINextNumGauss = INPUT_HTK_MODEL
    
    for toNumGaussians in range(2,maxNumGaussians):
        
        outputModelFolder = os.path.join(OUTPUTMODELPATH, 'hmmdefs' + str(toNumGaussians) )
        
        # make dir where we put model output
        if not os.path.isdir(outputModelFolder):
            os.mkdir(outputModelFolder)
        
        # create codetrain list
        HHedScript = os.path.join( os.path.abspath('.'), 'increaseNumGaussiansTo' + str(toNumGaussians)  + '.cmd' )
        command = [ '/usr/local/bin/HHEd', '-H' , inputModelURINextNumGauss, '-M', outputModelFolder , HHedScript, HMM_LIST]
    
        pipe = subprocess.Popen(command)
        pipe.wait()
        
        inputModel = outputModelFolder + '/hmmdefs'
        
        # repeat HЕRest 3 times
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
        



def increaseOneGaussian(toNumGaussians, numReestimIters, pathToInputModel, outputModelFolder, phoneLevelAnno_uri, codeTrainURI, hmmlistURI):
    
#     for toNumGaussians in range(2,toNumGaussians):
    logName = 'log_split'
    currLogHandle = open(logName, 'w')
    currLogHandle.flush()
    
    # make dir where we put model output
    if not os.path.isdir(outputModelFolder):
        os.mkdir(outputModelFolder)
    
    # create codetrain list
    path = os.path.abspath('..') + '/multipleGauss/'
    HHedScript = os.path.join(path , 'increaseNumGaussiansByOne' +  '.cmd' )
    command = [ '/usr/local/bin/HHEd',  '-A', '-T', '1', '-H' , pathToInputModel, '-M', outputModelFolder , HHedScript, hmmlistURI]

    pipe = subprocess.Popen(command, stdout=currLogHandle)
#     pipe = subprocess.Popen(command)

    pipe.wait()
    currLogHandle.close()
    
    inputModel = outputModelFolder + '/hmmdefs'
    
    # repeat HЕRest 3 times
    return  callHRestNTimes(toNumGaussians, numReestimIters, outputModelFolder, inputModel, phoneLevelAnno_uri, codeTrainURI, hmmlistURI )
    
        
        
# '''
# plots a list as a simple plot
# '''
# def plotList(listOfPlots):
#     figure()
#     # original model
#     plot(listOfPlots, 'g')
#     # adapted model
#     show()


 # parse logs    
def parseLogs(toNumGaussians, numReestimIters):
    listLogs = []
    
    for i in range(numReestimIters): 
        logName = 'log_numGauss_' + str(toNumGaussians) + '_iter' + str(i) +  '.txt'
              # parse Log: 
        log = parseLogLik(logName)
        listLogs.append(log)
        
   
    return listLogs


'''
parse logLik from output of HERest
'''
def parseLogLik(pathToLogFile):
    
    # read logs
    from Tools import loadFileWithColumns
    content = loadFileWithColumns(pathToLogFile, 1)
    logLik = content[-16][0].split()[-1]
    
    log = float(logLik)
    return log


def doit(numReestimIters, numGaussians, pathToInputModel, outputmodelPATH, phoneLevelAnno_uri= PATH_TO_SCRIPTS + 'interim_files/phones0.mlf', codeTrainURI='/tmp/train.scp', hmmlistURI=HMM_LIST ) :
    
    
    
    # all log liks
    totalListLogLiks = []
    

    for toNumGaussians in range(2,numGaussians):
        outputModelFolder = os.path.join(outputmodelPATH, 'hmmdefs' + str(toNumGaussians) )
    

        lastOutputModelURI= increaseOneGaussian(toNumGaussians, numReestimIters, pathToInputModel, outputModelFolder, phoneLevelAnno_uri, codeTrainURI, hmmlistURI)
        
        # upload number
        pathToInputModel = lastOutputModelURI
   
        listLogLiks = []
        listLogLiks = parseLogs(toNumGaussians, numReestimIters)
        
        totalListLogLiks.extend(listLogLiks)
    
    plotList(totalListLogLiks)
        

if __name__ == '__main__':
    
# generate /tmp/train.scp
    listWavFiles( TRAIN_DIR_WAV  , '/tmp/blah', '/tmp/train.scp')
    
    numReestimIters = 10
    numGaussians = 10 
    doit(numReestimIters, numGaussians, INPUT_HTK_MODEL, OUTPUTMODELPATH )
    
#     increaseNumGaussians(5)