#!/bin/sh

II. ADAPTATION: 

MAIN_TRAIN_DIR=/Users/joro/Documents/Phd/UPF/METUdata/
TRAIN_OUTPUT=$MAIN_TRAIN_DIR/model_output


################
# params 
#######################


# dir should have .wav .txtTur  files for each file to be adapted 
# prepare .txt just all words in METUbet script,

# ADAPTATION_DATA=

# this will be overwritten on new adaptation:
ADAPTED_DICT=$ADAPTATION_DATA/all_pronunciation_dict.adapted

# this will be overwritten on new adaptation:
ALL_MLF=$ADAPTATION_DATA/all.phn.mlf

ADAPTED_MODEL=${ADAPTATION_DATA}/adaptedModel/hmmdefs.gmllrmean






###############################
# PREPARATION
###############################
1) create dict file. mix speech dict and adaptation dict: 
# input needed: files with extension .txtTur
/Users/joro/Documents/Phd/UPF/voxforge/myScripts/turkishLyrics2phoneDict.sh  $ADAPTATION_DATA 1 ${TRAIN_OUTPUT}/all-pronunciation.dict $ADAPTED_DICT

# do manually: delete SIL (with capital letters) and SILSIL from /Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/interim_files/monophones1

2) ANNOTATE manually. Use <filename>.lexicon from previous step in the phoneme-level annotation. Put extension .phn                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     


#############################
# ADAPT 
##############################

3) prepare phoneme-level mlf. Parses file with extension .phn
#if Praat used: do for each file: 
python /Users/joro/Documents/Phd/UPF/voxforge/myScripts/utils/TextGrid_Parsing.py <fileName>.TextGrid <fileName>.phoneAnno

# always do:
python /Users/joro/Documents/Phd/UPF/voxforge/myScripts/utils/sonicVisTextPhnDir2mlf.py $ADAPTATION_DATA $ALL_MLF

4) adapt

$UPF/voxforge/myScripts/buildAdaptedModel.sh  $ADAPTATION_DATA  $ADAPTED_DICT $ALL_MLF $TRAIN_OUTPUT $ADAPTED_MODEL


#resulting new model: 
$ADAPTED_MODEL




