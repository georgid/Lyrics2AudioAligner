'''
Created on Mar 12, 2014

@author: joro
'''
import codecs
from IPython.utils._tokenize_py2 import Token

    ##################################################################################

    ## TODO: callback function to load code. Put it in a different folder
def loadTextFile( pathToFile):
        
        # U means cross-platform  end-line character
        inputFileHandle = codecs.open(pathToFile, 'rU', 'utf-8')
        
        allLines = inputFileHandle.readlines()

        
        inputFileHandle.close()
        
        return allLines

##################################################################################
def writeListOfListToTextFile(listOfList,headerLine, pathToOutputFile):    
    outputFileHandle = codecs.open(pathToOutputFile, 'w', 'utf-8')
    
    if not headerLine == None:
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
def writeListToTextFile(inputList,headerLine, pathToOutputFile):    
    outputFileHandle = codecs.open(pathToOutputFile, 'w', 'utf-8')
    
    if not headerLine == None:
        outputFileHandle.write(headerLine)
    
    for listLine in inputList:
        outputFileHandle.write(listLine)
    
    outputFileHandle.close()



'''
parse output of alignment in mlf format ( with words) 
output: phonemes with begin and end ts 

# TODO: change automatically extension from txt to mlf

''' 


def mlf2PhonemesAndTsList(inputFileName):
    
    allLines = loadTextFile(inputFileName)
    
    
    listPhonemesAndTs = []
    prevStartTime = -1    
    
    
    # when reading lines from MLF, skip first 2 and last
    for line in allLines[2:-1]:
        
        tokens =  line.split(" ")

        startTime = float(tokens[0])/10000000
        
        # if Praat does not allow insertion of new token with same timestamp. This happend when prev. token was 'sp'. So remove it and insert current
        if (prevStartTime == startTime):
            listPhonemesAndTs.pop()
            
        
        phoneme = tokens[2].strip()
        listPhonemesAndTs.append([startTime, phoneme])
        
        # remember startTime 
        prevStartTime = startTime
         
    return listPhonemesAndTs
    
    
    
def mlf2WordAndTsList(inputFileName):
        
    '''
    parse output of alignment in mlf format ( with words) 
    output: words with begin and end ts 
    NOTE: length of tokens=5 if no -o option is set on HVite
    TODO: change automatically extension from txt to mlf
    ''' 
    
    extracedWordList = []
    
    LENGTH_TOKENS_NEW_WORD= 5
    
    allLines = loadTextFile(inputFileName)
    
    listWordsAndTs = allLines[2:-1]
        
    currentTokenIndex = 0    
    tokens =  listWordsAndTs[currentTokenIndex].split(" ")
    
    while currentTokenIndex < len(listWordsAndTs):
        
        # get begin ts 
        startTime = float(tokens[0])/10000000
        wordMETU = tokens[-1].strip()
        
        # move to next        
        prevTokens = tokens 
        currentTokenIndex += 1
        
        # sanity check
        if currentTokenIndex >= len(listWordsAndTs):
            endTime =  float(prevTokens[1])/10000000
            extracedWordList.append([startTime, endTime, wordMETU])     
 
            break
        
        tokens =  listWordsAndTs[currentTokenIndex].split(" ")
        
        # fast forward phonemes while end of word
        while len(tokens) == LENGTH_TOKENS_NEW_WORD - 1 and currentTokenIndex < len(listWordsAndTs):
            
            # end of word is last phoneme before 'sp' 
            if tokens[2]=="sp":
                # move to next
                currentTokenIndex += 1
                if currentTokenIndex < len(listWordsAndTs):
                    tokens =  listWordsAndTs[currentTokenIndex].split(" ")

                break
            
            prevTokens = tokens 
            currentTokenIndex += 1
            tokens =  listWordsAndTs[currentTokenIndex].split(" ")
        
        # end of word. after inner while loop  
        endTime =  float(prevTokens[1])/10000000
        
        extracedWordList.append([startTime, endTime, wordMETU])     
        
    return extracedWordList    
    
    
    
    
def mlf2WordAndTsList(inputFileName):
        
    '''
    parse output of alignment in mlf format ( with words) 
    output: words with begin and end ts 
    NOTE: length of tokens=5 if no -o option is set on HVite
    TODO: change automatically extension from txt to mlf
    ''' 
    
    extracedWordList = []
    
    LENGTH_TOKENS_NEW_WORD= 5
    
    allLines = loadTextFile(inputFileName)
    
    listWordsAndTs = allLines[2:-1]
        
    currentTokenIndex = 0    
    tokens =  listWordsAndTs[currentTokenIndex].split(" ")
    
    while currentTokenIndex < len(listWordsAndTs):
        
        # get begin ts 
        startTime = float(tokens[0])/10000000
        wordMETU = tokens[-1].strip()
        
        # move to next        
        prevTokens = tokens 
        currentTokenIndex += 1
        
        # sanity check
        if currentTokenIndex >= len(listWordsAndTs):
            endTime =  float(prevTokens[1])/10000000
            extracedWordList.append([startTime, endTime, wordMETU])     
 
            break
        
        tokens =  listWordsAndTs[currentTokenIndex].split(" ")
        
        # fast forward phonemes while end of word
        while len(tokens) == LENGTH_TOKENS_NEW_WORD - 1 and currentTokenIndex < len(listWordsAndTs):
            
            # end of word is last phoneme before 'sp' 
            if tokens[2]=="sp":
                # move to next
                currentTokenIndex += 1
                if currentTokenIndex < len(listWordsAndTs):
                    tokens =  listWordsAndTs[currentTokenIndex].split(" ")

                break
            
            prevTokens = tokens 
            currentTokenIndex += 1
            tokens =  listWordsAndTs[currentTokenIndex].split(" ")
        
        # end of word. after inner while loop  
        endTime =  float(prevTokens[1])/10000000
        
        extracedWordList.append([startTime, endTime, wordMETU])     
        
    return extracedWordList    
    
    
    