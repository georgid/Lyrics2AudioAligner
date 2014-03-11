# -*- coding: utf-8 -*-
'''
Created on Feb 6, 2014

@author: joro
'''

# import unidecode
import re
import os
import codecs
import sys
import unicodedata

# lookupTable for conversion deom turkish to METU

lookupTable = {
    # soft g
         u'\u011f' : 'G',
    # Ğ
        u'\u011e' : 'G',
    # ı 
        u'\u0131' : 'I',
        'I':'I',
     
    # İ 
        u'\u0130' : 'i',
    # ö
        u'\u00f6' : 'O',
        u'o\u0308' : 'O',
        
   #  Ö  
        u'\u00d6' : 'O',
        u'O\u0308' : 'O',
    
    # ü 
        u'\u00fc' : 'U',
        u'u\u0308' : 'U',
        
    # Ü 
        u'\u00dc' : 'U',
        u'U\u0308' : 'U',
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
      "\'": '',
      "\," : ''
     
    }
       

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
    



# converts non-unicode chars into METU-defined chars. 
# here METU paper    
def turkishScriptWord2METUScriptWord(turkishWord): 
        
    
    s = list(turkishWord)

    # combine two-char Diaresis
    combinedList = combineDiaresisChars(s)
         
    
    # convert to METU
    for i in range(len(combinedList)):
        if combinedList[i] in lookupTable:
            combinedList[i] = lookupTable[combinedList[i]]
        else:
            combinedList[i] = combinedList[i].lower()
            
    
    return "".join(combinedList)

# convert to METU script a string of words

    
    
   # if there are diaresis expressed as two chars in utf, combines them together
   # @param - listA - list with letters of a word
   # @return listWithCombined  
def combineDiaresisChars(listA):
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

def grapheme2Phoneme(METUword):

    
    
    
    
    s = list(METUword)

    for i in range(len(s)):
        if s[i] in METUlookupTable:
            s[i] = METUlookupTable[s[i]]
        else:
            s[i] = "NON-EXISTENT"
            
    return s
    
    
    
    
    
    '''
     convert turkish scritp to METU script. used in word-level annotation of lyrics in audio
# @param: string with lyrics in turkish
    Optionally this function can be called with lyrics instead of turkishScriptLyrics2METUScriptLyricsFile  
'''

def turkishScriptLyrics2METUScriptLyrics(lyrics, outputFileName):
    
#     lyrics = unicode(lyrics,'utf-8')
    
    lyrics = lyrics.replace('\n', ' ')
    list = lyrics.split()
#     wordSequence =  wordList.split()
    for i in range(len(list)):
        list[i] = turkishScriptWord2METUScriptWord(list[i])
    

    processedLyrics = " ".join(list).strip()

    outputFileHandle = open(outputFileName, 'w')
    outputFileHandle.write(processedLyrics)
    outputFileHandle.close() 

   
    
    # same as turkishScriptLyrics2METUScriptLyrics. but takes as input file
    #  @param: inputFileName - one-line file with lyrics
def turkishScriptLyrics2METUScriptLyricsFile(inputFileName, outputFileName):

    inputFileHandle = codecs.open(inputFileName, 'r', 'utf-8')
    
    
    lyrics = inputFileHandle.read()
    lyrics = lyrics.replace('\n', ' ')
    
    turkishScriptLyrics2METUScriptLyrics(lyrics, outputFileName)

    inputFileHandle.close()
    
     
    return
    





if __name__ == '__main__':
# TODO:     arg parse 
# TODO:     generate word - phoneme list

# call 
# lyrics2mlf(lyricsFileName ):

#     wordList = u'Kudûmün rahmet-i zevk u safâdır yâ Resûl Allah Zuhûrun derd-i uşşâkâ devâdır yâ Resûl Allah Hüdâî\'ye şefaat kıl, eer zâhir eer bâtın Kapına intisâb etmiş gedâdır yâ Resûl Allah'
# 
#     convertedList =  turkishScriptLyrics2METUScriptLyrics(wordList)
#     print convertedList
#     
#     print grapheme2Phoneme('kapIna')
#     
#     turkishScriptLyrics2phoneticDict(sys.argv[1], sys.argv[2])
    
        turkishScriptLyrics2METUScriptLyricsFile(sys.argv[1], sys.argv[2])


#         turkishScriptLyrics2METUScriptLyrics(u"Rüzgâr söylüyor şimdi o yerlerde bizim eski şarkımızı", '/Users/joro/Downloads/phoneme-level.out.mlf')

#         turkishScriptLyrics2METUScriptLyrics(sys.argv[1], sys.argv[2])
        
    
    
    
