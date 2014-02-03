#!/bin/bash

#############################
# script to make mlf, extract features and extend given dictionary with new wordds from transcript  
#############################



if [ $# -ne 2 ]; then
    echo "Tool for preparing audio data to be used in adaptation of acoustic model"
    echo "Have in mind that input pronounciation lexicons are hard=coded "
    echo ""
    echo "USAGE: $0  DIR_WITH_WavAndTxt ADAPTED_LEXICON.output"
    echo ""
    echo ""
    exit 0
fi

#################
### parameters
################
DIR_WITH_WavAndTxt=$1;
ADAPTED_LEXICON=$2;
# ADAPTED_LEXICON=$DIR_WITH_WavAndTxt/lexicon.adapted
SCRIPTS=/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/

for i in `ls $DIR_WITH_WavAndTxt/*.wav`; 
do a=`basename $i .wav` ;   printf "$i $DIR_WITH_WavAndTxt/$a.mfc"  ; echo;  
 #   if [ -n "$(tail -c 1 <"$i")" ]; then echo; fi;   done

done >$DIR_WITH_WavAndTxt/codetrain.scp

# extract features 
HCopy -A -D -T 1 -C /Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/input_files/wav_config -S $DIR_WITH_WavAndTxt/codetrain.scp


# combine all prompts in one file
/Users/joro/Documents/Phd/UPF/voxforge/myScripts/combineAllPrompts.sh $DIR_WITH_WavAndTxt $DIR_WITH_WavAndTxt/all.prompts

# create mlf from prompts
 perl /Users/joro/Documents/Phd/UPF/voxforge/HTK_scripts/prompts2mlf $DIR_WITH_WavAndTxt/all.mlf $DIR_WITH_WavAndTxt/all.prompts
 

#combine lexion files
cat $DIR_WITH_WavAndTxt/*.lexicon | sort | uniq > $DIR_WITH_WavAndTxt/all.lexicon;

# combine the last 2 parameters - two pronounciation lexicons into one
HDMan -A -D -T 1 -m  -e $SCRIPTS/input_files -n $SCRIPTS/interim_files/monophones1 -i $ADAPTED_LEXICON /Users/joro/Documents/Phd/UPF/METUdata/alignments/s1000/all.lexicon $DIR_WITH_WavAndTxt/all.lexicon

