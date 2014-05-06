'''
Created on Apr 27, 2014

@author: joro
'''
from utilsLyrics.Tools import listWavFiles
import subprocess
from multiprocessing import Pipe
from Adapt import PATH_TO_WAV_CONFIG, PATH_TO_CONFIG
from combineTxtIntoPrompts import callHRestNTimes
import os
import shutil
from tempfile import TMP_MAX
from multipleGauss.toMultipleGaussians import doit, OUTPUTMODELPATH

DATA_URI = '/Volumes/IZOTOPE/sertan_sarki/aranagmes/'

if __name__ == '__main__':

#     wavlist aranagmes
  
    WAVMAFC_URI = '/tmp/codetrain_aranagmes.wav-mfc'
    MFC_URI = "/tmp/codetrain_aranagmes.mfc"
    PROTO_URI = '/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/interim_files/hmm0/NOISE' 
    NOISE_LIST_URI = '/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/interim_files/NOISE'
    listWavFiles(DATA_URI, WAVMAFC_URI , '/tmp/codetrain_aranagmes.mfc')
    phoneLevelAnno_uri = os.path.abspath('aranagmes.mlf')
    
    
    # Init model from proto
    HCopyCommand = \
    ["/usr/local/bin/HCopy", "-C", PATH_TO_WAV_CONFIG,  '-S', WAVMAFC_URI, "-D", "-T", "1" ]
    pipe = subprocess.Popen(HCopyCommand)
    pipe.wait()
     
    HCompV = [ "/usr/local/bin/HCompV", "-C", PATH_TO_CONFIG, "-S", MFC_URI,  "-f", "0.01", "-m", "-D", "-T", "1", "-M", "/tmp/", PROTO_URI ]
    pipe = subprocess.Popen(HCompV)
    pipe.wait()
     
    shutil.move('/tmp/NOISE', '/tmp/model_out/hmmdefs')
 
 
     
    # call HERest 3 times
    callHRestNTimes('1', 3, '/tmp/model_out/', '/tmp/model_out/hmmdefs', phoneLevelAnno_uri, MFC_URI, NOISE_LIST_URI)

# split into many Gaussians   
    
    doit(numReestimIters=2, numGaussians=50, pathToInputModel='/tmp/model_out/iter2/hmmdefs', \
          outputmodelPATH = OUTPUTMODELPATH + '/NOISE/' , phoneLevelAnno_uri=phoneLevelAnno_uri, codeTrainURI=MFC_URI, hmmlistURI=NOISE_LIST_URI )
