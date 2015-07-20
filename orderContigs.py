

import subprocess
import argparse
import os
import shutil
from os import listdir
from os.path import isfile, join, isdir
import sys
from datetime import datetime


def main():

	parser = argparse.ArgumentParser(description="This program performs sequence alignments using the NUCmer software")
	parser.add_argument('-q', nargs='?', type=str, help="folder with query fasta files", required=True)
	parser.add_argument('-r', nargs='?', type=str, help="reference file", required=True)
	parser.add_argument('-o', nargs='?', type=str, help='Destination folder', required=True)

	args = parser.parse_args()

	orderContigs(args)

def orderContigs(args):

	onlyfiles = [ f for f in listdir(args.q) if isfile(join(args.q,f)) ]

	if not os.path.isdir(os.path.join(args.o)):
		os.makedirs(os.path.join(args.o))

	countFiles = 0

	for i in onlyfiles:
		countFiles += 1
		deltaPath =  os.path.join(args.o, args.o + '_' + str(countFiles))
		subprocess.call(['nucmer', '-p', deltaPath, args.r, os.path.join(args.q,i)]);
		
		deltaFile = deltaPath + '.delta'
		deltaFilefiltered = deltaPath + 'Filtered.delta'
		with open(deltaFilefiltered, "w") as outfile:
			subprocess.call(['delta-filter', '-i', '0.8',  '-l', '1000', deltaFile], stdout = outfile);

		coordFile = deltaPath + '.coords'
		with open(coordFile, "w") as outfile:
			subprocess.call(['show-coords', '-r', '-c', '-l', deltaFilefiltered], stdout = outfile)
		#"delta-filter -i ".$minidentity." -l ".$minAlignment." ".$pathAligment." > ".$pathDeltaF;
        # exec($execution);
        # $execution="show-coords -r -c -l ".$pathDeltaF." > ".$pathCoords;
        os.remove(deltaFile)
        os.remove(deltaFilefiltered)


if __name__ == "__main__":
    main()
