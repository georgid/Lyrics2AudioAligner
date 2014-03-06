
#!/bin/bash


#NOTE: Pronunciation Dictionnary needs to be balanced to in order to permit HTK to compile an Acoustic Model. 
#  e.g. it has to have at least 3-5 occurences of each prhoneme. THis is asserted by HDMan
# HDMan creates as well monophones1

if [ $# -ne 2 ]; then
    echo "Tool to make a pronounciation dict from words in .phn and .wrd files"
    echo "optionally xombines the created one with a given oldDictionary"
    echo "USAGE: $0  TRAIN_DIR_WITH_PHN_AND_WRD_FILES  output.extendedDictionary"
    echo ""
    echo ""
    exit 0
fi



TRAIN_DIR_WITH_PHN_AND_WRD_FILES=$1;
NEW_DICT=$2;

PARENT_OF_INTERIM_AND_INPUT_FILES=/Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/
GITDIR=/Users/joro/Documents/Phd/UPF/voxforge/myScripts


make_monophones0 () {
	for STR in `cat $PARENT_OF_INTERIM_AND_INPUT_FILES/interim_files/monophones1`; # monophones1 = monophones0 less "sp" phone
	do 
		if [ "${STR}" != "sp" ]; then 
			echo ${STR} >> $PARENT_OF_INTERIM_AND_INPUT_FILES/interim_files/monophones0; 
		fi; 
	done;
	return 0
}


# blah

python $GITDIR/TrainingStep/2phoneDict.py $TRAIN_DIR_WITH_PHN_AND_WRD_FILES /tmp/pronunciation_dict

echo "NOTE:  manually check that there are no SILSIL things  in  /tmp/pronunciation_dict "

#combine all lexicons 
cat /tmp/pronunciation_dict | sort | uniq > $TRAIN_DIR_WITH_PHN_AND_WRD_FILES/all.pronunciation_dict2;


echo "Running HDMan..."


# create NEW_DICT - use some transform rules from /Users/joro/Documents/Phd/UPF/voxforge/auto/scripts/input_files/global.ded and generate monophones
HDMan -A -D -T 1 -m  -e $PARENT_OF_INTERIM_AND_INPUT_FILES/input_files -n $PARENT_OF_INTERIM_AND_INPUT_FILES/interim_files/monophones1 -i -l /tmp/Step2_HDMan_log  $NEW_DICT $TRAIN_DIR_WITH_PHN_AND_WRD_FILES/all.pronunciation_dict2

make_monophones0

echo "dict written  $NEW_DICT"
echo "monophone list in $PARENT_OF_INTERIM_AND_INPUT_FILES/interim_files/monophones1 and monophones0" 

