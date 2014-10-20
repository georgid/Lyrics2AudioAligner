'''
Created on Oct 8, 2014

@author: joro
'''
from Phonetizer import Phonetizer
from Phoneme import Phoneme



class Syllable():
        ''' syllables class done because in symbolic file lyrics are represented as syllables
        BUT not meant to be used alone, instead Syllable is a part of a Word class
        '''
        def __init__(self, text, noteNum):
            self.text = text
            
#             corresponding note num
            self.noteNum = int(noteNum)
            self.phonemes = None
            self.duration = None
            self.hasShortPauseAtEnd = False
            
        def setHasShortPauseAtEnd (self,hasShortPauseAtEnd): 
            '''
            set if this is last syllable in word
            '''
            self.hasShortPauseAtEnd = hasShortPauseAtEnd
        
        def expandToPhonemes(self):
            '''
            make sure text has no whitespaces
            '''
            
            METUtext = Phonetizer.turkishScriptWord2METUScriptWord(self.text)
            phonemeIDs = Phonetizer.grapheme2Phoneme(METUtext)
            
            self.phonemes = []
            for phonemeID in phonemeIDs:
                self.phonemes.append(Phoneme(phonemeID))
            if self.hasShortPauseAtEnd:
                self.phonemes.append(Phoneme('sp'))
           
            

        def getNumPhonemes(self):
            if self.phonemes == None:
                self.expandToPhonemes()
            return len(self.phonemes)
        
        def getPositionVowel(self):
            '''
            which is the vowel phoneme. 
            check vowels in lookup table
            NOTE: assume only one vowel in syllable. this is true if no diphtongs in language 
            '''
            for i, phoneme in enumerate(self.phonemes):
                if phoneme.isVowel():
                    return i
            return -1
        
        def calcPhonemeDurations(self):
            '''
            durations set to 1, the rest for the vowel.
            
            '''
            if self.phonemes is None:
                self.expandToPhonemes()
                
            vowelPos = self.getPositionVowel()
            
            # THERE should not be such syllable, just in case
            if vowelPos == -1:
                for phoneme in self.phonemes:
#                     no vowel => equal duration for all
                    phoneme.setDuration(self.duration / self.getNumPhonemes())
            else: # one vowel
                for phoneme in self.phonemes:
                       phoneme.duration = 1
                vowelDuration = self.duration - self.getNumPhonemes() + 1
                self.phonemes[self.getPositionVowel()].setDuration(vowelDuration)
