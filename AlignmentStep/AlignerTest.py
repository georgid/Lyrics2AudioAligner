'''
Created on Sep 23, 2015

@author: joro
'''
from Aligner import Aligner
import os.path

MODEL_URI = os.path.abspath('model/hmmdefs9gmm9iter')

import sys


parentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__) ), os.path.pardir)) 

pathHMMDuration = os.path.join(parentDir, 'JingjuAlignment')
if pathHMMDuration not in sys.path:
    sys.path.append(pathHMMDuration)

from lyricsParser import divideIntoSectionsFromAnno, loadLyricsFromTextGridSentence



if __name__ == '__main__':
    
    # LOAD LYRICS
    lyricsTextGrid = 'dan-xipi_01.TextGrid'
    listSentences = divideIntoSectionsFromAnno(lyricsTextGrid)
    lyrics = loadLyricsFromTextGridSentence(listSentences[0])
    
    URIrecordingWav = 'dan-xipi_01_32.511032007_51.9222930007.wav'
    # TODO: generate this TextGrid
    lyricsTextGridSentence = 'dan-xipi_01_32.511032007_51.9222930007.TextGrid'
    withSynthesis = 0
    
    # align
    outputHTKPhoneAlignedURI = Aligner.alignOnechunk(MODEL_URI, URIrecordingWav, lyrics,  lyricsTextGridSentence,  '/tmp/', withSynthesis)
    