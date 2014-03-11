#!/bin/bash

#############################
# script to run forced alignment. See HTK book page 44. 

#@param: path_to_file_no_ext - adds extension to wav
#@param HMM - adapted model- hard coded
# 
# graphem2phoneme is done by rules. 
# Note: the original dictionary is not extended but only the words in the transcript are used.
# TODO: before creating new word check if it is in dictionary
# 
#############################


###
# 	
# 	
# example run: 
# /Users/joro/Documents/Phd/UPF/voxforge/myScripts/doForceAligment.sh /Users/joro/Documents/Phd/UPF/Turkey-makam/all.mlf /Users/joro/Documents/Phd/UPF/Turkey-makam/codetrain_mfc.scp /Users/joro/Documents/Phd/UPF/Turkey-makam/lexicon.adapted  /Users/joro/Documents/Phd/UPF/Turkey-makam/adaptation/phoneme-level.out.mlf
#	
#
###


# STEP 0: Parse command-line
if [ $# -ne 3 ]; then
    echo "Tool to run forced alignment. Input: audio and text in turkish."
    echo ""
    echo "USAGE: $0 path_to_audio_file_no_ext lyrics.txtTur PHONE_LEVEL_ALIGNED.output.mlf "
    echo ""
    echo ""
    exit 0
fi


#### parameters.
HTK_34_PATH="/Users/joro/Documents/Fhg/htk3.4.BUILT/bin" 

PARENT_OF_INTERIM_AND_INPUT_FILES="/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/"

# HMMDefs model

#origninal speech HMM models 
# HMM=$PARENT_OF_INTERIM_AND_INPUT_FILES/interim_files/hmm7/hmmdefs

# adapted to singing voice
#HMM=/Users/joro/Documents/Phd/UPF/Turkey-makam/adaptedModel/hmmdefs.gmllrmean
HMM=/Users/joro/Documents/Phd/UPF/METUdata//model_output/hmmdefs.gmllrmean



# word-level transcriptions
WORD_LEVEL_MLF=${1}.wrd.mlf

# e.g. WORD_LEVEL_MLF="/Users/joro/Documents/Phd/UPF/Turkey-makam/all.mlf"

TXTTUR=$2
# DICTIONARY=$2
# DICTIONARY=/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/dict.adapted 

# NOTE: fist add dict with words from adaptation lexicon
#/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/test.lexicon


# output: 
PHONE_LEVEL_ALIGNMENT=$3
# PHONE_LEVEL_ALIGNMENT=/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/phone-level.adapted


HMMLIST=/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/interim_files/monophones1

# OUTPUT_ADAPTATION=$ADAPTATION/output
# mkdir $OUTPUT_ADAPTATION


##############################################################################################

if [ ! -f ${1}.wav ]
then 
/usr/local/bin/ffmpeg -i ${1}.mp3 ${1}.wav
fi

# TXT=/tmp/${1}.txt
TXT=${1}.txtMETU

# conver to METU txtx. done because  I need the .txt file
python /Users/joro/Documents/Phd/UPF/voxforge/myScripts/utils/turkishLyrics2METULyrics.py "$TXTTUR" $TXT


# create word-level mlf
     
a=`basename $TXT .txtMETU` ;   printf "$a "> /tmp/mlf; cat $TXT >> /tmp/mlf
perl /Users/joro/Documents/Phd/UPF/voxforge/HTK_scripts/prompts2mlf $WORD_LEVEL_MLF  /tmp/mlf


# put new words in dictionary
python /Users/joro/Documents/Phd/UPF/voxforge/myScripts/utils/METULyrics2phoneticDict.py $TXT  /tmp/lexicon1
cat /tmp/lexicon1 | sort | uniq > /tmp/lexicon2
printf "sil\tsil\n" >>/tmp/lexicon2

# here feature extraction
 #echo "${1}.wav ${1}.mfc" > /tmp/alignment_codetrain_mfc.scp
  #echo "${1}.mfc" > /tmp/only_mfc.scp

# extract mfccs
#/usr/local/bin/HCopy -A -D -T 1 -C /Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/input_files/wav_config -S /tmp/alignment_codetrain_mfc.scp
/usr/local/bin/HCopy -A -D -T 1 -C $PARENT_OF_INTERIM_AND_INPUT_FILES/input_files/wav_config ${1}.wav ${1}.mfc



# run forced alignment 
# make sure argiment to -i is less than 248 chars. Otherwise abort trap error comes.
$HTK_34_PATH/HVite -l "'*'" -o SW -A -D -T 1  -b sil -C $PARENT_OF_INTERIM_AND_INPUT_FILES/input_files/config  -a -H $HMM -i /tmp/phoneme-level.output -m -I $WORD_LEVEL_MLF -y lab /tmp/lexicon2 $HMMLIST ${1}.mfc
mv  /tmp/phoneme-level.output $PHONE_LEVEL_ALIGNMENT 

# visualize alignment in seconds
 echo "phone-level alignment writen to file $PHONE_LEVEL_ALIGNMENT"
 echo

rm $PHONE_LEVEL_ALIGNMENT.noMLF
 echo "startTs endTs phoneme"> $PHONE_LEVEL_ALIGNMENT.noMLF
 awk '{start = $1 / 10000000; end= $2 / 10000000;  print start, end,  $3, $4}' $PHONE_LEVEL_ALIGNMENT  | sed '1,2d' | sed '$d'   >> $PHONE_LEVEL_ALIGNMENT.noMLF
 # cat $PHONE_LEVEL_ALIGNMENT.noMLF

