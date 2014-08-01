#! /usr/bin/python
# -*- coding: utf-8 -*-
import re
import textgrid as tgp
import sys, os
from setuptools.command.easy_install import sys_executable
from utils.Utils import loadTextFile, writeListToTextFile,\
	writeListOfListToTextFile
from buildtools import MAGIC
from Aligner import PHRASE_ANNOTATION_EXT
sys.path.append(os.path.realpath('../Batch_Processing/'))
# import Batch_Proc_Essentia as BP  # @UnresolvedImport
import magic

# code from Sankalp

tier_name = "phonemes"
# tier_name = "words"
# tier_name = "phrases"

'''
textGrid to column file 
NOTE! make sure text writing preferences in Praat are set to utf-8 
'''
def TextGrid2Dict(textgrid_file, outputFileName):
	
	par_obj = tgp.TextGrid.load(textgrid_file)	#loading the object	
	tiers= tgp.TextGrid._find_tiers(par_obj)	#finding existing tiers
		
	outputFileHandle = open(outputFileName, 'w')
	
	
	for tier in tiers:
		
		if tier.tier_name() == tier_name:	#iterating over tiers and selecting the one specified
			
			tier_details = tier.make_simple_transcript();		#this function parse the file nicely and return cool tuples
			
			for line in tier_details:
				
				outputFileHandle.write(line[0] + "\t" + line[2]+ "\n") 

	outputFileHandle.close()		



'''
textGrid2Array of words only
NOTE! make sure text writing preferences in Praat are set to utf-8.

'''	
def TextGrid2WordList(textgrid_file, onlyLyrics=0):
		
			
		lyrics=''
		beginTsAndWordList=[]
		
		# if file not in UTF=encoding, stop
		blob = open(textgrid_file).read()
		magicInstance = magic.open(magic.MAGIC_MIME_ENCODING)
		magicInstance.load()
		encoding = magicInstance.buffer(blob)  # "utf-8" "us-ascii" etc
		
		if(encoding != 'utf-8'):
			print("Encoding of file {0} is not utf-8. If there are non-utf characters in the annotated text, make sure text writing preferences in Praat are set to utf-8 ".format(textgrid_file) )
		
		
		par_obj = tgp.TextGrid.load(textgrid_file)	#loading the object	
		tiers= tgp.TextGrid._find_tiers(par_obj)	#finding existing tiers		
		
		isTierFound = 0
		for tier in tiers:
		
			if tier.tier_name() == tier_name:	#iterating over tiers and selecting the one specified
				isTierFound = 1
				tier_details = tier.make_simple_transcript();		#this function parse the file nicely and return cool tuples
				
				for line in tier_details:
					beginTsAndWordList.append([line[0], line[1], line[2]])

					lyrics += line[2]
					lyrics += ' '
				

		
		if not isTierFound:
			sys.exit('tier in file {0} might not be named correctly. Currently the tool is configured to work with tiers named {1}' .format(textgrid_file, tier_name))
		
		if onlyLyrics:
			return lyrics
		else:
			return beginTsAndWordList		


##################################################################################




if __name__ == '__main__':
	
	PATH_TEST_DATASET_NEW = '/Users/joro/Dropbox/Varnam_Analysis/data/audio/abhogi/'
	audio = "prasanna_Evvari_bodhanavini"
	
	PATH_TEST_DATASET_NEW = '/Users/joro/Documents/Phd/UPF/adaptation_data_soloVoice/ISTANBUL/safiye/'
	audio ='01_Olmaz_Part2_T1'
	

	annotationPhraseListA = TextGrid2WordList(PATH_TEST_DATASET_NEW + audio + PHRASE_ANNOTATION_EXT)
	writeListOfListToTextFile(annotationPhraseListA, '', PATH_TEST_DATASET_NEW + audio + '.anno')
