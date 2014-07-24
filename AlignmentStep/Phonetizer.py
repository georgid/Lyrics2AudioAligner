# -*- coding: utf-8 -*-
'''
Created on Mar 22, 2014

@author: joro
'''


import codecs
import sys
from utils.Utils import *


  


'''
    replace roman transliteration with diacritics by corresponding phoneme models
    UTF=8 MApping TABLE from http://www.alanwood.net/unicode/latin_extended_a.html
    IAST list from http://ebmp.org/p_easyunicode.php 

 
'''
telugulLookupTable = {
               'a': 'AA',
               
                # ā
               u'\u0101':'AA',
               
               'e': 'E',
               
               # ē
               u'\u0113':'E',
               
               
               'i': 'IY',
              
              # ī
               u'\u012b':'IY',
               
               
               'o': 'O',
               # ō
               u'\u014d':'O',
               
               'u': 'U',
               
               # ū
               u'\u016b':'U',
              
               
               
               'b': 'B',
               'c':'CH',
               'd': 'D',
               'g': 'GG',
               'h': 'H',
               'k': 'KK',
               'l': 'LL',
               'm': 'M',
               'n': 'NN',
                # ṅ
               u'\u1e45':'NN',
               
               'p': 'P',
               'r': 'RR',
               # ṛ
               u'\u1e5b':'RR',
               
               # ṝ
               u'\u1e5d':'RR',
              
               's': 'S',
               # ś
               u'\u015b':'S',
               
                # ṣ
               u'\u1e63':'SH',
               
               't': 'T',
                # ṭ
               u'\u1e6d':'T',
               
               'v': 'VV',
               'y': 'Y',
               'z': 'Z',
               'f': 'F',
               'j': 'C',
               
               '-' : '',
               "\'": '',
               "\," : '',
               "_":'',
               "?":''
               }




   # if there are diaresis expressed as two chars in utf, combines them together
   # @param - listA - list with letters of a word
   # @return listWithCombined  
def combineDiaresisChars( listA):
    diaresisIndeces = []
    for i, j in enumerate(listA): 
        if j == u'\u0308':
           diaresisIndeces.append(i)
    
    # transform diaresis
    for indexL in diaresisIndeces:
        diaresisLetter = listA.pop(indexL - 1)
        newLetter = diaresisLetter + u'\u0308'
        listA.insert(indexL - 1, newLetter)

    # remove diaresis    
    counter = 0
    for indexL in diaresisIndeces:
         indexL = indexL - counter;  listA.pop(indexL); counter = counter + 1
    return  listA



def grapheme2Phoneme( word):
#     wprd = word.lower()
    s = list(word)

    # combine two-char Diaresis
    s = combineDiaresisChars(s)                    

    for i in range(len(s)):
        s[i] = s[i].lower()
        if s[i] in telugulLookupTable:
            s[i] = telugulLookupTable[s[i]]
        else:
            sys.exit("grapheme {0} not in gpraheme-to-phoneme lookup table".format(s[i]) )
            
    return s
    

# converts original script lyrics to phonetic dictionary 
# @param: inputFileName - one-line file with lyrics
def lyrics2phoneticDict(words, outputFileName):
    
    pronunciationList = []
    
    outputFileHandle = open(outputFileName,  'w')
    

    
    # sort and uniq the words
    uniqWords = list(set(words))
    uniqWords.sort()
    
    for word in uniqWords:
        
        # list of METU phonemes for current word
        phonemeList = grapheme2Phoneme(word)
        
        # create a pronunciation entry
        wordAndPronunciation = word + "\t"

        for phoneme in phonemeList:
            wordAndPronunciation += phoneme
            wordAndPronunciation += " "
        
        #  here add sp
        wordAndPronunciation += 'sp'
        wordAndPronunciation =  wordAndPronunciation.rstrip()
        wordAndPronunciation +='\n'
        
        pronunciationList.append(wordAndPronunciation)
        
    pronunciationList.append('sil\tsil\n')
    pronunciationList.append('NOISE\tNOISE\n')
       
    writeListToTextFile(pronunciationList, None,  outputFileName )
    outputFileHandle.close()
    
            
    return

        
