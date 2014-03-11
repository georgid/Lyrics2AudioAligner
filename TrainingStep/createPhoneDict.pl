#!/usr/bin/perl

# creates pronunciation dict (lexicon). creates one lexicon from wrd and phn level transcpits from alignments in metu. 
# This is a trick since no pronunciation dict is available 
# important :  phoneme end timestamp should not be after the end timestamp of its correposnding word. ASSUME 
# read files
my $alignedPhonemes=$ARGV[0];
my $alignedWords= $ARGV[1];
my $outputfileURI= $ARGV[2];

# open the files
open(IN, "<$alignedPhonemes") or die ("file cannot be opened");
@alignedPhonemes=<IN>;
close(IN);

open(INP, "<$alignedWords") or die ("file cannot be opened");
@alignedWords=<INP>;
close(INP);


open(OUT, ">$outputfileURI ") or die ("cannot open file for output");


$counterPhoneme=0;

# get curr phoneme
$currPhoneme = $alignedPhonemes[$counterPhoneme];
@tokens = split(" ",$currPhoneme);
$endTsCurrPhoneme = $tokens[1];

# loop through words and take ts of end

foreach $alignedWord (@alignedWords) {



my @tokenss = split(" ",$alignedWord);

my $endTsCurrWord = $tokenss[1];

# DEBUG
#print "WARN:", $alignedWord, "\n";

print OUT $tokenss[2], "\t";


# DEBUG
#  print "endTsCurrWord ", $endTsCurrWord, "\n";
 
# go to next phoneme and compare its endTs to the endTs of current word
  while ($endTsCurrWord >= $endTsCurrPhoneme )
  {
  
  #record phoneme of word
  print OUT " ", $tokens[2];
  
  # prepare next phoneme

  $counterPhoneme++;

  # size of alignedPhonemes
  my $alignedPhonemes = @alignedPhonemes;
  exit if ($counterPhoneme + 1 > $alignedPhonemes  );

  # get curr phoneme
  $currPhoneme = $alignedPhonemes[$counterPhoneme];
  @tokens = split(" ",$currPhoneme);
  $endTsCurrPhoneme = $tokens[1];

  # DEBUG  
  # print "endTsCurrPhoneme ", $endTsCurrPhoneme, "\n";


  }

  print OUT "\n";
  

}
close(OUT);








