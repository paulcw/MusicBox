MusicBox
========

A web interface around mplayer to play music in a way I prefer.
Or really, a prototype thereof.

Hold it!
--------

In retrospect, this project was unnecessary.  Other, probably nicer solutions exist.

tl;dr: Get VLC and a VLC remote controller app, or XMBC and an XMBC remote controller app.

Read on if you want to know more about the context/background of this.

What it's for
-------------

Like all of us, at this point I either buy my music digitally or rip
the CD and only listen to the music files.  But I didn't like the options
of how to listen to stuff:
* In the basic case, you could play music directly on your computer, but this was a pain when
  you wanted to hear music in your living room or kitchen while making eggs.
* You could listen via a portable MP3 player (eg, a smartphone), but that means you always have
  headphones on, or are listening through tiny speakers.  Also you need to carry the MP3 player around,
  which might not be convenient when you're in the kitchen making eggs.
* You could play music on your TV, either directly or using a games console or the like, but that required
  turning on your TV to select music.
* You could put your portable MP3 player in a speaker dock, but now you're
  (probably) manipulating three different pieces of hardware, and limiting
  the amount of music you can use by the storage capacity of the portable
  player.
* You can invest a lot of money in wifi speakers, which still ties you to your computer.
* There are variations of the above using various streaming systems/services, but they didn't seem, to me,
  to improve the situation much.

What I wanted was something that would behave more like a traditional audio
system: a standalone box that just played music, from the MP3 collection,
without being connected to a TV or a full computer.

So the solution was: get a small, cheapest possible computer, put Linux on it,
install Apache and mplayer on it, and connect it to normal external speakers.
The code in this project provides a web interface to select music, and sends it to
mplayer to actually play it.  I use my iPad, typically, to get at the
web interface.  The music is stored on a NAS.

In addition, I attached a small FM transmitter to the player box.
This allows you to use existing music equipment (e.g., an old boom box)
to play from your newly digitized collection without modification.

The result feels like a regular old audio system.  You have speakers and music plays on it.  I didn't have to completely upgrade my audio equipment -- existing speakers/players work just fine.  I'm not tethered to tinny little speakers or earbuds.

Other stuff
-----------
I like arranging my music in an ideosyncratic way: top-level directories
are based on the format of music (e.g., MP3 vs Ogg Vorbis), and then
subdirectories under each, usually based on artist.  (This way, it's easy
to make subsections of your music collection available to devices based on what
they can handle; if you have a player that only knows about MP3s, then copy just
that directory to that device.)  And a lot of music players I've seen do dumb
things with albums -- e.g., you'll search for an album by band name, and if
the album has multiple artist combinations, it'll only list part of the album.
Or if you've ripped an album twice, say in MP3 and Ogg Vorbis, it interleaves the
two copies of the songs (assuming it doesn't ignore the Ogg Vorbis entirely).
The code here tries to at least start mitigating that.


Is it completely finished and ready to go?
------------------------------------------

Oh, God no.  It runs for me but it makes lots of assumptions about
the environment.  Also the UI is ugly.  It has kluges.
It's basically a proof of concept.

Other things that might serve the same purpose
----------------------------------------------

As mentioned above, this project was probably unnecessary because other, existing systems can probably do almost all of the above, and more, at a lower cost.

VLC has a web interface that does a lot of this.  It's probably a better solution.
It doesn't have an interface that I like, but it's extensible; I probably ought to have 
implemented this as extensions to VLC.  That's probably what the next pass of this project will be.

The Google Nexus Q (that sphere) looks like it might do exactly this, including the hardware.
This is such an obvious use case that I'm surprised that no electronics
manufacturers (that I could find, anyway) have made such a thing already.

There's software  called "mpd" which apparently does largely the same thing.
mpd is the server and you can use various clients.  It has a web client.
But I couldn't get it to work, and after fiddling with it, it wasn't clear
whether it really did what I wanted.  You might prefer to work with
that.

A DLNA Player and a DLNA Controller, together, should do the same thing,
especially if the player is connected to audio output instead of or in addition
to video output.  The Controller might just be an app on a smartphone or tablet.
Theoretically, there are cheap (about $100) media players that are DLNA players.
But when I tried this, the interfaces ranged from unintuitive to unworkable.
I think that most equipment manufacturers aren't really thinking about 
controllers and players on two different pieces of hardware, and don't
test these use cases well.  (Since I wrote this paragraph, I've tried other DLNA controller
software that worked better.)

You could get an OUYA and put XMBC on it.  You could get a RaspberryPi and put VLC or XMBC on it.
There are VLC (and XMBC, probably) remote apps for smartphones and tablets which would work just fine with these.
If I were doing this project again, that's what I'd probably do: get a RaspberryPi, put VLC on it, plug in the FM transmitter and some speakers, and install remote apps on tablets.  Problem solved.  Any additional functionality could hopefully be done in an extension language (eg, Lua in VLC) rather than reinventing the wheel.

Other things to note
--------------------

Some stuff here -- in particular, the delegation to mplayer -- is also
done via other projects.  One TODO item is to rework this to use those
projects rather than reinventing the wheel.
(See this: http://code.google.com/p/python-mplayer/wiki/Player)

Currently it uses the CGI interface to Apache; it would make sense to
switch to a more modern web framework, especially one that lets the
server maintain state.  (Why CGI?  It's quick and easy.)

