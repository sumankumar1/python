#! /usr/bin/python3

import sys

who=sys.argv[1] if len(sys.argv)>1 else 'world'
print ('Hello',who)