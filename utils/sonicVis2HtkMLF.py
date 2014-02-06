'''
Created on Feb 5, 2014

@author: joro
'''

import os


# TODO: change automatically extension from txt to mlf
def mlf2sonicVisText(inputFileName, outputFileName):
    inputFileHandle = open(inputFileName)
    outputFileHandle = open(outputFileName,  'w')
    
    # when reading lines from MLF, skip first 2 and last
    allLines = inputFileHandle.readlines()[2:-1]

    for line in allLines:
        
        tokens =  line.split(" ")
        output = str(float(tokens[0])/10000000) + "\t" + tokens[2]
        outputFileHandle.write(output)
        
    inputFileHandle.close()
    outputFileHandle.close()
        

def sonicVisText2mlf(inputFileName, outputFileName):

    
    absFileName = os.path.abspath(inputFileName)
    
    absOutputFileName = os.path.abspath(outputFileName)
   
    
    inputFileHandle = open(absFileName)
    outputFileHandle = open(absOutputFileName,  'w')
    
    outputFileHandle.write  ("#!MLF!#\n")
    outputFileHandle.write  ("\"*/kani_karaca-hicaz-durak.lab\"\n")

    allLines = inputFileHandle.readlines()
    
    for i in range( len(allLines) - 1):
        
        tokens =  allLines[i].split("\t")
        nextLineTokens = allLines[i+1].split("\t")
        
        output=str(float(tokens[0])*10000000) +" " + str(float(nextLineTokens[0])*10000000) + " " +  tokens[1]
        outputFileHandle.write(output)
        
    outputFileHandle.write  (".\n")
   
    
    inputFileHandle.close()
    outputFileHandle.close()
    
        

    
    return

if __name__ == '__main__':
    sonicVisText2mlf("/Users/joro/Documents/Phd/UPF/Turkey-makam/kani_karaca-hicaz-durak.annotation.phn.txt","/Users/joro/Documents/Phd/UPF/Turkey-makam/kani_karaca-hicaz-durak.annotation.phn.txt.htk" )
   
    
    mlf2sonicVisText("/Users/joro/Downloads/out.phoneme-level.mlf", "/Users/joro/Downloads/out.test.phoneme-level.txt")
    mlf2sonicVisText("/Users/joro/Downloads/out.phoneme-level.noadapt.mlf", "/Users/joro/Downloads/out.phoneme-level.noadapt.txt")
    
    
    