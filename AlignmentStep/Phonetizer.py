# -*- coding: utf-8 -*-
'''
Created on Mar 22, 2014

@author: joro
'''


import codecs
import sys
from utils.Utils import *



'''
Converts the turkish script into METUbet letters. 
Then the METUBet is phonetized into METUBet phonemes.
 
'''
class Phonetizer(object):
    
     
     
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
      "\," : '',
      "_":''
     
    }
       

        '''
            Just replace letters by corresponding names of phoneme models
        
            # TODO: More carefull distinction between variants. e. g. # disctinction between NN and N
         
        '''
        telugulLookupTable = {
                       'a': 'AA',
                       'e': 'E',
                       'ee':'IY',
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
                       'h': '',
                       'k': 'KK',
                       'l': 'LL',
                       'm': 'M',
                       'n': 'NN',
                       'p': 'P',
                       'r': 'RR',
                       's': 's',
                       't': 'T',
                       'v': 'VV',
                       'y': 'Y',
                       'z': 'Z',
                       'ch': 'TS',
                       'f': 'f',
                       'j': 'DJ'
                       }
       
        def __init__(self):
        
            return
        
 
    



        # converts non-unicode chars into METU-defined chars. 
        # here METU paper    
        @staticmethod
        def turkishScriptWord2METUScriptWord(turkishWord): 
                
            
            s = list(turkishWord)
        
            # combine two-char Diaresis
            combinedList = Phonetizer.combineDiaresisChars(s)
                 
            
            # convert to METU
            for i in range(len(combinedList)):
                if combinedList[i] in Phonetizer.lookupTable:
                    combinedList[i] = Phonetizer.lookupTable[combinedList[i]]
                else:
                    combinedList[i] = combinedList[i].lower()
                    
            
            return "".join(combinedList)
        
        # convert to METU script a string of words

    
    
           # if there are diaresis expressed as two chars in utf, combines them together
           # @param - listA - list with letters of a word
           # @return listWithCombined  
        @staticmethod
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
        
        @staticmethod
        def grapheme2Phoneme( METUword):
            
            s = list(METUword)
        
            for i in range(len(s)):
                if s[i] in Phonetizer.telugulLookupTable:
                    s[i] = Phonetizer.telugulLookupTable[s[i]]
                else:
                    s[i] = "NON-EXISTENT"
                    sys.exit("grapheme", s[i], "not in gpraheme-to-phoneme lookup table")
                    
            return s
            
            
            
            
            
            '''
             convert turkish scritp to METU script. used in word-level annotation of lyrics in audio
        # @param: string with lyrics in turkish. checks if already in unicode
        '''
        @staticmethod
        def turkishScriptLyrics2METUScriptLyrics(lyrics, outputFileName):
        
            if not isinstance(lyrics, unicode):
                lyrics = unicode(lyrics,'utf-8')
            
            lyrics = lyrics.replace('\n', ' ')
            list = lyrics.split()
        #     wordSequence =  wordList.split()
            for i in range(len(list)):
                list[i] = Phonetizer.turkishScriptWord2METUScriptWord(list[i])
            
        
            processedLyrics = " ".join(list).strip()
        
            outputFileHandle = open(outputFileName, 'w')
            outputFileHandle.write(processedLyrics)
            outputFileHandle.close()
            return processedLyrics
        
        
            # same as turkishScriptLyrics2METUScriptLyrics. but takes as input file
            #  @param: inputFileName - one-line file with lyrics
        @staticmethod
        def turkishScriptLyrics2METUScriptLyricsFile(inputFileName, outputFileName):
        
            inputFileHandle = codecs.open(inputFileName, 'r', 'utf-8')
            
            
            lyrics = inputFileHandle.read()
            lyrics = lyrics.replace('\n', ' ')
            
            METUlyrics = Phonetizer.turkishScriptLyrics2METUScriptLyrics(lyrics, outputFileName)
        
            inputFileHandle.close()
            
             
            return METUlyrics
        

                # converts METU lyrics to phonetic dictinary 
        # @param: inputFileName - one-line file with lyrics
        @staticmethod        
        def METULyrics2phoneticDict(inputFileName, outputFileName):
            
            pronunciationList = []
            
            inputFileHandle = open(inputFileName,'r')
            outputFileHandle = open(outputFileName,  'w')
            
            METUlyrics = inputFileHandle.read()
            METUlyrics = METUlyrics.replace('\n',' ')    
            
            words = METUlyrics.split()
            
            # sort and uniq the words
            uniqWords = list(set(words))
            uniqWords.sort()
            
            for word in uniqWords:
                
                # list of METU phonemes for current word
                phonemeList = Phonetizer.grapheme2Phoneme(word)
                
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
            
                    
            inputFileHandle.close()
            return

        
