#!/usr/bin/python
import os
import subprocess
from datetime import datetime
import sys


def func_NUCmer_alignment(query, reference, outputFolder, countFiles):
	
	deltaPath =  os.path.join(outputFolder, outputFolder + '_' + str(countFiles))
	
	subprocess.call(['nucmer', '-p', deltaPath, reference, query]);

	deltaFile = deltaPath + '.delta'
	deltaFilefiltered = deltaPath + 'Filtered.delta'
	with open(deltaFilefiltered, "w") as outfile:
		subprocess.call(['delta-filter', '-i', '0.8',  '-l', '1000', deltaFile], stdout = outfile);

	coordFile = deltaPath + '.coords'
	with open(coordFile, "w") as outfile:
		subprocess.call(['show-coords', '-r', '-c', '-l', deltaFilefiltered], stdout = outfile)

	return deltaPath
