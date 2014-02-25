'''
Created on Feb 21, 2014

@author: joro
'''



import os
import sys
import subprocess

def listWavFiles(pathToDirWithTxt, nameCodeTrainFile, nameTrainFile):
    # get all files in .txt
    
    outputFileHanldeTrain = open(nameTrainFile, 'w')
    outputFileHanlde = open(nameCodeTrainFile, 'w')
    
    for root, dirs, files in os.walk(pathToDirWithTxt):
        
        for file in files:
            if file.endswith(".wav"):
                
                wavFileName = os.path.join(root, file)

                baseFileName = os.path.splitext(file)[0]
               
                # derive name of .wrd file             
                mfcFileName = os.path.join(root, baseFileName) + ".mfc"  + "\n"
                
                wavAndMfc = wavFileName + " " +  mfcFileName + "\n"
             
                outputFileHanlde.write(wavAndMfc)
                
                outputFileHanldeTrain.write(mfcFileName)
                
                
               
                
        outputFileHanlde.close()
        
        outputFileHanldeTrain.close()
    return 
    
if __name__ == '__main__':
        listWavFiles(sys.argv[1],sys.argv[2], sys.argv[3] )