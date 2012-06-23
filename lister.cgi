#!/usr/bin/python

# Basically, this is a program to list the music files
# I have on my server.
# Making mplayer play the songs is delegated to script "control.cgi"

# TODO make it read ID3/Ogg tags.
# See Python Mutagen library.

# Arguably this whole thing is a waste.
# "mpd" apparently does the same thing already, probably better.
# Nah, I tried it and it didn't work out.

import sys
import cgi
import os
import json

ROOT='/nas/media/Music'
MUSICDIRS = ['mp3', 'ogg', 'wma', 'flac', 'm4a']

print "Content-type: application/json\r\n\r\n"
sys.stdout.flush() # for better debugging, when there's an error
# otherwise, error msgs get sent before this header, and it confuses apache


f = cgi.FieldStorage()

#absdir = ROOT # to be used to talk to shell
#reldir = ''   # to be used to put in html args
#
#if f.has_key('dir'):
#    absdir += f['dir'].value
#    reldir = f['dir'].value
#
#if not os.path.exists(absdir):
#    print "{error: 'No such directory: %s'}" % absdir
#    sys.exit(0)
#if not os.path.isdir(absdir):
#    print "{error: 'Not a directory: %s'}" % absdir
#    sys.exit(0)


path = ''
if f.has_key('dir'):
    path = f['dir'].value

data = {}

data['directory'] = path
data['files'] = []
data['mystery'] = []

paths = []
for area in MUSICDIRS:
    abspath = ROOT + '/' + area
    if path: abspath += '/' + path
    if os.path.exists(abspath) and os.path.isdir(abspath):
        paths.append({'path':abspath, 'type':area})

if not paths:
    print "{error: 'No such directory: %s'}" % path
    sys.exit(0)

types = {}
dirs = {}

for apath in paths:
    entries = filter(lambda x: not x.startswith('.'), os.listdir(apath['path']))
    entries.sort()

    for d in entries:
        #print "<li>raw: %s</li>" % d
        if os.path.isdir(apath['path'] + '/' + d):
            dirs[d] = 1

        #else, must be a file

        elif d.endswith(".ogg") or d.endswith(".wma") or d.endswith('mp3') or d.endswith('.flac') or d.endswith('.m4a'):
            data['files'].append({'name':d, 'type':apath['type']})
            types[apath['type']] = 1 # found a music file of this type

        elif d == 'cover.jpg':
            data['cover'] = d
            # TODO: support any image (say, scanned liner notes?) 
            # or with different extensions?

        else:
            data['mystery'].append(d)

data['types'] = types.keys()        
data['subdirs'] = dirs.keys()
data['subdirs'].sort()

print json.dumps(data)

