'''
Created on Mar 17, 2014

@author: joro
'''
import os
import subprocess
from utils.Utils import mlf2WordAndTsList, writeListOfListToTextFile
from Phonetizer import Phonetizer
import shutil


PHONEME_ALIGNED_SUFFIX= ".phonemeAligned"
WORD_ALIGNED_SUFFIX= ".wordAligned"

PATH_TO_ALIGNMENT_TOOL = os.path.abspath('doForceAligment.sh')
PATH_TO_HCOPY= '/usr/local/bin/HCopy'
PATH_TO_HVITE= '/Users/joro/Documents/Fhg/htk3.4.BUILT/bin/HVite'
PATH_TO_CONFIG_FILES= '/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/input_files/'
PATH_TO_HMMLIST='/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/interim_files/monophones1'

PATH_TO_PRAAT = '/Applications/Praat.app/Contents/MacOS/Praat'
PATH_TO_PRAAT_SCRIPT= '/Users/joro/Documents/Phd/UPF/voxforge/myScripts/praat/loadAlignedResult'


class Aligner():
    '''
    classdocs
    '''


    def __init__(self, pathToHtkModel, pathToAudioFile, lyrics):
        
        self.pathToHtkModel = pathToHtkModel
        self.pathToAudioFile = pathToAudioFile
        self.lyrics = lyrics
    
     ##################################################################################

    '''
    only one audio file and lyrics provided
    @param timeShift: add to start of timstamps (needed tog get real audio timestamp if audio is part of a bigger recording)
    '''
    

    def _createWordMLFandDict(self, baseNameAudioFile):
        #txtTur to METU
    # FIXME: this is quick and dirty place to do that. It is now repeated
        METULyrics = Phonetizer.turkishScriptLyrics2METUScriptLyrics(self.lyrics, baseNameAudioFile + '.txtMETU')
    # create Word-level mlf:
        baneN = os.path.basename(self.pathToAudioFile)
        baneN = os.path.splitext(baneN)[0]
        headerLine = baneN + ' ' + METULyrics
        writeListOfListToTextFile([], headerLine, '/tmp/prompts')
        
        # prompts2mlf
        mlfName = baseNameAudioFile + '.wrd.mlf'
        pipe = subprocess.Popen(['/usr/bin/perl', '/Users/joro/Documents/Phd/UPF/voxforge/HTK_scripts/prompts2mlf', mlfName, '/tmp/prompts'])
        
        # phonetize
        dictName = '/tmp/lexicon2'
        
        Phonetizer.METULyrics2phoneticDict(baseNameAudioFile + '.txtMETU', dictName)
        return (dictName, mlfName )


    def _extractFeatures(self, baseNameAudioFile):
     
        mfcFileName = baseNameAudioFile + '.mfc' 
        pipe= subprocess.Popen([PATH_TO_HCOPY, '-A', '-D', '-T', '1', '-C', PATH_TO_CONFIG_FILES + 'wav_config', self.pathToAudioFile, mfcFileName])
        pipe.wait()
        return mfcFileName
        
    def alignAudio(self, timeShift, outputHTKPhoneAligned =''):
    
        baseNameAudioFile = os.path.splitext(self.pathToAudioFile)[0]
        
        
        (dictName, mlfName )  = self._createWordMLFandDict(baseNameAudioFile)
        
        # extract featuues
        
        mfcFileName = self._extractFeatures(baseNameAudioFile)
        
        if outputHTKPhoneAligned =='':
            outputHTKPhoneAligned = baseNameAudioFile + PHONEME_ALIGNED_SUFFIX
        
        # Align with hHVite
        pipe = subprocess.Popen([PATH_TO_HVITE, '-l', "'*'", '-o', 'S', '-A', '-D', '-T', '1', '-b', 'sil', '-C', PATH_TO_CONFIG_FILES + 'config', '-a', '-H', self.pathToHtkModel, '-i', '/tmp/phoneme-level.output', '-m', '-I', mlfName, '-y', 'lab', dictName, PATH_TO_HMMLIST, mfcFileName])
        pipe.wait()      
        if os.path.exists('/tmp/phoneme-level.output'):
            shutil.move('/tmp/phoneme-level.output', outputHTKPhoneAligned)
            
       
    
# END OF CLASS

    
'''
parse output in HTK's mlf output format ; load into list; 
convert from phoneme to word level alignment
serialize into table format easy to load from praat   

'''    
def prepareOutputForPraat(baneNameAudioFile, timeShift):
    #TODO: load time shift
   
    
    listTsAndWords = mlf2WordAndTsList(baneNameAudioFile + PHONEME_ALIGNED_SUFFIX)
    
    for index in range(len(listTsAndWords)):
        listTsAndWords[index][0] = listTsAndWords[index][0] + timeShift
        
    wordAlignedfileName = baneNameAudioFile + WORD_ALIGNED_SUFFIX    
    writeListOfListToTextFile(listTsAndWords, 'startTs word\n', wordAlignedfileName)
    print 'word level alignment written to file: ',  wordAlignedfileName
    return wordAlignedfileName

    
    '''
    call Praat script to: 
    -open phoneLevel.annotation file  .TextGrid
    -open the result alignemnt  
    -add the result as tier in the TextGrid
    -save the new file as .comparison.TextGrid
    
    open Praat to visualize it 
    '''
def openAlignmentInPraat(wordAnnoURI, outputHTKPhoneAlignedURI, timeShift):
    
    # prepare
    outputHTKPhoneAlignedNoExt = os.path.splitext(outputHTKPhoneAlignedURI)[0]
    wordAlignedfileName = prepareOutputForPraat(outputHTKPhoneAlignedNoExt, timeShift)
     
     
    # call praat script 
  #  path = '/Volumes/IZOTOPE/adaptation_data_soloVoice/kani_karaca-cargah-tevsih/'
    wordAlignedPath = os.path.dirname(wordAlignedfileName)
    wordAlignedFileName = os.path.splitext(os.path.basename(wordAlignedfileName))[0]
    
    
    pathTowordAnno = os.path.dirname(wordAnnoURI)
    fileNameWordAnno = os.path.splitext(os.path.basename(wordAnnoURI))[0]
    
    pipe =subprocess.Popen( [ PATH_TO_PRAAT, PATH_TO_PRAAT_SCRIPT, pathTowordAnno, fileNameWordAnno, wordAlignedPath, wordAlignedFileName ])
    pipe.wait()
    
    
    # open comparison.TextGrid in  praat. optional
    comparisonTextGridURI =  os.path.join(wordAlignedPath, fileNameWordAnno)  + '.comparison.TextGrid'
    pipe = subprocess.Popen(["open", '-a', PATH_TO_PRAAT, comparisonTextGridURI])
    pipe.wait()
