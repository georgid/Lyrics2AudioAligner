'''
Created on Mar 5, 2014

@author: joro
'''

from evaluation.TextGrid_Parsing import TextGrid2Dict, TextGrid2WordList
from evaluation.textgrid import TextGrid
from SymbTrParser import loadTextFile
from utils.Utils import writeListOfListToTextFile, mlf2WordAndTsList


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
                currdifference = abs(tupleWordAndTs[0] - tupleDetectedWordAndTs[0])
                matchedWordCounter +=1
                sumDifferences = sumDifferences + currdifference
                # from beginning of list till first matched word
                break
    return sumDifferences/matchedWordCounter
            
            
            
    return


##################################################################################

if __name__ == '__main__':
    tmpMLF= '/Users/joro/Documents/Phd/UPF/turkish-makam-lyrics-2-audio-test-data/muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde_nakarat2_from_192.962376_to_225.170507.phone-level.output'
    listWordsAndTs = mlf2WordAndTsList(tmpMLF)
  
    
    
  
# TODO: error in parsing of sertan's textGrid
# TODO: think about sil. Discard in counting
    textGridFile = '/Users/joro/Documents/Phd/UPF/turkish-makam-lyrics-2-audio-test-data/muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde.TextGrid'
#     textGridFile='/Volumes/IZOTOPE/adaptation_data/kani_karaca-cargah_tevsih.TextGrid'
#     textGridFile = '/Users/joro/Documents/Phd/UPF/Example_words_phonemes.TextGrid'
    
    listWordsAndTsAnnot = TextGrid2WordList(textGridFile)
    
    
    annotationWordList = [[0.01, 'sil'], [0.05, 'rUzgar'], [0.9,'Simdi']]
    avrgDiff = wordsList2avrgTxt(annotationWordList,listWordsAndTs)
    
    
    print avrgDiff
    