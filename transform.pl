#!/usr/bin/perl

# Script originally developed by Jochen Schwenninger. jochen.schwenninger@iais.fraunhofer.de
# adapted by Georgi Dzhambazov.

use strict;

if ( @ARGV < 2 ) {
    print "$0 transform model output\n";
    exit(1);
}

my $trans_file;
my $model_file;
my $output_file;

my $featureVectorSize = 25;

( $trans_file, $model_file, $output_file ) = @ARGV;

my $read_lines_bias = 0;
my $read_lines_trans = 0;
my @bias;
my @trans;

sub matrix_read_file {
    my ($filename) = @_;
    open (F, $filename) || die "Could not open $filename: $!";
    while (my $line = <F>) {
        chomp($line);
        if ($read_lines_bias > 0) {
        	$line = substr($line, 1);
            (@bias) = split (/\s+/, $line);
            $read_lines_bias--;
        }

        if ($read_lines_trans > 0) {
            $line = substr($line, 1);
            my (@row) = split (/\s+/, $line);
            push (@trans, \@row); # insert the row-array into the outer matrix array
            $read_lines_trans--;
        }

        if ($line =~ /^<BIAS>*/) {
            $read_lines_bias = 1;
        } 
        elsif ($line =~ /^<XFORM> */) {
            #TODO: make this adjustable
        	$read_lines_trans = $featureVectorSize;
        } 
        
    }
    close(F);
}

&matrix_read_file($trans_file);

if (@trans == 0) {
    system("cp $model_file $output_file");
    print "No transformation read, copying $model_file to $output_file\n";
    exit;
}

open (IN, "$model_file") || die "Could not open $model_file: $!";
open (OUT, ">$output_file") || die "Could not open $output_file: $!";
my $edit = 0;
while (my $line = <IN>) {
    chomp($line);
    if ($edit) {
    	$edit = 0;
    	$line = substr($line, 1);
        my (@mean) = split (/\s+/, $line);
        my @new_mean;
        for (my $i = 0; $i < $featureVectorSize; $i++) {
        	my $sum = 0;
        	for (my $j = 0; $j < $featureVectorSize; $j++) {
        		$sum += @trans->[$i][$j] * @mean->[$j];
        	}
        	@new_mean->[$i] = $sum + @bias->[$i]; 
        }
        foreach my $num (@new_mean) {
        	print(OUT " $num");
        }
        print(OUT "\n");
    }
    else {
    	print(OUT "$line\n");
    }
    
    if ($line =~ /^<MEAN>*/) {
    	$edit = 1;
    }
}
    	
close(IN);
close(OUT);

