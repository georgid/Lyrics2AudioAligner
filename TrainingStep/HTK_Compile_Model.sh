#!/bin/sh
####################################################################
###
### script name: HTK_Compile_Model.sh
### modified by: Ken MacLean
### edited by: Georgi Dzhambazov 
### email: contact@voxforge.org
### Date: 2006.02.24
###		
### Copyright (C) 2006 Ken MacLean
###
### This program is free software; you can redistribute it and/or
### modify it under the terms of the GNU General Public License
### as published by the Free Software Foundation; either version 2
### of the License, or (at your option) any later version.
###
### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.
###
####################################################################

# PARAMETERS: 

echo "Starting training HMM models..."


ALL_PRON_DICT=$1
WORD_LEVEL_MLF=$2
TRAIN_DIR_WAV=$3
PARENT_OF_INTERIM_AND_INPUT_FILES=$4

# PARENT_OF_INTERIM_AND_INPUT_FILES=/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/
GITDIR=/Users/joro/Documents/Phd/UPF/voxforge/myScripts


make_hmmdefs () {
	for WORD in `cat ./interim_files/monophones0`
	do 
		tail -n 28  ./interim_files/hmm0/proto | sed s/~h\ \"proto\"/~h\ \"$WORD\"/g >> ./interim_files/hmm0/hmmdefs
	done                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
	return 0
}

make_macros () {
	head -n 3 ./interim_files/hmm0/proto > ./interim_files/hmm0/macros
	cat ./interim_files/hmm0/vFloors >> ./interim_files/hmm0/macros
	return 0
}

make_hmm4 () {
    LINE="start"
    NUM=1

	rm -rf ./interim_files/hmm4/hmmdefs.tmp1
	rm -rf ./interim_files/hmm4/hmmdefs.tmp2
	
    while [ `echo ${LINE} | awk '{ print $1 }'` != "" ];
    do
		LINE=`cat -n ./interim_files/hmm4/hmmdefs | grep ^[[:space:]]*${NUM}[[:space:]] | sed s/^[[:space:]]*[[:digit:]]*//g`
		if [ `echo ${LINE} | awk '{ print $2 }'` = "\"sil\"" ]; then
            while [ `echo ${LINE} | awk '{ print $1 }'` != "<ENDHMM>" ];
            do
                echo ${LINE} >> ./interim_files/hmm4/hmmdefs.tmp1
                echo ${LINE} >> ./interim_files/hmm4/hmmdefs.tmp2
				print_process ${NUM}
				let "NUM += 1"
				LINE=`cat -n ./interim_files/hmm4/hmmdefs | grep ^[[:space:]]*${NUM}[[:space:]] | sed s/^[[:space:]]*[[:digit:]]*//g`
			done
			
			echo ${LINE} >> ./interim_files/hmm4/hmmdefs.tmp1

			NUM2=1
			while [ "${NUM2}" != "28" ];
			do
				LINE2=`cat -n ./interim_files/hmm4/hmmdefs.tmp2 | grep ^[[:space:]]*${NUM2}[[:space:]] \
				| sed s/^[[:space:]]*[[:digit:]]*//g`

			   case ${NUM2} in
					1 ) 
						echo ${LINE2} | sed s/~h\ \"sil\"/~h\ \"sp\"/g >> ./interim_files/hmm4/hmmdefs.tmp1
						;;
					2 ) 
						echo ${LINE2} >> ./interim_files/hmm4/hmmdefs.tmp1
						;;
					3 ) 
						echo ${LINE2} | sed s/5/3/g >> ./interim_files/hmm4/hmmdefs.tmp1
						;;
					10 ) 
						echo ${LINE2} | sed s/3/2/g >> ./interim_files/hmm4/hmmdefs.tmp1
						;;
					11 | 12 | 13 | 14 | 15)
						echo ${LINE2} >> ./interim_files/hmm4/hmmdefs.tmp1
						;;
					22 )
						echo ${LINE2} | sed s/5/3/g >> ./interim_files/hmm4/hmmdefs.tmp1
						;;
					24 ) 
						echo "0.000000e+000 1.000000e+000 0.000000e+000" >> ./interim_files/hmm4/hmmdefs.tmp1
						;;
					25 ) 
						echo "0.000000e+000 0.900000e+000 0.100000e+000" >> ./interim_files/hmm4/hmmdefs.tmp1
						;;
					26 ) 
						echo "0.000000e+000 0.000000e+000 0.000000e+000" >> ./interim_files/hmm4/hmmdefs.tmp1
						;;
				esac
				let "NUM2 += 1"
			done
        fi
		echo ${LINE} >> ./interim_files/hmm4/hmmdefs.tmp1
		print_process ${NUM}
		let "NUM += 1"
	done
	mv -f ./interim_files/hmm4/hmmdefs.tmp1 ./interim_files/hmm4/hmmdefs
	return 0
} 

make_dict1 () {
	cat ./interim_files/dict > ./interim_files/dict1
	echo "silence  []  sil" >> ./interim_files/dict1
	return 0
}



print_heading () {
	if [ $? = "0" ]; then
		echo
		echo -e "\t$1"
		NUM=1
		while [ ${NUM} -lt 32 ];
		do
			echo -n "=="
			let "NUM += 1"
		done
		echo
	else
		exit 1
	fi
	return 0
}


########################################################################
#	Main 
########################################################################
print_heading "init"
	

cd $PARENT_OF_INTERIM_AND_INPUT_FILES
htk_init
print_heading "Step 4 - create Phoneme-level alignemnt in format understandable for HTK. 
Replace each word with its phonemes, and put the result in a new Phone Level Master Label File.
phones0 is without sp model. phones1 is absolutely same but with sp at end of each word "
	HLEd -A -D -T 1 -l '*' -d $ALL_PRON_DICT -i ./interim_files/phones0.mlf ./input_files/mkphones0.led $WORD_LEVEL_MLF > logs/Step4_HLEd_phones0.log
	HLEd -A -D -T 1 -l '*' -d $ALL_PRON_DICT -i ./interim_files/phones1.mlf ./input_files/mkphones1.led $WORD_LEVEL_MLF > logs/Step4_HLEd_phones1.log



print_heading "Step 5 - Extract MFCCs. Coding the (Audio) Data"	
	

python $GITDIR/TrainingStep/listWavFiles.py ${TRAIN_DIR_WAV} /tmp/codetrain.scp /tmp/train.scp
	HCopy -A -D -T 1 -C ./input_files/wav_config -S /tmp/codetrain.scp> logs/Step5_HCopy.log
	

print_heading "Step 6 - Creating Monophones"
    echo -e 'making hmm0\n. HCompV computes the global mean and variance'
	HCompV -A -D -T 1 -C ./input_files/config -f 0.01 -m -S /tmp/train.scp -M ./interim_files/hmm0 input_files/proto > logs/Step6_HCompV_hmm0.log
	make_hmmdefs
	make_macros
	echo -e 'making hmm1\n'
	HERest -A -D -T 1 -C ./input_files/config -I ./interim_files/phones0.mlf -t 250.0 150.0 1000.0 -S /tmp/train.scp -H ./interim_files/hmm0/macros -H ./interim_files/hmm0/hmmdefs -M ./interim_files/hmm1 ./interim_files/monophones0 > logs/Step6_HERest_hmm1.log
	echo -e 'making hmm2\n'
	HERest -A -D -T 1 -C ./input_files/config -I ./interim_files/phones0.mlf -t 250.0 150.0 1000.0 -S /tmp/train.scp -H ./interim_files/hmm1/macros -H ./interim_files/hmm1/hmmdefs -M ./interim_files/hmm2 ./interim_files/monophones0 > logs/Step6_HERest_hmm2.log
	echo -e 'making hmm3\n'
	HERest -A -D -T 1 -C ./input_files/config -I ./interim_files/phones0.mlf -t 250.0 150.0 1000.0 -S /tmp/train.scp -H ./interim_files/hmm2/macros -H ./interim_files/hmm2/hmmdefs -M ./interim_files/hmm3 ./interim_files/monophones0 > logs/Step6_HERest_hmm3.log

#step 7 - DONE because HVIte requires sp models

print_heading "Step 7 - Fixing the Silence Model"
	cp  -R ./interim_files/hmm3/. ./interim_files/hmm4
	echo -e 'making hmm4\n'
	make_hmm4 2> /dev/null
	echo -e 'making hmm5\n'
	HHEd -A -D -T 1 -H ./interim_files/hmm4/macros -H ./interim_files/hmm4/hmmdefs -M ./interim_files/hmm5 ./input_files/sil.hed ./interim_files/monophones1 > logs/Step7_HHEd_hmm5.log
	echo -e 'making hmm6\n'
	HERest -A -D -T 1 -C ./input_files/config  -I ./interim_files/phones1.mlf -t 250.0 150.0 3000.0 -S /tmp/train.scp -H ./interim_files/hmm5/macros -H ./interim_files/hmm5/hmmdefs -M ./interim_files/hmm6 ./interim_files/monophones1 > logs/Step7_HERest_hmm6.log
	echo -e 'making hmm7\n'
	HERest -A -D -T 1 -C ./input_files/config  -I ./interim_files/phones1.mlf -t 250.0 150.0 3000.0 -S /tmp/train.scp -H ./interim_files/hmm6/macros -H ./interim_files/hmm6/hmmdefs -M ./interim_files/hmm7 ./interim_files/monophones1 > logs/Step7_HERest_hmm7.log

	
#step 8 - will be not done at all. in turkish there only one possible pronunciation per word.

print_heading "***completed*** model is interim_files/hmm7/hmmdefs"
