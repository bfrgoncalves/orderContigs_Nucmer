#!/usr/bin/python
from nucmer_Functions import func_NUCmer_alignment
import sys
import pickle
import os

def main():

	try:
		input_file = sys.argv[1]
		temppath = sys.argv[2]
	except IndexError:
		print "usage: list_pickle_obj"

	argumentList=[]
	
	print type(input_file)
	print input_file
	with open(input_file,'rb') as f:
		argumentList = pickle.load(f)


	def Nucmer_align(args):
	    Nucmer_results = func_NUCmer_alignment(args[0], args[1], args[2], args[3])

	    final =	(args[0], Nucmer_results)

	    filepath=os.path.join(temppath , str(args[4]) +"_NUCmer_Align_result.txt")

	    with open(filepath, 'wb') as f:
			pickle.dump(final, f)

	    return True


	Nucmer_align(argumentList)

if __name__ == "__main__":
    main()