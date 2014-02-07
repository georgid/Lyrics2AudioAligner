# -*- coding: utf-8 -*-
'''
Created on Feb 6, 2014

@author: joro
'''

import unidecode
import re
import os
import codecs

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
# @param: inputFileName - one-line file with lyrics
def turkishScriptLyrics2METUScriptLyrics(lyrics):
#     wordList = re.findall(r'\w+', lyrics)
    list = lyrics.split()
#     wordSequence =  wordList.split()
    for i in range(len(list)):
        list[i] = turkishScriptWord2METUScriptWord(list[i])
    return " ".join(list).strip()
    
    
    
# converts turkish script lyrics to phoneme-level 
# @param: inputFileName - one-line file with lyrics
def turkishScriptLyrics2METUphonemes(inputFileName, outputFileName):
    
    inputFileHandle = codecs.open(inputFileName,'r','utf-8')
    outputFileHandle = open(outputFileName,  'w')
    
    lyrics = inputFileHandle.read()
    lyrics = lyrics.replace('\n',' ')    
    
    words = lyrics.split()
    for i in range(len(words)):
        words[i] = turkishScriptWord2METUScriptWord(words[i])
       
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


def lyrics2mlf(lyricsFileName ):
    # lyrics to METU 
    
    # generate phone level 
    
    
    # return dictionary
    
    # return phoneme-level mlfFile

    return






if __name__ == '__main__':
# TODO:     arg parse 
# TODO:     generate word - phoneme list

# call 
# lyrics2mlf(lyricsFileName ):

    wordList = u'Kapına Kapına'   
    convertedList =  turkishScriptLyrics2METUScriptLyrics(wordList)
    print convertedList
    
    print grapheme2Phoneme('kapIna')
    
    turkishScriptLyrics2METUphonemes('/Users/joro/Downloads/test1.txt','/Users/joro/Downloads/test1.blah')
    