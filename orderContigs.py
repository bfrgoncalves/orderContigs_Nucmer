#!/usr/bin/python
import subprocess
import argparse
import os
import shutil
from os import listdir
from os.path import isfile, join, isdir
from datetime import datetime


from cluster_utils import create_pickle, create_Jobs
import pickle
import sys


def main():

	parser = argparse.ArgumentParser(description="This program performs sequence alignments using the NUCmer software")
	parser.add_argument('-q', nargs='?', type=str, help="folder with query fasta files", required=True)
	parser.add_argument('-r', nargs='?', type=str, help="reference file", required=True)
	parser.add_argument('-o', nargs='?', type=str, help='Destination folder', required=True)

	args = parser.parse_args()

	orderContigs(args)

def orderContigs(args):

	print 'Running cluster version'

	onlyfiles = [ f for f in listdir(args.q) if isfile(join(args.q,f)) ]

	job_args = []
	allQueryBasePaths = []

	currentDir = os.getcwd()



	if not os.path.isdir(os.path.join(args.o)):
		os.makedirs(os.path.join(args.o))

	countFiles = 0

	for i in onlyfiles:
		countFiles += 1
		listOfArgs = (os.path.join(currentDir, args.q, i), os.path.join(currentDir, args.r), os.path.join(currentDir, args.o), countFiles, countFiles)
		action = 'NUCmer_Align'
		job_args, allQueryBasePaths = create_pickle(listOfArgs, os.path.join(currentDir, args.o) , job_args, action, 'align', allQueryBasePaths, countFiles)
	
	create_Jobs(job_args, 'nucmer_Alignment.py', allQueryBasePaths)


if __name__ == "__main__":
    main()
