'''
Created on Feb 20, 2014

@author: joro
'''

import os
import sys

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
    
if __name__ == '__main__':
    combineTxtIntoPrompts(sys.argv[1],sys.argv[2])