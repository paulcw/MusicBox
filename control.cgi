#!/usr/bin/python


# A script to tell mplayer what to play.

import sys
import cgi
import os
from time import sleep
#import urlparse
from urllib import quote_plus
#import base64
#from StringIO import StringIO
#import pickle
import json

ROOT='/nas/media/Music'
CONTROL='/home/music/mplayercontrol'
CONSOLE="/home/music/mplayer.output"

def is_music_filename(x):
    if x.startswith('.'): return False 
    if x.endswith(".ogg") or x.endswith(".wma") or x.endswith('mp3') or x.endswith('flac') or x.endswith('m4a'): return True
    return False


def queue_all(thedir, mplayer, stop_current=False):
    #open the directory and play every music file found there
    status = {'msg': 'queueing everything'}
    status['dir'] = thedir
    status['queue'] = []
    status['skipped'] = []
    status['stopped'] = False

    #global trace

    stopped = False

    #trace.write("in queue_all 1\n")

    #trace.write("about to list dir, root: %s ; thedir: %s\n" % (ROOT, thedir))
    #trace.write("types: root: %s ; thedir: %s\n" % (type(ROOT), type(thedir)))
    #entries = filter(is_music_filename, os.listdir(ROOT + thedir))
    entries = os.listdir(ROOT + thedir)
    #trace.write("entries is at first %s\n" % entries)
    entries = filter(is_music_filename, entries)

    #trace.write("in queue_all entries is %s\n" % entries)

    if len(entries) > 0:
        entries.sort()
        for f in entries:
            fulldir = ROOT + thedir + '/' + f
            if os.path.isdir(fulldir):
                status['skipped'].append({'name': f, 'reason': 'directory'})
                continue
            if stop_current and not stopped:
                # only stop what's playing currently, if we find something
                # new to play
                status['stopped'] = True
                mplayer.write('stop\n')
                stopped = True
            status['queue'].append(fulldir)
            mplayer.write('loadfile "%s" 1\n' % fulldir)
    else:
        status['error'] = 'no recordings found in this directory'

    #trace.write("in queue_all end\n")
    print json.dumps(status)


print "Expires: 0" # hack to mitigate the fact that
# args are currently GET query strings.  they should be POST

print "Content-type: application/json\r\n\r\n"
sys.stdout.flush() # for better debugging, when there's an error
# otherwise, error msgs get sent before this header, and it confuses apache

f = cgi.FieldStorage()

#os.system('whoami')
#os.system('id')
if not f.has_key('do'):
    print "{error: 'you didnt say what to do'}"
    sys.exit(0)

mplayer = open(CONTROL, "a")

do = f['do'].value

#trace = open('/tmp/jukebox-trace.log', 'a')
#trace.write("do is %s\n" % do)


if do == 'stop': 
    mplayer.write("stop\n")
    print '{did: "stopped"}'

elif do == 'pause': 
    mplayer.write("pause\n")
    print '{did: "paused/unpaused"}'

elif do == 'skipforward':
    mplayer.write("pt_step 1\n")
    print '{did: "skipped forward"}'

elif do == 'skipback':
    mplayer.write("pt_step -1\n")
    print '{did: "skipped back"}'

# When you "play" a song (as opposed to queuing it)
# it stops whatever is playing currently.  So "play all"
# really means stop and queue all. (otherwise, it would play
# then stop every song queued, until finally playing only the last song)
elif do == 'playdir': 
    #trace.write("got here\n")
    queue_all(f['dir'].value, mplayer, True)
    #trace.write("got here 2\n")
    

elif do == 'playfile': 
    thefile = f['file'].value
    mplayer.write('loadfile "%s%s"\n' % (ROOT, thefile))
    print "{status: 'playing %s'}" % thefile

elif do == 'queuedir': 
    queue_all(f['dir'].value, mplayer)

elif do == 'queuefile': 
    thefile = f['file'].value
    mplayer.write('loadfile "%s%s" 1\n' % (ROOT, thefile))
    print "{status: 'queuing %s'}" % thefile

elif do == 'nowplaying':
    # you write commands to the FIFO, but must read from the console
    # (where mplayer writes the data you request)
    #print con.readline()
    #trace.write("in nowplaying\n")
    filestats = os.stat(CONSOLE)
    #trace.write("in nowplaying 2\n")
    #print str(filestats)

    size = filestats[6]

    #trace.write("current console size is " + str(size) + "\n")

    # Print out the full pathname of the current file.
    mplayer.write('pausing_keep get_property path\n')
    # Print out the name of the current file.
    mplayer.write('pausing_keep get_file_name\n')
    # Print out the 'Album' metadata of the current file.
    mplayer.write('pausing_keep get_meta_album\n')
    # Print out the 'Artist' metadata of the current file.
    mplayer.write('pausing_keep get_meta_artist\n')
    # Print out the 'Comment' metadata of the current file.
    mplayer.write('pausing_keep get_meta_comment\n')
    # Print out the 'Genre' metadata of the current file.
    mplayer.write('pausing_keep get_meta_genre\n')
    # Print out the 'Title' metadata of the current file.
    mplayer.write('pausing_keep get_meta_title\n')
    # Print out the 'Track Number' metadata of the current file.
    mplayer.write('pausing_keep get_meta_track\n')
    # Print out the 'Year' metadata of the current file.
    mplayer.write('pausing_keep get_meta_year\n')
    # Print out the current position in the file, as integer percentage [0-100).
    mplayer.write('pausing_keep get_percent_pos\n')
    # Print out the length of the current file in seconds.
    mplayer.write('pausing_keep get_time_length\n')
    # Print out the current position in the file in seconds, as float.
    mplayer.write('pausing_keep get_time_pos\n')
    # Print out current pause state
    mplayer.write('pausing_keep_force get_property pause\n')

    mplayer.flush()

    sleep(1) # give mplayer a second to write

    # the following is for a case where it wouldn't find the
    # metadata when asked (above).
    # oddly, this waiting code never seems to wait...
    # I think the filestat actually causes something to flush,
    # thus preventing the condition where the data isn't read...
    tries = 0
    while tries < 3:
        filestats = os.stat(CONSOLE)
        newsize = filestats[6]
        #trace.write("current console newsize is " + str(newsize) + "\n")
        if newsize > size:
            break
        sleep(1) # give it another second
        tries += 1

    con = file(CONSOLE)

    #con.seek(0, 2) # move position to end of file
    # move head to position BEFORE WE ASKED FOR DATA
    con.seek(size)
    #print con.tell()
    #print con.tell()

    rawdata = con.readlines()

    #trace.write("rawdata is %s\n" % rawdata)

    data = {}

    # turn data into json
    for datum in rawdata:
        if not datum.startswith("ANS_"):
            # no idea what's going on here.  skip it.
            continue
        key, value = datum.split('=', 1);
        key = key[4:].lower() # skip the "ANS_"
        value = value.strip()
        value = value.strip("'")
        data[key] = value

    # TODO is this just a hack?
    # Not necessarily, but there's no reason it needs to be in this program.
    # It makes more sense to put this in web page and cover.cgi.
    # Well, maybe.  Can we just let a 404 denote lack of presense?
    # Would that suck?
    if data.has_key('filename'):
        # there wouldn't be a filename, or a lot of stuff, if nothing is playing
        directory = data['path'][0:-len(data['filename'])]
        if os.path.exists(directory + 'cover.jpg'):
            data['cover'] = directory[len(ROOT):]

    print json.dumps(data)

    con.close()

else:
    print "{error: 'I do not know what you mean'}"

#trace.close()

mplayer.close()


