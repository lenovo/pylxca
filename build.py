# Build script for PyLXCA

#!/usr/bin/env python 
import sys,os
import subprocess

if len(sys.argv) < 2:
	print "Building Repository"
	subprocess.call(sys.executable + " setup.py sdist bdist_egg --exclude-source-file",shell = True)
	print "Done"
	print "Build drop location is: ",  os.getcwd() + "/dist"
elif sys.argv[1] == "clean":
	subprocess.call(sys.executable + " setup.py clean --all",shell = True)
	print "Done"
exit