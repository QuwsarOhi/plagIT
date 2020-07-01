# -*- coding: utf-8 -*-
"""copyChecker.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R4ae0CYr2kArlB3_OuIYdzOS3EhEDR3A
"""

from difflib import SequenceMatcher
import json
from glob import glob
import pandas as pd
import re
import string

!mkdir /content/data
#!unzip /content/bubt-iupc-spring-2020-senior.zip -d /content/data
!unzip /content/bubt-iupc-spring-2020-junior.zip -d /content/data

cppfiles = glob('/content/data/*.cpp')
jsonfiles = glob('/content/data/*.json')
cppfiles.sort()
jsonfiles.sort()

keywords = """asm else new this main
auto	enum	operator	throw
bool	explicit	private	true
break	export	protected	try
case	extern	public	typedef
catch	false	register	typeid
char	float	reinterpret_cast	typename
class	for	return	union
const	friend	short	unsigned
const_cast	goto	signed	using
continue	if	sizeof	virtual
default	inline	static	void
delete	int	static_cast	volatile
do	long	struct	wchar_t
double	mutable	switch	while
dynamic_cast	namespace	template
using std include define
bits stdc
iostream
stdio printf scanf cin cout bits 
"""
keywords = set(keywords.split())

def cpp_parser(codefile):
    ret = []
    with open(codefile) as f:
        for line in f.readlines():
            line = line.strip()
            
            # Ignore the comments
            if line.startswith('//'):
                continue
            
            data = line.split()
            for dat in data:
                vals = re.split(f"[{string.punctuation}]", dat)
                #ret = ret + vals
                #print(vals)
                for val in vals:
                    if val in keywords or len(val) == 0:
                        continue
                    #print('adding', val)
                    ret.append(val)
    #print(ret)
    return ret

data = []
data_non_parsed = dict()

for cpp, jsn in zip(cppfiles, jsonfiles):
    fname1 = (((str(cpp).split('/'))[-1]).split('.'))[0]
    fname2 = (((str(jsn).split('/'))[-1]).split('.'))[0]

    if fname1 != fname2:
        print('Error in file', fname1, fname2)

    with open(cpp) as f:
        code = ''.join(cpp_parser(cpp))
    
    with open(jsn) as f:
        jinfo = json.load(f)
    jinfo['code'] = code
    data.append(jinfo)

    # Read the orginal code, to manually check
    with open(cpp) as f:
        jinfo['code'] = f.read()
    data_non_parsed[jinfo['id']] = jinfo

ratio = 0.3
skipped_problems = [1173, 1171, 1169]

for i in range(len(data)):
    if data[i]['verdict'] != 'ACCEPTED': continue
    if data[i]['problem_id'] in skipped_problems: continue

    same = set()
    minmatch = 1
    for j in range(i+1, len(data)):
        if data[j]['problem_id'] in skipped_problems: continue
        if data[j]['verdict'] != 'ACCEPTED': continue
        if data[i]['problem_id'] != data[j]['problem_id']: continue
        if data[i]['user_id'] == data[j]['user_id']: continue
        #if data[i]['contest_id'] == data[j]['contest_id']: continue

        r = SequenceMatcher(None, data[i]['code'], data[j]['code']).ratio()
        if r >= ratio:
            same.add((data[j]['id'], data[j]['user_id'], data[j]['contest_id']))
            same.add((data[i]['id'], data[i]['user_id'], data[i]['contest_id']))
            minmatch = min(minmatch, r)
            print(f"{data[i]['problem_id']}, {same}, {minmatch:.2f}")
            same.clear()

    #if len(same) != 0:
    #    print(f"{data[i]['problem_id']}, {same}, {minmatch:.2f}")

print(data_non_parsed[16071]['code'])

print(data_non_parsed[15786]['code'])

