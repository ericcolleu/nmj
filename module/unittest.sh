#!/bin/sh

rm -rf html
nosetests --cover-html --cover-html-dir=./html -v --with-coverage --cover-package=nmj $*
