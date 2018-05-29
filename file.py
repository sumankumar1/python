import sys

if len(sys.argv) !=3:
	exit('Syntax: filecopy1.py filename copyname')
ifile = open(sys.argv[1],'r')
ofile = open(sys.argv[2],'w')
for line in ifile:
	ofile.write(line)
ifile.close()
ofile.close()