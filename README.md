MusicBox
========

A web interface around mplayer to play music in a way I prefer.

What it''s for
-------------

Like all of us, at this point I either buy my music digitally or rip
the CD and only listen to the music files.  But I didn''t like the options
of how to listen to stuff:
* You could play music via a games console or the like, but that required
  turning on your TV to select music (or just to listen to music unless you
  have a second audio on on your console).
* You could play music directly on your computer, but this was a pain when
  you wanted to hear music in your living room or kitchen while making eggs.
* You could listen via an MP3 player, but that means you always have headphones
  on, or are listening through tiny speakers.  Also you need a way to carry
  the MP3 player around, which means you have to wear pants.  This might not
  be convenient when you''re in the kitchen making eggs.

What I wanted was something that would behave more like a traditional audio
system: a standalone box that just played music, from the MP3 collection,
without being connected to a TV.

Also, I like arranging my music in a particular way: top-level directories
are based on the format of music (e.g., MP3 vs Ogg Vorbis), and then
subdirectories under each, usually based on artist.  This way, it''s easy
to make subsections of your music collection available to devices based on what
they can handle; if you have a player that only knows about MP3s, then copy just
that directory to that device.

So the solution was: get a small, cheapest possible computer, put Linux on it,
install Apache and mplayer on it, and connect it to normal external speakers.
The code here uses Apache to provide a web interface to select music, and it
uses mplayer to actually play it.  I use my iPad, typically, to get at the
web interface.


Is it completely finished and ready to go?
------------------------------------------

Oh, God no.  It runs for me but it makes lots of assumptions about
the environment.  Also the UI is ugly.

Other things that might serve the same purpose
----------------------------------------------

There''s a thing called "mpd" which apparently does largely the same thing.
But I couldn''t get it to work, and from fiddling with it, it wasn''t clear
whether it really did the same thing or not.  You might prefer to work with
that, than this.

A DLNA Player and a DLNA Controller, together, should do the same thing,
especially if the player is connected to audio output instead of or in addition
to video output.  The Controller might just be an app on a smartphone or tablet.
Theoretically, there are cheap (about $100) media players that are DLNA players.
But when I tried this, the interfaces ranged from unintuitive to unworkable.
I think that most equipment manufacturers aren''t really thinking about 
controllers and players on two different pieces of hardware, and don''t
test these scenarios well.

Other things to note
--------------------

Some stuff here -- in particular, the delegation to mplayer -- is also
done via other projects.  I should consider reworking this to use those
projects rather than reinventing the wheel.

Currently it uses the CGI interface to Apache; I plan on switching to
mod_python.  It looks much nicer to work with, although it might also
create stronger dependencies on Apache.  I don''t really care about that though.


