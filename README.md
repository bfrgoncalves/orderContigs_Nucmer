# orderContigs_Nucmer

# Usage 

`orderContigs.py [-h] [-q QUERYFOLDER] [-r REFERENCEFILE] [-o DESTINATIONFOLDER]`

# Description 

This program performs a NUCmer alignment of a set of query sequence files (.fasta) against a reference and returns a set of files with the contigs ordered, in a .tab format. 

Arguments:
 
  -h show this help message and exit

  -q QUERYFOLDER (Required = True)
  			Folder with the different query files

  -r REFERENCEFILE (Required = True)
  			Path to the fasta file to be used as reference

  -o DESTINATIONFOLDER (Required = True)
  			Output directory
  

# Example of usage


`python orderContigs.py -q queryFiles/ -r referenceFiles/referenceFile.fasta -o results/`


#Dependencies

For ANI analysis

* Biopython http://www.biopython.org

* MUMmer executables in the $PATH, or available on the command line (required for NUCmer alignemnt) http://mummer.sourceforge.net/
