#!/bin/bash

#############################
# script to run forced alignment. See HTK book page 44. 

#@param: path_to_file_no_ext - adds extension to wav
#@param HMM - adapted model- hard coded
#############################


###
# example run: 
# /Users/joro/Documents/Phd/UPF/voxforge/myScripts/doForceAligment.sh /Users/joro/Documents/Phd/UPF/Turkey-makam/all.mlf /Users/joro/Documents/Phd/UPF/Turkey-makam/codetrain_mfc.scp /Users/joro/Documents/Phd/UPF/Turkey-makam/lexicon.adapted  /Users/joro/Documents/Phd/UPF/Turkey-makam/adaptation/phoneme-level.out.mlf
###


# STEP 0: Parse command-line
if [ $# -ne 2 ]; then
    echo "Tool to run forced alignment. Input: 1) word-level mlf; 2) dictionary with at least all words in the word-level mlf. 3) mfc features. "
    echo ""
    echo "USAGE: $0 path_to_file_no_ext PHONE_LEVEL_ALIGNED.output.mlf "
    echo ""
    echo ""
    exit 0
fi


#### parameters.
HTK_34_PATH="/Users/joro/Documents/Fhg/htk3.4.BUILT/bin" 

DATA="/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/"

# HMMDefs model

#origninal speech HMM models 
# HMM=$DATA/interim_files/hmm6/hmmdefs

# adapted to singing voice
HMM=/Users/joro/Documents/Phd/UPF/Turkey-makam/adaptedModel/hmmdefs.gmllrmean



# word-level transcriptions
WORD_LEVEL_MLF=${1}.wrd.mlf

# e.g. WORD_LEVEL_MLF="/Users/joro/Documents/Phd/UPF/Turkey-makam/all.mlf"

# DICTIONARY=$2
# DICTIONARY=/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/dict.adapted 

# NOTE: fist add dict with words from adaptation lexicon
#/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/test.lexicon


# output: 
PHONE_LEVEL_ALIGNMENT=$2
# PHONE_LEVEL_ALIGNMENT=/Users/joro/Documents/Phd/UPF/voxforge/auto/adaptation/phone-level.adapted


HMMLIST=/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/interim_files/monophones1

# OUTPUT_ADAPTATION=$ADAPTATION/output
# mkdir $OUTPUT_ADAPTATION


##############################################################################################

if [ ! -f ${1}.wav ]
then 
ffmpeg -i ${1}.mp3 ${1}.wav
fi

# done because  I need the .txt file
python /Users/joro/Documents/Phd/UPF/voxforge/myScripts/utils/turkishLyrics2METULyrics.py ${1}.txtTur ${1}.txt


# create word-level mlf
     
a=`basename ${1}.txt .txt` ;   printf "$a "> /tmp/mlf; cat ${1}.txt >> /tmp/mlf
perl /Users/joro/Documents/Phd/UPF/voxforge/HTK_scripts/prompts2mlf $WORD_LEVEL_MLF  /tmp/mlf


# put new words in dictionary
python /Users/joro/Documents/Phd/UPF/voxforge/myScripts/utils/turkishScriptLyrics2phoneticDict.py ${1}.txtTur /tmp/lexicon1
cat /tmp/lexicon1 | sort | uniq > /tmp/lexicon2
printf "sil\tsil\n" >>/tmp/lexicon2

# here feature extraction
 echo "${1}.wav ${1}.mfc" > /tmp/alignment_codetrain_mfc.scp
  echo "${1}.mfc" > /tmp/only_mfc.scp

# extract mfccs
HCopy -A -D -T 1 -C /Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/input_files/wav_config -S /tmp/alignment_codetrain_mfc.scp



# run forced alignment 
$HTK_34_PATH/HVite -l '*' -o SW -A -D -T 1  -b sil -C $DATA/input_files/config  -a -H $HMM -i $PHONE_LEVEL_ALIGNMENT -m -I $WORD_LEVEL_MLF -y lab -S /tmp/only_mfc.scp /tmp/lexicon2 $HMMLIST

# visualize alignment in seconds
# awk '{start = $1 / 10000000; end= $2 / 10000000;  print start, end,  $3}' alignment.output



