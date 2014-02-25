'''
Created on Feb 20, 2014

@author: joro
'''

import os
import sys
import subprocess

def toPhoneDict(pathToDirWithTxt, pathForOutput):
    # get all files in .txt
    
    outputFileHanlde = open(pathForOutput, 'w')
    
    for root, dirs, files in os.walk(pathToDirWithTxt):
        
        for file in files:
            if file.endswith(".phn"):
                
                phnFileName = os.path.join(root, file)

                baseFileName = os.path.splitext(file)[0]
               
                # derive name of .wrd file             
                wrdFileName = os.path.join(root, baseFileName) + ".wrd"
                
                # derive name of  pronunciation_dict file 
                pronunciation_dictFileName  = os.path.join(root, baseFileName) + ".pronunciation_dict"
                
                pipe = subprocess.Popen(["perl", "/Users/joro/Documents/Phd/UPF/voxforge/myScripts/createPhoneDict.pl", phnFileName, wrdFileName, pronunciation_dictFileName   ])
                
                pronunciation_dictHandle = open(pronunciation_dictFileName, 'r')
                dictContent = pronunciation_dictHandle.read()
                outputFileHanlde.write(dictContent)
                
                
               
                
        outputFileHanlde.close()
    return 
    
if __name__ == '__main__':
        toPhoneDict(sys.argv[1],sys.argv[2] )
    