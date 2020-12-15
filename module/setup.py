#!/usr/bin/env python

from distutils.core import setup

setup(
	name='python-nmj',
	version='2.0',
	description="""Python tool for popcorn hour NMJV2 database update.
  Retreive french informations on movies and TV shows from www.themoviedb.org and thetvdb.com""",
	author='PyNMJ Team',
	author_email='pynmj@gmail.com',
	url='https://code.google.com/p/pynmj/',
	packages=[
		'nmj',
		'nmj.db',
		'nmj.scanners',
	],
	scripts=['scripts/pynmj',]
)


