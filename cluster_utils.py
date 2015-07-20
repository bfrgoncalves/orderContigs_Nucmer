#!/usr/bin/python
import drmaa
import sys
import pickle
import os

def create_pickle(listOfArgs, queryFolder, job_args, action, identifier, allQueryBasePaths, numberOfqueries):

	basepath=os.path.join(queryFolder, "temp")
	allQueryBasePaths.append(basepath)
	if not os.path.exists(basepath):
		os.makedirs(basepath)
	filepath=os.path.join(basepath, identifier + '_' + str(numberOfqueries) + '_' + action+"_argList.txt")
	with open(filepath, 'wb') as f:
		var = listOfArgs
		pickle.dump(var, f)
	job_args.append(filepath)

	return job_args, allQueryBasePaths



def create_Jobs(job_args, pythonScript, allQueryBasePaths):
	joblist = []
	countargList = 0
	with drmaa.Session() as s:
		for argList in job_args:
			jt = s.createJobTemplate()
			jt.remoteCommand = os.path.join(os.getcwd(), pythonScript)
			jt.args = [str(argList),allQueryBasePaths[countargList]]
			jt.joinFiles=True
			jt.nativeSpecification='-V'
			jobid = s.runJob(jt)
			joblist.append(jobid)
			print('Your job has been submitted with ID %s' % jobid)
			with open("jobsid.txt","a") as f:
				f.write(str(argList[0])+"\n"+str(jobid))
			s.deleteJobTemplate(jt)
			countargList +=1
		for curjob in joblist:
			print 'Collecting job ' + curjob
			retval = s.wait(curjob, drmaa.Session.TIMEOUT_WAIT_FOREVER)
			print 'Job: ' + str(retval.jobId) + ' finished with status ' + str(retval.hasExited)