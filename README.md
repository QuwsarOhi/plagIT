# plagIT
 A plagiarism checker for programming languages

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


Command Instruction:
--------------------
plagIT [-h] [-f file file] [-t threshold] [-l [filename]]

Optional arguments:

  -h, --help     show this help message and exit

  -f file file   check plagiarism for two input files

  -t threshold   defines threshold [0, 1] of the match (default=0.85)
  
  -l [filename]  create log file