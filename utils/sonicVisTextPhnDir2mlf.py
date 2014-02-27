'''
Created on Feb 5, 2014

@author: joro
'''

import os
import sys
pathToTools = '/Users/joro/Documents/workspace/Tools'
if pathToTools not in sys.path:
    sys.path.insert(0,pathToTools)
from Tools import walklevel





# TODO: change automatically extension from txt to mlf
def mlf2sonicVisText(inputFileName, outputFileName):
    inputFileHandle = open(inputFileName)
    outputFileHandle = open(outputFileName,  'w')
    
    # when reading lines from MLF, skip first 2 and last
    allLines = inputFileHandle.readlines()

    for line in allLines:
        
        tokens =  line.split("\t")
        output = str(float(tokens[0])/10000000) + "\t" + tokens[1]
        outputFileHandle.write(output)
        
    inputFileHandle.close()
    outputFileHandle.close()
        
# convert from
# SV text format:
#  0.000000000    sil
# to .mlf format
# @param: inputFileName- abs file path and name
def sonicVisText2mlf(inputFileName, outputFileHandle):
  
    
    inputFileHandle = open(inputFileName)
   
    
    inputFileBaseName = os.path.basename(inputFileName)
    nameAndExt = os.path.splitext(inputFileBaseName)
    outputFileHandle.write  ("\"*/")
    outputFileHandle.write  (nameAndExt[0])
    outputFileHandle.write  (".lab\"\n")

    allLines = inputFileHandle.readlines()
    
    for i in range( len(allLines) - 1):
        
        tokens =  allLines[i].split("\t")
        nextLineTokens = allLines[i+1].split("\t")
        
        output=str(float(tokens[0])*10000000) +" " + str(float(nextLineTokens[0])*10000000) + " " +  tokens[1]
        outputFileHandle.write(output)
    
    outputFileHandle.write  (".\n")
        
   
    
    inputFileHandle.close()

    return

# convert all files in a dir from
# SV text format:
#  0.000000000    sil
# to .mlf format
# @param: inputPath - dir with phn Files
# @param outputFileName - abs path and name to file  .mlf 

def sonicVisTextPhnDir2mlf(inputDir, outputFileName):
       
    
    outputFileHandle = open(outputFileName,  'w')
    outputFileHandle.write  ("#!MLF!#\n")

    
#     browse dir inputDir
    for roots, dirs, files in walklevel(inputDir, level=1):
        for inputFileName in files:
            ext = os.path.splitext(inputFileName)[1]
            # search for files with phn extension
            if ".phn" == ext: 
                    inputFileName = os.path.join(inputDir,inputFileName)
                    sonicVisText2mlf(inputFileName, outputFileHandle)
    



    
   
    
   
    outputFileHandle.close()
    
    # end each file  

    
    return




if __name__ == '__main__':

#      sonicVisText2mlf(sys.argv[1], sys.argv[2]) 
    sonicVisTextPhnDir2mlf(sys.argv[1], sys.argv[2])
    
#     sonicVisText2mlf("/Users/joro/Documents/Phd/UPF/Turkey-makam/kani_karaca-hicaz-durak.annotation.phn.txt","/Users/joro/Documents/Phd/UPF/Turkey-makam/kani_karaca-hicaz-durak.annotation.phn.txt.htk" )
#    
#     
#     mlf2sonicVisText("/Users/joro/Documents/Phd/UPF/Turkey-makam/kani_karaca-hicaz-durak.phn", "/Users/joro/Documents/Phd/UPF/Turkey-makam/kani_karaca-hicaz-durak.phn2")
#     
    
    