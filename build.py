"""
Build script to build repository
"""
#!/usr/bin/env python
# Build Script
import sys
import os
import subprocess

if len(sys.argv)<2 :
    print ("Building Repository")
    CONST_RET = subprocess.call(sys.executable + " setup.py sdist bdist_wheel", shell = True)
    print ("Done ", CONST_RET)
    print ("Build drop location is: ",  os.getcwd() + "/dist")
elif sys.argv[1] == "clean":
    CONST_RET = subprocess.call(sys.executable + " setup.py clean --all", shell = True)
    print ("Done ", CONST_RET)
sys.exit(CONST_RET)
