#!/usr/bin/python
#builder.py

import shutil
import argparse
import os, sys

def enum(**enums):
    return type('Enum', (), enums)

Levels = enum(debug='[DEBUG]', info='[INFO]', warns='[WARN]', error='[ERROR]', fatal='[FATAL]')

DEBUG = False

def log(level, message):
    if level == Levels.debug and not DEBUG:
        return
    print level, message

parser = argparse.ArgumentParser('This is a builder script to deploy webapps')
parser.add_argument('-s','--source', dest='source', default='../src/', help='This is the source dir of the webapp to deploy.')
parser.add_argument('-d','--destination', dest='destination', default='/usr/share/nginx/html/staging/', help='The location to deploy the project')
parser.add_argument('-x','--debug', dest='debug', default=False, help='Turn debug level output on.')

args = parser.parse_args()
DEBUG = args.debug
log(Levels.debug, ' '.join([value for value in vars(args)]))

dest = args.destination
source = args.source
log(Levels.info, "Deploying application to %s from %s"%(dest, source))
log(Levels.debug, "Current directory: %s"%os.getcwd())

#TODO: maybe some validation, or support for ftp?
if os.path.exists(dest):
    log(Levels.debug, "Directory %s already exists. Removing entire directory."%dest)
    shutil.rmtree(dest)
try:
	shutil.copytree(source, dest)
except shutil.Error as e:
	log(Levels.error, "There was an error deploying the app:")
	for error in e:
		log(Levels.error, `error`)

log(Levels.info, "Successfully depoloyed web app to %s"%dest)
