'''
Created on Feb 5, 2014

Converts from format: tuple (phoneme and timestamp) 
(as used by  sonic visualizer ) to mlf. 
Currently adjusted according to syllablingDB
@author: joro
'''

import os
import sys
# utilLyrics should be installed as a python library
from Tools import walklevel
pathToTools = os.path.abspath(".")
if pathToTools not in sys.path:
    sys.path.insert(0,pathToTools)

listVocals = ['AA', 'A', 'E', 'EE', 'O', 'IY', 'I', 'U', 'UE' , 'OE' ,  'sil']




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
    
    #  with end ts. at least two lines of vowels needed. For only one vowel annotations this is not the case. But ts are not use by HEREst anyway 
#     for i in range( 1, len(allLines) - 1):
#         
#         tokens =  allLines[i].split("\t")
#         nextLineTokens = allLines[i+1].split("\t")
#         
#         monoPhone = replaceMonophonesNotDefinedInHMMList(tokens[1])
#         output=str(float(tokens[0])*10000000) +" " + str(float(nextLineTokens[0])*10000000) + " " +  monoPhone
#         outputFileHandle.write(output)
     
    #only one line    
    for i in range( len(allLines) ):
        
        tokens =  allLines[i].split("\t")
         
        monoPhone = replaceMonophonesNotDefinedInHMMList(tokens[-1])
        outputFileHandle.write(monoPhone)
        
        
    
    outputFileHandle.write  (".\n")
        
   
    
    inputFileHandle.close()

    return
    '''
    replace all non-vowel monophones with model 'DUMMY'
    '''
def replaceMonophonesNotDefinedInHMMList(monophone):
    monophone  = monophone.rstrip()
    if  monophone in listVocals:
        return monophone + '\n'
    else: 
        return 'DUMMY\n'
    
'''
# convert all files in a dir from
# .phoneAnno SV text format:
#  0.000000000    sil
# to .mlf format
NOTE: all .phoneAnno should have a corresponding .wav file. uses .wav correpsonding to existing .phoneAnno files
# @param: inputPath - dir with .phoneAnno Files
# @param outputFileName - abs path and name to file  .mlf 

'''

def sonicVisTextPhnDir2mlf(inputDir, outputFileName):
       
    
    outputFileHandle = open(outputFileName,  'w')
    outputFileHandle.write  ("#!MLF!#\n")

    
#     browse dir inputDir
    for roots, dirs, files in walklevel(inputDir, level=1):
        for inputFileName in files:
            ext = os.path.splitext(inputFileName)[1]
            # search for files with phn extension
            if ".phoneAnno" == ext: 
                    inputFileName = os.path.join(inputDir,inputFileName)
                    sonicVisText2mlf(inputFileName, outputFileHandle)
    



    
   
    
   
    outputFileHandle.close()
    
    # end each file  

    
    return




if __name__ == '__main__':
    print 'in main'
#      sonicVisText2mlf(sys.argv[1], sys.argv[2]) 
#    sonicVisTextPhnDir2mlf(sys.argv[1], sys.argv[2])
    
#     sonicVisText2mlf("/Users/joro/Documents/Phd/UPF/Turkey-makam/kani_karaca-hicaz-durak.annotation.phn.txt","/Users/joro/Documents/Phd/UPF/Turkey-makam/kani_karaca-hicaz-durak.annotation.phn.txt.htk" )
#    
#     
#     mlf2sonicVisText("/Users/joro/Documents/Phd/UPF/Turkey-makam/kani_karaca-hicaz-durak.phn", "/Users/joro/Documents/Phd/UPF/Turkey-makam/kani_karaca-hicaz-durak.phn2")
#     
    
    