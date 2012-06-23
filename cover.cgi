#!/usr/bin/python

import sys
import cgi
import os

ROOT='/nas/media/Music'
MUSICDIRS = ['', 'mp3', 'ogg', 'wma', 'flac', 'm4a']

#print "Content-type: application/json\r\n\r\n"
#sys.stdout.flush() # for better debugging, when there's an error
# otherwise, error msgs get sent before this header, and it confuses apache

f = cgi.FieldStorage()

if not f.has_key('dir'):
    print "Status: 400\r\n",
    print "Content-type: text/plain\r\n\r\n",
    print "nerror: No path given\r\n"
    sys.exit(0)

for part in MUSICDIRS:
    abspath = ROOT + '/' + part + '/' + f['dir'].value + '/cover.jpg'

    if os.path.exists(abspath) and os.path.isfile(abspath):
        print "Content-type: image/jpeg\r\n\r\n",
        sys.stdout.flush()
        os.system('cat "' + abspath + '"')
        sys.exit(0) # success!

print "Status: 404\r\n",
print "Content-type: text/plain\r\n\r\nerror: No such path, or not a file: %s\r\n" % f['dir'].value

