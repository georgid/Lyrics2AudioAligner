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
averg error for begin Ts of phrase. 
TODO: averg error for end Ts of phrase (not done yet)
TODO: combine both
'''
def evalPhraseLevelError(phraseLevelAnno, htkAlignedFile  ):
    
    sumDifferences = 0;
    matchedWordCounter = 0.0;
    
    # load both files 
    annotationPhraseList = TextGrid2WordList(phraseLevelAnno)
    detectedWordList= mlf2WordAndTsList(htkAlignedFile)
    if len(detectedWordList) == 0:
        print htkAlignedFile + 'is empty!'
        exit
    
    
    # remove sp and sil entries from word detectedWordList
    
    detectedWordListNoPauses = []   #result 
    for detectedTsAndWrd in detectedWordList:
        if detectedTsAndWrd[1] != 'sp' and detectedTsAndWrd[1] != 'sil':
            detectedWordListNoPauses.append(detectedTsAndWrd)
            
    
    # find start words of annotationPhraseList
    firstWords = [] # result :  first words in phrases 
    currentWordNumber = 0
    for tsAndPhrase in annotationPhraseList:
        if tsAndPhrase[1] == "": # skip empy words
            continue
        tsAndPhrase[1] = tsAndPhrase[1].strip()
        words = tsAndPhrase[1].split(" ")
        numWordsInPhrase = len(words)
        
        # calc difference
        annotatedPhraseBEginTs = tsAndPhrase[0]
        detectedPhraseBeginTs = detectedWordListNoPauses[currentWordNumber][0]
        
        currdifference = abs(float(annotatedPhraseBEginTs) - float(detectedPhraseBeginTs))
        matchedWordCounter +=1.0
        sumDifferences = sumDifferences + currdifference
        
        
        currentWordNumber +=numWordsInPhrase
    
    return sumDifferences/matchedWordCounter
        
        
        
    
    # eval avrg error
    
    
    
    

##################################################################################

if __name__ == '__main__':
    
    
    PATH_TO_EVAL_FILE = '/Users/joro/Documents/Phd/UPF/adaptation_data_NOT_CLEAN/HTS_japan_female/'
    audioName = 'nitech_jp_song070_f001_070'  
    baseNameAudioURI = os.path.join(PATH_TO_EVAL_FILE + audioName)
    
    diff = evalPhraseLevelError(baseNameAudioURI)
    print diff
    
    ############# FROM HERE ON: old testing code for word-level eval 
#     tmpMLF= '/Users/joro/Documents/Phd/UPF/turkish-makam-lyrics-2-audio-test-data/muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde_nakarat2_from_192.962376_to_225.170507.phone-level.output'
#     listWordsAndTs = mlf2WordAndTsList(tmpMLF)
#   
#     
#     
#   
# # TODO: error in parsing of sertan's textGrid
# # TODO: think about sil. Discard in counting
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
    