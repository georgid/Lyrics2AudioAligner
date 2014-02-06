#!/bin/bash



awk '{ for (i=2; i<=NF; i++)  print $i}' kani_karaca-hicaz-durak.lexicon > kani_karaca-hicaz-durak.phn.tmp

awk 'NR==FNR {a[FNR""]=$0 ; next} {print $1, a[FNR""]}' kani_karaca-hicaz-durak.phn.tmp kani_karaca-hicaz-durak.annotation.phn.txt 

rm kani_karaca-hicaz-durak.phn.tmp