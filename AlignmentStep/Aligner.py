'''
Created on Mar 17, 2014

@author: joro
'''
import os
import subprocess
from utils.Utils import mlf2WordAndTsList, writeListOfListToTextFile,\
    mlf2PhonemesAndTsList, writeListToTextFile
from Phonetizer import Phonetizer
import shutil
from Adapt import MODEL_NOISE_URI
import utils
import utilsLyrics

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
LYRICS_TXT_METUBET_EXT = '.txtMETU'
PHRASE_ANNOTATION_EXT = '.TextGrid'

# only to satisfy HTK 
DUMMY_HMM_URI = '/Users/joro/Documents/Phd/UPF/METUdata/model_output/multipleGaussians/DUMMY'

class Aligner():
    '''
    classdocs
    '''


    def __init__(self, PATH_TO_HTK_MODEL, pathToAudioFile,  lyrics, loadLyricsFromFile=0):
        
        self.pathToHtkModel = PATH_TO_HTK_MODEL
        self.pathToAudioFile = pathToAudioFile
        self.lyrics = lyrics
        self.loadLyricsFromFile = loadLyricsFromFile 
    
     ##################################################################################

    '''
    only one audio file and lyrics provided
    @param timeShift: add to start of timstamps (needed tog get real audio timestamp if audio is part of a bigger recording)
    '''
    

    def _createWordMLFandDict(self):
        #txtTur to METU. txtMETU as persistent file not really needed. For reference stored
        
        baseNameAudioFile = os.path.splitext(self.pathToAudioFile)[0]
        
        METUBETfileName = baseNameAudioFile + LYRICS_TXT_METUBET_EXT
        
        if (self.loadLyricsFromFile == 1):
            METULyrics = Phonetizer.turkishScriptLyrics2METUScriptLyricsFile(baseNameAudioFile + LYRICS_TXT_EXT, METUBETfileName)
        else:
            METULyrics = Phonetizer.turkishScriptLyrics2METUScriptLyrics(self.lyrics, METUBETfileName)
    # create Word-level mlf:
        baneN = os.path.basename(self.pathToAudioFile)
        baneN = os.path.splitext(baneN)[0]
        headerLine = baneN + ' ' + METULyrics
        
        writeListOfListToTextFile([], headerLine, '/tmp/prompts')
        
        # prompts2mlf
        mlfName = '/tmp/tmp' + HTK_MLF_WORD_ANNO_SUFFIX
        pipe = subprocess.Popen(['/usr/bin/perl', '/Users/joro/Documents/Phd/UPF/voxforge/HTK_scripts/prompts2mlf', mlfName, '/tmp/prompts'])
        pipe.wait()

        # phonetize
        dictName = '/tmp/lexicon2'
        
        Phonetizer.METULyrics2phoneticDict(METUBETfileName, dictName)
        return (dictName, mlfName, METULyrics )
    
    def _toWordNetwork(self, METULyrics):
        '''
        creates word network including optional sil and backgr noise at end and beginning
        '''
        grammar = '([sil|NOISE] '  + METULyrics + ' [sil|NOISE])'
        writeListToTextFile(grammar, None, '/tmp/grammar')
        
        HParseCommand = ['/usr/local/bin/HParse', '/tmp/grammar', '/tmp/wordNetw' ]
        pipe= subprocess.Popen(HParseCommand)
        pipe.wait()
        
        return '/tmp/wordNetw'
        

    def _extractFeatures(self, path_TO_OUTPUT):
        baseNameAudioFile = os.path.splitext(os.path.basename(self.pathToAudioFile))[0]
        mfcFileName = os.path.join(path_TO_OUTPUT, baseNameAudioFile  ) + '.mfc'
        
#         if not os.path.isfile(mfcFileName):
        pipe= subprocess.Popen([PATH_TO_HCOPY, '-A', '-D', '-T', '1', '-C', PATH_TO_CONFIG_FILES + 'wav_config_singing', self.pathToAudioFile, mfcFileName])
        pipe.wait()
        return mfcFileName
   
    '''
       @param path_TO_OUTPUT:  all generated files are put in this dir. e.g. - the files with extracted .mfc
       @param outputHTKPhoneAligned: alignment result file
    '''     
    def alignAudio(self, timeShift, path_TO_OUTPUT,  outputHTKPhoneAligned ):
        
        (dictName, mlfName, METULyrics )  = self._createWordMLFandDict()
        
        wordNetwURI = self._toWordNetwork( METULyrics)
        
        # extract featuues
         
        mfcFileName = self._extractFeatures(path_TO_OUTPUT)
        

#         # Align with hHVite
                # Align with hHVite
        pipe = subprocess.Popen([PATH_TO_HVITE, '-l', "'*'", '-A', '-D', '-T', '1', '-b', 'sil', '-C', PATH_TO_CONFIG_FILES + 'config_singing', '-a', \
                                 '-H', self.pathToHtkModel, '-H',  DUMMY_HMM_URI , '-H',  MODEL_NOISE_URI , '-i', '/tmp/phoneme-level.output', '-m', \
                                 '-w', wordNetwURI, '-y', 'lab', dictName, PATH_TO_HMMLIST, mfcFileName])
        
        pipe.wait()      
        if os.path.exists('/tmp/phoneme-level.output'):
            shutil.move('/tmp/phoneme-level.output', outputHTKPhoneAligned)
            
       
    '''
    align one file
    '''
    @staticmethod
    def alignOnechunk(pathToHtkModel, pathToAudioFile,   wordAnnoURI, path_TO_OUTPUT, outputHTKPhoneAlignedURI='' ):
            
            lyrics = ""
            aligner = Aligner(pathToHtkModel, pathToAudioFile,  lyrics, 1) 
            
            timeShift = 35.81
            timeShift =  0
    #         aligner.alignAudio(  timeShift, outputHTKPhoneAligned)
                
            if outputHTKPhoneAlignedURI=='':
                baseNameAudioFile = os.path.splitext(os.path.basename(aligner.pathToAudioFile))[0]
                outputHTKPhoneAlignedURI = os.path.join(path_TO_OUTPUT, baseNameAudioFile ) + HTK_MLF_ALIGNED_SUFFIX
            
            
            aligner.alignAudio( timeShift, path_TO_OUTPUT, outputHTKPhoneAlignedURI)
            
            openAlignmentInPraat(wordAnnoURI, outputHTKPhoneAlignedURI, timeShift, pathToAudioFile)
    
            return outputHTKPhoneAlignedURI  
    
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
def openAlignmentInPraat(wordAnnoURI, outputHTKPhoneAlignedURI, timeShift, pathToAudioFile):
    
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
    command = [ PATH_TO_PRAAT, PATH_TO_PRAAT_SCRIPT, alignedResultPath, fileNameWordAnno,  alignedFileBaseName, PHONEME_ALIGNED_SUFFIX ]
    pipe =subprocess.Popen(command)
    pipe.wait()
    
    # open comparison.TextGrid in  praat. OPTIONAL
    comparisonTextGridURI =  os.path.join(alignedResultPath, fileNameWordAnno)  + PHRASE_ANNOTATION_EXT
    pipe = subprocess.Popen(["open", '-a', PATH_TO_PRAAT, comparisonTextGridURI])
    pipe.wait()
    
    # and audio

    pipe = subprocess.Popen(["open", '-a', PATH_TO_PRAAT, pathToAudioFile])
    pipe.wait()
    
