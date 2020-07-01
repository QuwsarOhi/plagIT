# -*- coding: utf-8 -*-

import sys
import os
import re
import string
from glob import glob
from difflib import SequenceMatcher

HELP = \
"""
------------------------------------------------------
plugIT: A plagiarism checker for programming languages
------------------------------------------------------

plugIT is a plagiarism checker that checks for plagiarism based
on the lexical changes of two scripts. The changes made to a script 
using variables, new lines, comments, line numbers, and identifiers 
are referred to as the lexical changes. plugIT ignores the lexical 
changes and tries to match two or more scripts.

plagIT currently supports plagiarism check on c, c++, python, and 
java.

---------------------
Command instructions:
---------------------
Currently, two types of instructions are available. 

* A versus check that checks for a match in single pair of files.
command: "plagIT [filedirectory1] [filedirectory2]"

* A batch check that checks for a match for all possible pairs of 
  files. All the files must be in the "codes" folder. 
command: "plagIT"
"""
ERR = \
"""\n'codes' directory not found!
execute 'plagIT -h' for instruction"""



# returns the keywords of the given programming language
def extract_keywords(lang):
	if lang == "cpp" or lang == 'c':
		with open(os.path.join('keywords', 'cpp.txt')) as f:
			return f.read().split()
	elif lang == "py":
		pass
	elif lang == "java":
		pass



# extracts the script type using file name
def script_type(filedir):
	return filedir.split('.')[-1] 



# the parser parses the input script files based
def parser(filedir):
    ret = []
    keywords = set(extract_keywords(script_type(filedir)))

    with open(filedir) as f:
    	# read line by lines
        for line in f.readlines():
        	# exclude starting and ending whitespaces
            line = line.strip()
            
            # ignore the full line comments
            if line.startswith('//') or line.startswith('#'):
                continue
            # ignore the comments after the script
            line = line[:line.find('//')]
            line = line[:line.find('#')]

            # split words based on spaces
            data = line.split()

            for dat in data:
                vals = re.split(f"[{string.punctuation}]", dat)
                for val in vals:
                    if val in keywords or len(val) == 0:
                        continue
                    ret.append(val)
    return ret


# check for match between two files
def matcher(file1, file2):
	parsed1 = parser(file1)
	parsed2 = parser(file2)

	match_ratio = round(SequenceMatcher(None, parsed1, parsed2).ratio(), 2)
	return match_ratio


THRES = 0.85
def checkall(log=False):
	extentions = ['c', 'cpp', 'py', 'java']
	path = os.path.join('codes', '*.')
	filedirs = []
	logindex = 0

	for ext in extentions:
		filedirs = filedirs + glob(path+ext, recursive=True)
	
	totalfiles = len(filedirs)
	for i in range(totalfiles):
		for j in range(i+1, totalfiles):
			ratio = matcher(filedirs[i], filedirs[j])
			if ratio >= THRES:
				if log == True:
					makelog(filedirs[i], filedirs[j], ratio, logid=logindex)
					logindex += 1
				print(os.path.split(filedirs[i])[-1], 
					  os.path.split(filedirs[j])[-1], 
					  ratio)


# the log writer
def makelog(file1, file2, ratio, logid=0):
	fname1 = os.path.split(file1)[-1]
	fname2 = os.path.split(file2)[-1]
	full_match = False

	if ratio == 1:
		with open(file1) as f1:
			with open(file2) as f2:
				if f1.read() == f2.read():
					full_match = True
	
	writer = "Match Ratio: " + str(ratio) + "\nFull Match: " + str(full_match) + "\n\n"

	writer += fname1 + "\n" + "-"*30 + "\n"
	with open(file1) as f:
		writer += f.read()

	writer += "\n\n" + fname2 + "\n" + "-"*30 + "\n"
	with open(file2) as f:
		writer += f.read()

	logpath = os.path.join('logs')
	if not os.path.exists(logpath):
		os.mkdir(logpath)
	with open(os.path.join(logpath, f"{logid}.txt"), "w") as f:
		f.write(writer)


if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1].startswith("-h"):
		print(HELP)	
	elif len(sys.argv) >= 3:
		file1 = sys.argv[1]
		file2 = sys.argv[2]
		ratio = matcher(file1, file2)
		print("Ratio:", ratio)
		if sys.argv[-1].startswith('-l') and ratio >= THRES:
			if len(sys.argv[-1]) > 2:
				makelog(file1, file2, ratio, logid=sys.argv[-1][2:])
			else:
				makelog(file1, file2, ratio, logid=0)
	else:
		if os.path.exists('codes'):
			if sys.argv[-1].startswith('-l'):
				checkall(log=True)
			else:
				checkall()
		else:
			print(ERR)