
INPUTMODEL=/Users/joro/Documents/Phd/UPF/METUdata/model_output/hmmdefs
OUTPUTMODELPATH=/Users/joro/Documents/Phd/UPF/METUdata/model_output/multipleGaussians/

MODEL=$OUTPUTMODELPATH/hmmdefs3
# create codetrain list
HHEd -H $INPUTMODEL -M $MODEL increaseNumGaussiansTo3.cmd $PARENT_OF_INTERIM_AND_INPUT_FILES/interim_files/monophones0

# increase number of Gaussians: 


# reestimate
HERest -A -D -T 1 -C $PARENT_OF_INTERIM_AND_INPUT_FILES/input_files/config -I $PARENT_OF_INTERIM_AND_INPUT_FILES/interim_files/phones0.mlf -t 250.0 150.0 1000.0 -S /tmp/train.scp -H $PARENT_OF_INTERIM_AND_INPUT_FILES/interim_files/hmm2/macros -H $MODEL -M $OUTPUTMODELPATH $PARENT_OF_INTERIM_AND_INPUT_FILES/interim_files/monophones0