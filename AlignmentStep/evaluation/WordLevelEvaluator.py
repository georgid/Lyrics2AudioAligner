'''
Created on Mar 5, 2014

@author: joro
'''

from evaluation.TextGrid_Parsing import TextGrid2Dict, TextGrid2WordList
from evaluation.textgrid import TextGrid
from SymbTrParser import loadTextFile
from utils.Utils import writeListOfListToTextFile, mlf2WordAndTsList
from lib2to3.btm_utils import tokens
from Aligner import HTK_MLF_ALIGNED_SUFFIX, PHRASE_ANNOTATION_EXT
import os
import sys
from IPython.core.tests.test_formatters import numpy


##################################################################################

'''
calculate evaluation metric
For now works only with begin ts
'''
def wordsList2avrgTxt(annotationWordList, detectedWordList):
    
    sumDifferences = 0;
    matchedWordCounter = 0;
    
    # parse annotation word ts and compare each with its detected
    for tupleWordAndTs in annotationWordList:
        for tupleDetectedWordAndTs in  detectedWordList:
            
            if tupleWordAndTs[1] == tupleDetectedWordAndTs[1]:
                currdifference = abs(float(tupleWordAndTs[0]) - float(tupleDetectedWordAndTs[0]))
                matchedWordCounter +=1
                sumDifferences = sumDifferences + currdifference
                # from beginning of list till first matched word
                break
    return sumDifferences/matchedWordCounter
            
            
            
    return

'''
TODO: eval performance of end timest. only and compare with begin ts. 
'''
def evalPhraseLevelError(phraseLevelAnno, htkAlignedFile  ):
    
    alignmentErrors = []
    
    ######################  
    # prepare list of phrases from ANNOTATION:
    annotationPhraseListA = TextGrid2WordList(phraseLevelAnno)
    
    annotationPhraseListNoPauses = []
    for tsAndPhrase in annotationPhraseListA:
        if tsAndPhrase[2] != "" and not(tsAndPhrase[2].isspace()): # skip empty phrases
                annotationPhraseListNoPauses.append(tsAndPhrase)
    
    if len(annotationPhraseListNoPauses) == 0:
        sys.exit(phraseLevelAnno + ' is empty!')
    
    ####################### 
    # # prepare list phrases from DETECTED:
    detectedWordList= mlf2WordAndTsList(htkAlignedFile)
    
    # remove NOISE and sil entries from word detectedWordList
    detectedWordListNoPauses = []   #result 
    for detectedTsAndWrd in detectedWordList:
        if detectedTsAndWrd[2] != 'sp' and detectedTsAndWrd[2] != 'sil' and detectedTsAndWrd[2] != 'NOISE':
            detectedWordListNoPauses.append(detectedTsAndWrd)
    
    if len(detectedWordListNoPauses) == 0:
        sys.exit(htkAlignedFile + ' is empty!')
    
    # TODO: The whole evaluation, not but numWords, but by word id. ISSUE: 19
  
    
    # find start words of annotationPhraseListNoPauses
    currentWordNumber = 0
    for tsAndPhrase in annotationPhraseListNoPauses:
       
        tsAndPhrase[2] = tsAndPhrase[2].strip()
        words = tsAndPhrase[2].split(" ")
        numWordsInPhrase = len(words)
        
        if numWordsInPhrase == 0:
            sys.exit('phrase with no words in annotation file!')
        
        if  currentWordNumber + 1 > len(detectedWordListNoPauses):
            sys.exit('more words detected than in annotation. No evaluation possible')
            
        currTsandWord = detectedWordListNoPauses[currentWordNumber]
        
        # calc difference phrase begin Ts
        annotatedPhraseBEginTs = tsAndPhrase[0]
        detectedPhraseBeginTs = currTsandWord[0]
        
        currAlignmentError = calcError(annotatedPhraseBEginTs, detectedPhraseBeginTs)
        alignmentErrors.append(currAlignmentError)
        
        # calc difference phrase end Ts
        annotatedPhraseEndTs = tsAndPhrase[1]
        detectedPhraseEndTs = currTsandWord[1]
        
        currAlignmentError = calcError(annotatedPhraseEndTs, detectedPhraseEndTs)
        alignmentErrors.append(currAlignmentError)
        
        #### proceed as many words in annotation as         
        currentWordNumber +=numWordsInPhrase
                
    return  alignmentErrors
        

def calcError(annotatedPhraseBEginTs, detectedPhraseBeginTs):
    currAlignmentError = float(annotatedPhraseBEginTs) - float(detectedPhraseBeginTs)
    currAlignmentError = numpy.round(currAlignmentError, decimals=2)
    return currAlignmentError      
    
    
    
    
    

##################################################################################

if __name__ == '__main__':
    
    
    print "in WordLevelEval"

    
    ############# FROM HERE ON: old testing code for word-level eval 
#     tmpMLF= '/Users/joro/Documents/Phd/UPF/turkish-makam-lyrics-2-audio-test-data/muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde_nakarat2_from_192.962376_to_225.170507.phone-level.output'
#     listWordsAndTs = mlf2WordAndTsList(tmpMLF)
#   
#     
#     
#   
# # TODO: error in parsing of sertan's textGrid
#     textGridFile = '/Users/joro/Documents/Phd/UPF/turkish-makam-lyrics-2-audio-test-data/muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde.TextGrid'
# #     textGridFile='/Volumes/IZOTOPE/adaptation_data/kani_karaca-cargah_tevsih.TextGrid'
# #     textGridFile = '/Users/joro/Documents/Phd/UPF/Example_words_phonemes.TextGrid'
#     textGridFile = '/Users/joro/Documents/Phd/UPF/adaptation_data_soloVoice/04_Hamiyet_Yuceses_-_Bakmiyor_Cesm-i_Siyah_Feryade/04_Hamiyet_Yuceses_-_Bakmiyor_Cesm-i_Siyah_Feryade_gazel.wordAnnotation.TextGrid'
#     
#     
#     
#     
#     listWordsAndTsAnnot = TextGrid2WordList(textGridFile)
#     
#     
#     annotationWordList = [[0.01, 'sil'], [0.05, 'rUzgar'], [0.9,'Simdi']]
#     avrgDiff = wordsList2avrgTxt(annotationWordList,listWordsAndTs)
#     
#     
#     print avrgDiff
    