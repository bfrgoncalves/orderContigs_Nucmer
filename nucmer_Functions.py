#!/usr/bin/python
import os
import subprocess
from datetime import datetime
import sys
import ntpath


def func_NUCmer_alignment(query, reference, outputFolder, countFiles):

	queryFileName = ntpath.basename(query)
	queryFileName = queryFileName.split('.')
	del queryFileName[-1]

	queryFileName = '_'.join(queryFileName)
	
	deltaPath =  os.path.join(outputFolder, 'results_' + str(queryFileName))
	
	subprocess.call(['nucmer', '-p', deltaPath, reference, query]);

	deltaFile = deltaPath + '.delta'
	deltaFilefiltered = deltaPath + 'Filtered.delta'
	with open(deltaFilefiltered, "w") as outfile:
		subprocess.call(['delta-filter', '-i', '0.8',  '-l', '1000', deltaFile], stdout = outfile);

	coordFile = deltaPath + '.coords'
	with open(coordFile, "w") as outfile:
		subprocess.call(['show-coords', '-r', '-c', '-l', deltaFilefiltered], stdout = outfile)

	os.remove(deltaFile)
	os.remove(deltaFilefiltered)


	results = orderContigs(coordFile)


	resultsFile = deltaPath + '.tab'
	with open(resultsFile, "w") as outfile3:
		outfile3.write('reference\tquery\trefStart\tqueryStart\trefEnd\tqueryEnd\tidentity\n')
		for i in results:
			outfile3.write(i['reference']+'\t'+i['query'].strip('\n')+'\t'+i['refStart']+'\t'+i['queryStart']+'\t'+i['refEnd']+'\t'+i['queryEnd']+'\t'+i['identity']+'\n')

	return deltaPath


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