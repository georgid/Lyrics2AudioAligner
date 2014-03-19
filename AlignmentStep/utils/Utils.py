'''
Created on Mar 12, 2014

@author: joro
'''
import codecs

    ##################################################################################

    ## TODO: callback function to load code. Put it in a different folder
def loadTextFile( pathToFile):
        
        # U means cross-platform  end-line character
        inputFileHandle = codecs.open(pathToFile, 'rU', 'utf-8')
        
        allLines = inputFileHandle.readlines()

        
        inputFileHandle.close()
        
        return allLines

##################################################################################
def writeListToTextFile(listOfList,headerLine, pathToOutputFile):    
    outputFileHandle = codecs.open(pathToOutputFile, 'w', 'utf-8')
    
    outputFileHandle.write(headerLine)
    
    for listLine in listOfList:
        
        output = ""
        for element in listLine:
            output = output + str(element) + "\t"
        output = output.strip()
        output = output + '\n'
        outputFileHandle.write(output)
    
    outputFileHandle.close()


##################################################################################
        
'''
parse output of alignment in mlf format ( with words) 
output: words with begin and end ts 

# TODO: change automatically extension from txt to mlf

''' 


def mlf2WordAndTsList(inputFileName):
    
    allLines = loadTextFile(inputFileName)
    
    
    listWordsAndTs = []
        
    
    
    # when reading lines from MLF, skip first 2 and last
    for line in allLines[2:-1]:
        
        tokens =  line.split(" ")
        if len(tokens) != 4:
            continue
        startTime = float(tokens[0])/10000000
        wordMETU = tokens[3].strip()
        listWordsAndTs.append([startTime, wordMETU])
         
    return listWordsAndTs
    
    
    