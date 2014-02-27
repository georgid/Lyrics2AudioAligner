'''
Created on Feb 27, 2014

@author: joro
'''

import codecs
import sys
from turkishLyrics2METULyrics import turkishScriptWord2METUScriptWord
from turkishLyrics2METULyrics import grapheme2Phoneme
    
# converts turkish script lyrics to phonetic dictinary 
# @param: inputFileName - one-line file with lyrics

def turkishScriptLyrics2phoneticDict(inputFileName, outputFileName):
    
    inputFileHandle = codecs.open(inputFileName, 'r', 'utf-8')
    outputFileHandle = open(outputFileName, 'w')
    
    lyrics = inputFileHandle.read()
    lyrics = lyrics.replace('\n', ' ')    
    
    words = lyrics.split()
    for i in range(len(words)):
        words[i] = turkishScriptWord2METUScriptWord(words[i])
       
       # write the word
        outputFileHandle.write(words[i])
        outputFileHandle.write("\t")
        
        # list of METU phonemes for current word
        phonemeList = grapheme2Phoneme(words[i])
        for phoneme in phonemeList:
            outputFileHandle.write(phoneme)
            outputFileHandle.write(" ")
        # new line for new word
        outputFileHandle.write('\n')
    
            
    inputFileHandle.close()
    outputFileHandle.close()  
    return


if __name__ == '__main__':
    
     turkishScriptLyrics2phoneticDict(sys.argv[1], sys.argv[2])
