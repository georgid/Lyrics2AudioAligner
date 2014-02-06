# -*- coding: utf-8 -*-
'''
Created on Feb 6, 2014

@author: joro
'''

import unidecode

# load lyrics file  
def lyrics2mlf(lyricsFileName ):
    # lyrics to METU 
    
    # generate phone level 
    
    
    # return dictionary
    
    # return phoneme-level mlfFile

    return

# converts non-unicode chars into METU-defined chars. 
# here METU paper    
def turkishScript2METU(turkishWord):

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
        u'\u00c7' : 'C'
    }
    
    s = list(turkishWord)

    for i in range(len(s)):
        if s[i] in lookupTable:
            s[i] = lookupTable[s[i]]
        else:
            s[i] = s[i].lower()
            
    
    return "".join(s)

def grapheme2Phoneme(METUword):
    arrayPhonemes = 'blah' 
    return arrayPhonemes 

if __name__ == '__main__':
#     arg parse 

# call 
# lyrics2mlf(lyricsFileName ):

    word = u"Kapına"
    
    

    print turkishScript2METU(word)
    