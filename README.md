# plagIT
 A plagiarism checker for programming languages

plugIT is a plagiarism checker that checks for plagiarism based
on the lexical changes of two scripts. The changes made to a script 
using variables, new lines, comments, line numbers, and identifiers 
are referred to as the lexical changes. plugIT ignores the lexical 
changes and tries to match two or more scripts.

plagIT currently supports plagiarism check on c, c++, python, and 
java.


Command instructions:
---------------------
Currently, two types of instructions are available. 

* A versus check that checks for a match in single pair of files.

command: "plagIT [filedirectory1] [filedirectory2]"

* A batch check that checks for a match for all possible pairs of 
  files. All the files must be in the "codes" folder. 

command: "plagIT"