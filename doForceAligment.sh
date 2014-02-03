#!/bin/bash

#############################
# script to run forced alignment. See HTK book page 47.  
#############################


###
# example run: 
# /Users/joro/Documents/Phd/UPF/voxforge/myScripts/doForceAligment.sh /Users/joro/Documents/Phd/UPF/Turkey-makam/all.mlf /Users/joro/Documents/Phd/UPF/Turkey-makam/codetrain_mfc.scp /Users/joro/Documents/Phd/UPF/Turkey-makam/lexicon.adapted  /Users/joro/Documents/Phd/UPF/Turkey-makam/adaptation/phoneme-level.out.mlf
###


# STEP 0: Parse command-line
if [ $# -ne 4 ]; then
    echo "Tool to run forced alignment. Input: 1) word-level mlf; 2) dictionary with at least all words in the word-level mlf. 3) mfc features. "
    echo ""
    echo "USAGE: $0 WORD_LEVEL_LIST.mlf MfccFiles.list dict PHONE_LEVEL_ALIGNED.output.mlf "
    echo ""
    echo ""
    exit 0
fi


#### parameters.
HTK_34_PATH="/Users/joro/Documents/Fhg/htk3.4.BUILT/bin" 

DATA="/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/"

# HMMDefs model

#origninal speech HMM models 
#HMM=$DATA/interim_files/hmm6/hmmdefs

# adapted to singing voice
HMM=/Users/joro/Documents/Phd/UPF/Turkey-makam/adaptation/hmmdefs.gmllrmean



# word-level transcriptions
WORD_LEVEL_MLF=$1

# e.g. WORD_LEVEL_MLF="/Users/joro/Documents/Phd/UPF/Turkey-makam/all.mlf"

# blah 
MfccFiles=$2
# MfccFiles="/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/adapttrain_test.scp"

DICTIONARY=$3
# DICTIONARY=/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/dict.adapted 

# NOTE: fist add dict with words from adaptation lexicon
#/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/test.lexicon


# output: 
PHONE_LEVEL_ALIGNMENT=$4
# PHONE_LEVEL_ALIGNMENT=/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/phone-level.adapted


HMMLIST=/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/interim_files/monophones1

# OUTPUT_ADAPTATION=$ADAPTATION/output
# mkdir $OUTPUT_ADAPTATION

# run forced alignment 
$HTK_34_PATH/HVite -l '*' -o SW -A -D -T 1  -b sil -C $DATA/input_files/config  -a -H $HMM -i $PHONE_LEVEL_ALIGNMENT -m -I $WORD_LEVEL_MLF -y lab -S $MfccFiles $DICTIONARY $HMMLIST

# visualize alignment in seconds
# awk '{start = $1 / 10000000; end= $2 / 10000000;  print start, end,  $3}' alignment.output



