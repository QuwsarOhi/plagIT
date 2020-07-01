# -*- coding: utf-8 -*-

import sys
import os
import re
import string
from argparse import ArgumentParser, RawDescriptionHelpFormatter
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

Currently, two types of instructions are available. 

* A versus check that checks for a match in single pair of files.
* A batch check that checks for a match for all possible pairs of 
  files. All the files must be in the "codes" folder. 
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
        with open(os.path.join('keywords', 'python.txt')) as f:
            return f.read().split()
    elif lang == "java":
        with open(os.path.join('keywords', 'java.txt')) as f:
            return f.read().split()
    else:
        raise NameError('Invalid file name extention', lang)


# extracts the script type using file name
def script_type(filedir):
    return filedir.split('.')[-1] 



# the parser parses the input script files based
def codeParser(filedir):
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
    parsed1 = codeParser(file1)
    parsed2 = codeParser(file2)

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
    parser = ArgumentParser(prog="plagIT",
                            formatter_class=RawDescriptionHelpFormatter,
                            description=HELP
                           )
    parser.add_argument('-f', metavar='file', nargs=2, 
                        help='check plagiarism for two input files')
    parser.add_argument('-t', metavar='threshold', 
                        help='defines threshold [0, 1] of the match (default=0.85)')
    parser.add_argument('-l', metavar='filename', nargs='?', default='0',
                        help='create log file')
    args = parser.parse_args()

    if args.t:
        THRES = float(args.t)
    
    if args.f:
        file1 = args.f[0]
        file2 = args.f[1]
        ratio = matcher(file1, file2)
        print("Ratio:", ratio)
        if args.l != '0' and ratio >= THRES:
            makelog(file1, file2, ratio, logid=args.l)
    else:
        if os.path.exists('codes'):
            checkall(log=(args.l != '0'))
        else:
            print(ERR)
