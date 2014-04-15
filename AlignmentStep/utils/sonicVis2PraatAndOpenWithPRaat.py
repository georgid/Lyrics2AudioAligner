'''
Created on Apr 3, 2014

@author: joro
'''
import sys
import subprocess
import os

#used to open result only after alignemnt algorithm is run. It does not work now !

WORD_ALIGNED_SUFFIX= ".wordAligned"
PHONEME_ALIGNED_SUFFIX= ".phonemeAligned"

PATH_TO_PRAAT = '/Applications/Praat.app/Contents/MacOS/Praat'
# PATH_TO_PRAAT_SCRIPT= '/Users/joro/Documents/Phd/UPF/voxforge/myScripts/praat/loadAlignedResultAndTextGrid'

PATH_TO_PRAAT_SCRIPT= '/Users/joro/Documents/Phd/UPF/voxforge/myScripts/praat/loadAlignedResult'

LYRICS_TXT_EXT = '.txtTur'
PHRASE_ANNOTATION_EXT = '.TextGrid'

if __name__ == '__main__':

    
    command = [ PATH_TO_PRAAT, PATH_TO_PRAAT_SCRIPT, sys.argv[1], sys.argv[2],  sys.argv[2], WORD_ALIGNED_SUFFIX ]
    pipe = subprocess.Popen(command)
    pipe.wait()
    
    # open comparison.TextGrid in  praat. OPTIONAL
    comparisonTextGridURI =  os.path.join(sys.argv[1], sys.argv[2])  + PHRASE_ANNOTATION_EXT
    pipe = subprocess.Popen(["open", '-a', PATH_TO_PRAAT, comparisonTextGridURI])
    pipe.wait()