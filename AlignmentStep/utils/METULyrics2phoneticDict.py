# -*- coding: utf-8 -*-
'''
Created on Feb 6, 2014

@author: joro
'''

from turkishLyrics2METULyrics import grapheme2Phoneme
import codecs
import sys
    
# converts turkish script lyrics to phonetic dictinary 
# @param: inputFileName - one-line file with lyrics

def METULyrics2phoneticDict(inputFileName, outputFileName):
    
    inputFileHandle = codecs.open(inputFileName,'r','utf-8')
    outputFileHandle = open(outputFileName,  'w')
    
    METUlyrics = inputFileHandle.read()
    METUlyrics = METUlyrics.replace('\n',' ')    
    
    words = METUlyrics.split()
    for i in range(len(words)):
       
       # write the word
        outputFileHandle.write( words[i])
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

    
    METULyrics2phoneticDict(sys.argv[1], sys.argv[2])
    
#     turkishScriptLyrics2METUScriptLyricsFile('/Users/joro/Documents/Phd/UPF/Turkey-makam/kani_karaca-hicaz-durak.phn','/Users/joro/Documents/Phd/UPF/Turkey-makam/kani_karaca-hicaz-durak.phn.out' )
    