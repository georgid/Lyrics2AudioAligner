'''
Created on Mar 5, 2014

@author: joro
'''

from evaluation.TextGrid_Parsing import TextGrid2Dict, TextGrid2WordList


'''
parse output of alignment in mlf format ( with words) 
output: words with begin and end ts 

# TODO: change automatically extension from txt to mlf

''' 


def mlf2List(inputFileName):
    inputFileHandle = open(inputFileName)
    
    listWordsAndTs = []
        
    # when reading lines from MLF, skip first 2 and last
    allLines = inputFileHandle.readlines()
    
    
    # skip first two and last
    for line in allLines:
        
        tokens =  line.split(" ")
        if len(tokens) != 4:
            continue
        startTime = float(tokens[0])/10000000
        wordMETU = tokens[3].strip()
        listWordsAndTs.append([startTime, wordMETU])
         
    inputFileHandle.close()
    return listWordsAndTs

'''
For now works only with begin ts
'''
def wordsList2avrgTxt(annotationWordList, detectedWordList):
    
    sumDifferences = 0;
    matchedWordCounter = 0;
    
    # parse annotation word ts and compare each with its detected
    for tupleWordAndTs in annotationWordList:
        for tupleDetectedWordAndTs in  detectedWordList:
            
            if tupleWordAndTs[1] == tupleDetectedWordAndTs[1]:
                currdifference = abs(tupleWordAndTs[0] - tupleDetectedWordAndTs[0])
                matchedWordCounter +=1
                sumDifferences = sumDifferences + currdifference
                # from beginning of list till first matched word
                break
    return sumDifferences/matchedWordCounter
            
            
            
    return



if __name__ == '__main__':
    tmpMLF= '/tmp/phone-level.output'
  
# TODO: error in parsing of sertan's textGrid
# TODO: think about sil. Discard in counting
#     textGrid = '/Users/joro/Documents/Phd/UPF/turkish-makam-lyrics-2-audio-test-data/muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde.TextGrid'
    textGrid='/Volumes/IZOTOPE/adaptation_data/kani_karaca-cargah_tevsih.TextGrid'
    
    listWordsAndTsAnnot = TextGrid2WordList(textGrid)
    listWordsAndTs = mlf2List(tmpMLF)
    
    annotationWordList = [[0.01, 'sil'], [0.05, 'rUzgar'], [0.9,'Simdi']]
    avrgDiff = wordsList2avrgTxt(annotationWordList,listWordsAndTs)
    
    
    print avrgDiff
    