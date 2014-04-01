'''
Created on Mar 17, 2014

@author: joro
'''
import os
import subprocess
from utils.Utils import mlf2WordAndTsList, writeListOfListToTextFile,\
    mlf2PhonemesAndTsList
from Phonetizer import Phonetizer
import shutil

HTK_MLF_WORD_ANNO_SUFFIX = '.wrd.mlf'
HTK_MLF_ALIGNED_SUFFIX= ".htkAlignedMlf"

# in textual column-like format (e.g. timestamp \t word)
WORD_ALIGNED_SUFFIX= ".wordAligned"
PHONEME_ALIGNED_SUFFIX= ".phonemeAligned"


PATH_TO_ALIGNMENT_TOOL = os.path.abspath('doForceAligment.sh')
PATH_TO_HCOPY= '/usr/local/bin/HCopy'
PATH_TO_HVITE= '/Users/joro/Documents/Fhg/htk3.4.BUILT/bin/HVite'
PATH_TO_CONFIG_FILES= '/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/input_files/'
PATH_TO_HMMLIST='/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/interim_files/monophones1'

PATH_TO_PRAAT = '/Applications/Praat.app/Contents/MacOS/Praat'
PATH_TO_PRAAT_SCRIPT= '/Users/joro/Documents/Phd/UPF/voxforge/myScripts/praat/loadAlignedResultAndTextGrid'

LYRICS_TXT_EXT = '.txtTur'

class Aligner():
    '''
    classdocs
    '''


    def __init__(self, pathToHtkModel, pathToAudioFile, lyrics, loadLyricsFromFile=0):
        
        self.pathToHtkModel = pathToHtkModel
        self.pathToAudioFile = pathToAudioFile
        self.lyrics = lyrics
        self.loadLyricsFromFile = loadLyricsFromFile 
    
     ##################################################################################

    '''
    only one audio file and lyrics provided
    @param timeShift: add to start of timstamps (needed tog get real audio timestamp if audio is part of a bigger recording)
    '''
    

    def _createWordMLFandDict(self, baseNameAudioFile):
        #txtTur to METU. txtMETU as persistent file not really needed. For reference stored
        if (self.loadLyricsFromFile == 1):
            METULyrics = Phonetizer.turkishScriptLyrics2METUScriptLyricsFile(baseNameAudioFile + LYRICS_TXT_EXT, baseNameAudioFile + '.txtMETU')
        else:
            METULyrics = Phonetizer.turkishScriptLyrics2METUScriptLyrics(self.lyrics, baseNameAudioFile + '.txtMETU')
    # create Word-level mlf:
        baneN = os.path.basename(self.pathToAudioFile)
        baneN = os.path.splitext(baneN)[0]
        headerLine = baneN + ' ' + METULyrics
        writeListOfListToTextFile([], headerLine, '/tmp/prompts')
        
        # prompts2mlf
        mlfName = baseNameAudioFile + HTK_MLF_WORD_ANNO_SUFFIX
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
            outputHTKPhoneAligned = baseNameAudioFile + HTK_MLF_ALIGNED_SUFFIX
        
        # Align with hHVite
        pipe = subprocess.Popen([PATH_TO_HVITE, '-l', "'*'", '-o', 'S', '-A', '-D', '-T', '1', '-b', 'sil', '-C', PATH_TO_CONFIG_FILES + 'config', '-a', '-H', self.pathToHtkModel, '-i', '/tmp/phoneme-level.output', '-m', '-I', mlfName, '-y', 'lab', dictName, PATH_TO_HMMLIST, mfcFileName])
        pipe.wait()      
        if os.path.exists('/tmp/phoneme-level.output'):
            shutil.move('/tmp/phoneme-level.output', outputHTKPhoneAligned)
            
       
    
# END OF CLASS

    
'''
parse output in HTK's mlf output format ; load into list; 
serialize into table format easy to load from praat: 
-in word-level 
and 
- phoneme level

'''    
def prepareOutputForPraat(baneNameAudioFile, timeShift):
   
################ parse mlf and write word-level text file    
    listTsAndWords = mlf2WordAndTsList(baneNameAudioFile + HTK_MLF_ALIGNED_SUFFIX)
    wordAlignedfileName=  mlf2PraatFormat(listTsAndWords, timeShift, baneNameAudioFile, WORD_ALIGNED_SUFFIX)

  
########################## same for phoneme-level: 
    
    # with : phoneme-level alignment
    listTsAndPhonemes = mlf2PhonemesAndTsList (baneNameAudioFile + HTK_MLF_ALIGNED_SUFFIX)
    phonemeAlignedfileName=  mlf2PraatFormat(listTsAndPhonemes, timeShift, baneNameAudioFile, PHONEME_ALIGNED_SUFFIX)
    
    
    return wordAlignedfileName, phonemeAlignedfileName


'''
convenience method
'''
def mlf2PraatFormat(listTsAndPhonemes, timeShift, baneNameAudioFile, whichSuffix):
    
    # timeshift
    for index in range(len(listTsAndPhonemes)):
        listTsAndPhonemes[index][0] = listTsAndPhonemes[index][0] + timeShift
        
    phonemeAlignedfileName = baneNameAudioFile + whichSuffix
    
    writeListOfListToTextFile(listTsAndPhonemes, 'startTs phonemeOrWord\n', phonemeAlignedfileName)
    print 'phoneme level alignment written to file: ',  phonemeAlignedfileName
    return phonemeAlignedfileName
    

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
    wordAlignedfileName, phonemeAlignedfileName = prepareOutputForPraat(outputHTKPhoneAlignedNoExt, timeShift)
     
     
########### call praat script to add alignment as a new layer to existing annotation TextGrid
    alignedResultPath = os.path.dirname(wordAlignedfileName)
    alignedFileBaseName = os.path.splitext(os.path.basename(wordAlignedfileName))[0]
    
    
    # copy  annotation TExtGrid to path of results
    
    dirNameAnnotaion = os.path.dirname(wordAnnoURI)
    if (dirNameAnnotaion != alignedResultPath):
        shutil.copy2(wordAnnoURI,alignedResultPath )

    fileNameWordAnno = os.path.splitext(os.path.basename(wordAnnoURI))[0]
    
    # in praat script extensions  WORD_ALIGNED_SUFFIX  is added automatically
    pipe =subprocess.Popen( [ PATH_TO_PRAAT, PATH_TO_PRAAT_SCRIPT, alignedResultPath, fileNameWordAnno,  alignedFileBaseName, WORD_ALIGNED_SUFFIX ])
    pipe.wait()
    
    # same praat script for PHONEME_ALIGNED_SUFFIX
    pipe =subprocess.Popen( [ PATH_TO_PRAAT, PATH_TO_PRAAT_SCRIPT, alignedResultPath, fileNameWordAnno,  alignedFileBaseName, PHONEME_ALIGNED_SUFFIX ])
    pipe.wait()
    
    # open comparison.TextGrid in  praat. OPTIONAL
    comparisonTextGridURI =  os.path.join(alignedResultPath, fileNameWordAnno)  + '.TextGrid'
    pipe = subprocess.Popen(["open", '-a', PATH_TO_PRAAT, comparisonTextGridURI])
    pipe.wait()
