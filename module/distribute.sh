#!/bin/sh

rm -rf deb_dist dist

python setup.py sdist
ARCHIVE=`ls dist/*.tar.gz`
VERSION=`echo $ARCHIVE | awk '{print substr($0,17,3)}'`
py2dsc -m 'Eric Colleu <eric.colleu@gmail.com>' $ARCHIVE
cd deb_dist/python-nmj-$VERSION
touch debian/copyright
debuild

