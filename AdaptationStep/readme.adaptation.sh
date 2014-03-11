#!/bin/sh

II. ADAPTATION: 

MAIN_TRAIN_DIR=/Users/joro/Documents/Phd/UPF/METUdata/
TRAIN_OUTPUT=$MAIN_TRAIN_DIR/model_output

### (input and output are in folder /Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation)

-1) prepare. 

# dir should have .wav .txtTur  files for each file to be adapted 
# prepare .txt just all words in METUbet script,
ADAPTATION_TRAIN_DIR_WITH_PHN_AND_WRD_FILES_FILES=/Users/joro/Documents/Phd/UPF/Turkey-makam/

ADAPTATION_TRAIN_DIR_WITH_PHN_AND_WRD_FILES_FILES=$ADAPTATION_DATA



1) create dict file. mix speech dict and adaptation dict: 

/Users/joro/Documents/Phd/UPF/voxforge/myScripts/turkishLyrics2phoneDict.sh  $ADAPTATION_TRAIN_DIR_WITH_PHN_AND_WRD_FILES_FILES 1  ${TRAIN_OUTPUT}/all-pronunciation.dict ${ADAPTATION_TRAIN_DIR_WITH_PHN_AND_WRD_FILES_FILES}/all_pronunciation_dict.adapted

# do manually: delete SIL (with capital letters) and SILSIL from /Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/interim_files/monophones1

2) ANNOTATE manully. Use <filename>.lexicon from previous step in the phoneme-level annotation. Put extension .phn                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     


3) prepare phoneme-level mlf. Parses file with extension .phn
#if Praat used: do for each file: 
python /Users/joro/Documents/Phd/UPF/voxforge/myScripts/utils/TextGrid_Parsing.py <fileName>.TextGrid <fileName>.phn

# always do:
python /Users/joro/Documents/Phd/UPF/voxforge/myScripts/utils/sonicVisTextPhnDir2mlf.py $ADAPTATION_TRAIN_DIR_WITH_PHN_AND_WRD_FILES_FILES ${ADAPTATION_TRAIN_DIR_WITH_PHN_AND_WRD_FILES_FILES}/all.phn.mlf

4) adapt
$UPF/voxforge/myScripts/buildAdaptedModel.sh  ${ADAPTATION_TRAIN_DIR_WITH_PHN_AND_WRD_FILES_FILES}  ${ADAPTATION_TRAIN_DIR_WITH_PHN_AND_WRD_FILES_FILES}/pronunciation_dict.adapted ${ADAPTATION_TRAIN_DIR_WITH_PHN_AND_WRD_FILES_FILES}/all.phn.mlf  $TRAIN_OUTPUT


resulting new model: 
${ADAPTATION_TRAIN_DIR_WITH_PHN_AND_WRD_FILES_FILES}/adaptedModel/hmmdefs.gmllrmean





