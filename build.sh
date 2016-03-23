#!/bin/bash
echo "Building Repository"
`which python` setup.py sdist bdist_egg --exclude-source-file
echo "Done"
echo "build drop location: "  `pwd`/dist
