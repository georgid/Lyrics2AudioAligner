I. create model: 

on data: s1000


GITDIR=/Users/joro/Documents/Phd/UPF/voxforge/myScripts/

MAIN_TRAIN_DIR=/Users/joro/Documents/Phd/UPF/METUdata/
TRAIN_DIR_WAV=$MAIN_TRAIN_DIR/speech-text-all-georgi
TRAIN_DIR_WITH_PHN_AND_WRD_FILES=$MAIN_TRAIN_DIR/alignments-all-georgi
TRAIN_OUTPUT=$MAIN_TRAIN_DIR/model_output

0) remove old stuff
cd /Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/

htk_init () {
	rm -rf ./interim_files
	mkdir ./interim_files
	cd ./interim_files
	mkdir hmm0 hmm1 hmm2 hmm3 hmm4 hmm5 hmm6 hmm7 hmm8 hmm9 hmm10
	mkdir hmm11 hmm12 hmm13 hmm14 hmm15 mfcc
	cd ..
	return 0
}

htk_init


## this was used for one speaker only ./myScripts/combineAllPrompts.sh /Users/joro/Documents/Phd/UPF/voxforge/auto/train/wav/ /Users/joro/Documents/Phd/UPF/voxforge/auto/train/s1000.prompts


1) build phonetic dict file. Using given alignment transcription of words (a workaround because we do not have phonetic dict): 

### this was used for one speaker only TRAIN_DIR_WITH_PHN_AND_WRD_FILES=/Users/joro/Documents/Phd/UPF/METUdata/alignments/s1000/

# subtitute SIL for sil  
for i in `ls /Users/joro/Documents/Phd/UPF/METUdata/alignments-all-georgi/`; do sed -i '' 's/SIL/sil/g' $i  ; done

$GITDIR/TrainingStep/2phoneDict.sh  $TRAIN_DIR_WITH_PHN_AND_WRD_FILES  $TRAIN_OUTPUT/all-pronunciation.dict


# here make sure J is in monophones0 and SILSIL or silsil is not there


2) create all word-level mlf
python $GITDIR/TrainingStep/combineTxtIntoPrompts.py $TRAIN_DIR_WAV $TRAIN_OUTPUT/word-level.prompts
perl /Users/joro/Documents/Phd/UPF/voxforge/HTK_scripts/prompts2mlf $TRAIN_OUTPUT/word-level.mlf  $TRAIN_OUTPUT/word-level.prompts


3) train model
$GITDIR/TrainingStep/HTK_Compile_Model.sh $TRAIN_OUTPUT/all-pronunciation.dict $TRAIN_OUTPUT/word-level.mlf $TRAIN_DIR_WAV

#with MFCC_0_D_N_Z





-----------------	

step 8 - will be not done at all. in turkish there only one possible pronunciation per word.

only monophone models are used. No triphone models needed because in singing only vocals are bearing tones. The consonants in context do not influence vocals. The diphtongues do not exist in turkish language (expect for yu, ya).   

