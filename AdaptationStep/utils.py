'''
Created on May 7, 2014

@author: joro
'''


import glob
import os


def createPhoneAnno():
    '''
    creates phoneAnno files of one-phoneme only. from file name
    '''
    
    os.chdir("/Users/joro/Documents/Phd/UPF/adaptation_data_soloVoice/kani_karaca-all_VOCALS/")
    
    for file in glob.glob("*.wav"):
        fileTokens = file.split("_")
        fileBaseN = os.path.splitext(file)[0]
        
        outputFileHandle = open(fileBaseN + '.phoneAnno', 'w')
        outputFileHandle.write(fileTokens[-2])
    
        outputFileHandle.close()