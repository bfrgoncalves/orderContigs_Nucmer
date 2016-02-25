

import subprocess
import argparse
import os
import shutil
from os import listdir
from os.path import isfile, join, isdir
import sys
from datetime import datetime


def main():

	parser = argparse.ArgumentParser(description="This program performs sequence alignments using the NUCmer software and returns the contigs ordered against a reference")
	parser.add_argument('-q', nargs='?', type=str, help="folder with query fasta files", required=True)
	parser.add_argument('-r', nargs='?', type=str, help="reference file", required=True)
	parser.add_argument('-o', nargs='?', type=str, help='Destination folder', required=True)

	args = parser.parse_args()

	nucmer_Align(args)

def nucmer_Align(args):

	onlyfiles = [ f for f in listdir(args.q) if isfile(join(args.q,f)) ]

	resultsFolderName = os.path.relpath(args.o)


	if not os.path.isdir(os.path.join(args.o)):
		os.makedirs(os.path.join(args.o))

	countFiles = 0
	deltaPaths = []

	for i in onlyfiles:
		countFiles += 1
		deltaPath =  os.path.join(os.getcwd(), args.o,  resultsFolderName + '_' + str(countFiles))
		subprocess.call(['nucmer', '-p', deltaPath, args.r, os.path.join(args.q,i)]);

		deltaPaths.append(deltaPath)
		
		deltaFile = deltaPath + '.delta'
		deltaFilefiltered = deltaPath + 'Filtered.delta'
		
		with open(deltaFilefiltered, "w") as outfile1:
			subprocess.call(['delta-filter', '-i', '0.8',  '-l', '1000', deltaFile], stdout = outfile1)

		coordFile = deltaPath + '.coords'
		
		with open(coordFile, "w") as outfile2:
			subprocess.call(['show-coords', '-r', '-c', '-l', deltaFilefiltered], stdout = outfile2)

		
		try:
			os.remove(deltaFile)
			os.remove(deltaFilefiltered)

			results = orderContigs(coordFile)

			resultsFile = os.path.join(os.getcwd(), args.o,  resultsFolderName + os.path.splitext(i)[0]) + '.tab'

			with open(resultsFile, "w") as outfile3:
				outfile3.write('reference\tquery\trefStart\tqueryStart\trefEnd\tqueryEnd\tidentity\n')
				for i in results:
					outfile3.write(i['reference']+'\t'+i['query'].strip('\n')+'\t'+i['refStart']+'\t'+i['queryStart']+'\t'+i['refEnd']+'\t'+i['queryEnd']+'\t'+i['identity']+'\n')

			os.remove(coordFile)

		except OSError:
			"Not a sequence file"

		


def orderContigs(coordResults):

	coordObject = readCoordFile(coordResults)
	queryList = []
	results = []
	for i in coordObject['results']:
		if i['query'] not in queryList:
			results.append(i)
			queryList.append(i['query'])

	return results

def readCoordFile(coordR):

	coordObject = {}
	coordObject['results'] = []
	with open(coordR, "r") as outfile:
		allLines = outfile.readlines()
		lengthFile = len(allLines)
		for i in range(5, lengthFile-1):
			line = allLines[i].split(' ')
			inLine = []
			for i in line:
				if i != '':
					inLine.append(i)

			lineObject = {}
			lineObject['queryStart'] = inLine[0]
			lineObject['queryEnd'] = inLine[1]
			lineObject['refStart'] = inLine[3]
			lineObject['refEnd'] = inLine[4]
			lineObject['identity'] = inLine[9]
			lineObject['reference'] = inLine[17].split('\t')[0]
			lineObject['query'] = inLine[17].split('\t')[1]

			coordObject['results'].append(lineObject)

	return coordObject

if __name__ == "__main__":
    main()
