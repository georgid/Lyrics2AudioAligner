# -*- coding: utf-8 -*-
'''
Created on Feb 6, 2014

@author: joro
'''

import unidecode
import re
import os
import codecs
import sys

# converts non-unicode chars into METU-defined chars. 
# here METU paper    
def turkishScriptWord2METUScriptWord(turkishWord):

    lookupTable = {
    # g
         u'\u011f' : 'G',
    # Ğ
        u'\u011e' : 'G',
    # ı 
        u'\u0131' : 'I',
     
    #İ 
        u'\u0130' : 'I',
    # ö
        u'\u00f6' : 'O',
   #  Ö  
        u'\u00d6' : 'O',
    
    # ü 
        u'\u00fc' : 'U',
    # Ü 
        u'\u00dc' : 'U',
    # ş 
        u'\u015f' : 'S',
    
    # Ş  
        u'\u015e' : 'S',
   # ç 
        u'\u00e7' : 'C',
    
   # Ç  
        u'\u00c7' : 'C',
    # â 
        u'\u00e2': 'a',
     # Â
        u'\u00c2': 'a',
    
    
    # î
        u'\u00ee': 'i',
     
    # Î  
      u'\u00ce': 'i',
      
          # û
        u'\u00fb': 'u',
     
    # Û  
      u'\u00db': 'u',
      
      '-' : '',
      "\'": ''
        
     
    }
    
    s = list(turkishWord)

    for i in range(len(s)):
        if s[i] in lookupTable:
            s[i] = lookupTable[s[i]]
        else:
            s[i] = s[i].lower()
            
    
    return "".join(s)

# convert to METU script a string of words

     

def grapheme2Phoneme(METUword):

    
    # table 1 from Oe. Salor - Turkish speech corpora and recognition tools developed by porting SONIC: Towards multilingual speech recognition
    
    # TODO: More carefull distinction between variants. e. g. # disctinction between G and GG
    METUlookupTable = {
                       'a': 'AA',
                       'e': 'EE',
                       'i': 'IY',
                       'I': 'I',
                       'o': 'O',
                       'u': 'U',
                       'O': 'OE',
                       'U': 'UE',
                       'b': 'B',
                       'd': 'D',
                       'g': 'GG',
                       'G': '',
                       'h': 'H',
                       'k': 'KK',
                       'l': 'LL',
                       'm': 'M',
                       'n': 'NN',
                       'p': 'P',
                       'r': 'RR',
                       's': 'S',
                       'S': 'SH',
                       't': 'T',
                       'v': 'VV',
                       'y': 'Y',
                       'z': 'Z',
                       'c': 'C',
                       'C': 'CH',
                       'f': 'F',
                       'j': 'J'
                       }
    
    
    
    s = list(METUword)

    for i in range(len(s)):
        if s[i] in METUlookupTable:
            s[i] = METUlookupTable[s[i]]
        else:
            s[i] = "NON-EXISTENT"
            
    return s
    
    
    
    
    
    
# convert turkish scritp to METU script. used in word-level annotation of lyrics in audio
# @param: string with lyrics in turkish 
def turkishScriptLyrics2METUScriptLyrics(lyrics):
#     wordList = re.findall(r'\w+', lyrics)
    list = lyrics.split()
#     wordSequence =  wordList.split()
    for i in range(len(list)):
        list[i] = turkishScriptWord2METUScriptWord(list[i])
    return " ".join(list).strip()
    
    # same as turkishScriptLyrics2METUScriptLyrics. but takes as input file and print into file 
    #  @param: inputFileName - one-line file with lyrics
def turkishScriptLyrics2METUScriptLyricsFile(inputFileName, outputFileName):

    inputFileHandle = codecs.open(inputFileName,'r','utf-8')
    outputFileHandle = open(outputFileName,  'w')
    
    lyrics = inputFileHandle.read()
    lyrics = lyrics.replace('\n',' ')
    
    processedLyrics = turkishScriptLyrics2METUScriptLyrics(lyrics)
#     list = lyrics.split()
# #     wordSequence =  wordList.split()
#     for i in range(len(list)):
#         list[i] = turkishScriptWord2METUScriptWord(list[i])
#     return " ".join(list).strip()
    outputFileHandle.write(processedLyrics)
    inputFileHandle.close()
    outputFileHandle.close()  
    return
    
    
# converts turkish script lyrics to phonetic dictinary 
# @param: inputFileName - one-line file with lyrics

def turkishScriptLyrics2phoneticDict(inputFileName, outputFileName):
    
    inputFileHandle = codecs.open(inputFileName,'r','utf-8')
    outputFileHandle = open(outputFileName,  'w')
    
    lyrics = inputFileHandle.read()
    lyrics = lyrics.replace('\n',' ')    
    
    words = lyrics.split()
    for i in range(len(words)):
        words[i] = turkishScriptWord2METUScriptWord(words[i])
       
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


    wordList = u'Kudûmün rahmet-i zevk u safâdır yâ Resûl Allah Zuhûrun derd-i uşşâkâ devâdır yâ Resûl Allah Hüdâî\'ye şefaat kıl, eer zâhir eer bâtın Kapına intisâb etmiş gedâdır yâ Resûl Allah'

    convertedList =  turkishScriptLyrics2METUScriptLyrics(wordList)
    
    turkishScriptLyrics2phoneticDict(sys.argv[1], sys.argv[2])
    
#     turkishScriptLyrics2METUScriptLyricsFile('/Users/joro/Documents/Phd/UPF/Turkey-makam/kani_karaca-hicaz-durak.phn','/Users/joro/Documents/Phd/UPF/Turkey-makam/kani_karaca-hicaz-durak.phn.out' )
    