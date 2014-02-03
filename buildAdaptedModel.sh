#!/bin/bash

#############################
# script to adapt the monophones built from speech to singing voice. See HTK book page 47.  
#############################


###
# example run: 
# /Users/joro/Documents/Phd/UPF/voxforge/myScripts/buildAdaptedModel.sh  "/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/test.mlf" \ 
# "/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/" "/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/dict.adapted" \
# PHONE_LEVEL_ALIGNMENT=/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/phone-level.adapted


###


# STEP 0: Parse command-line
if [ $# -ne 5 ]; then
    echo "Tool for creating an adapted acoustic model. The adaptation transmorfmation form is in dir OUTPUT_ADAPTATION_DIR.output "
    echo ""
    echo "USAGE: $0 WORD_LEVEL_MLF.mlf WavFiles.list dict.adapted PHONE_LEVEL_ALIGNED.output OUTPUT_ADAPTATION_DIR.output "
    echo ""
    echo ""
    exit 0
fi


#### parameters.
HTK_34_PATH="/Users/joro/Documents/Fhg/htk3.4.BUILT/bin" 

DATA="/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/"

# trained HMM models 
HMM=$DATA/interim_files/hmm6/hmmdefs

# word-level transcriptions
WORD_LEVEL_MLF=$1

# e.g. WORD_LEVEL_MLF="/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/test.mlf"

# blah 
WAVS=$2
# WAVS="/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/adapttrain_test.scp"

DICTIONARY=$3
# DICTIONARY=/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/dict.adapted 

# NOTE: fist add dict with words from adaptation lexicon
#/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/test.lexicon

PHONE_LEVEL_ALIGNMENT=$4
# PHONE_LEVEL_ALIGNMENT=/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/phone-level.adapted

OUTPUT_ADAPTATION=$5 

HMMLIST=/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/interim_files/monophones1

# OUTPUT_ADAPTATION=$ADAPTATION/output
# mkdir $OUTPUT_ADAPTATION

# run forced alignment 
$HTK_34_PATH/HVite -l '*'  -A -D -T 1  -b sil -C $DATA/input_files/config  -a -H $HMM -i $PHONE_LEVEL_ALIGNMENT -m -I $WORD_LEVEL_MLF -y lab -S $WAVS $DICTIONARY $HMMLIST

# visualize alignment in seconds
# awk '{start = $1 / 10000000; end= $2 / 10000000;  print start, end,  $3}' alignment.output

# adapt model 
 HERest -T 1 -C $DATA/input_files/config -C $ADAPTATION/configs/gmllr.config.global -J $ADAPTATION/configs/ -K $OUTPUT_ADAPTATION gmllrmean -S $WAVS -I $PHONE_LEVEL_ALIGNMENT -H $HMM -u a $HMMLIST 


