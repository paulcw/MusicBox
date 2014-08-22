
oldEncodeURI = encodeURI
encodeURI = function(x) {
    var newx = oldEncodeURI(x);
    return newx.replace(";", "%3b");
};

// TODO refactor all the stuff about the progressbar
var playing = false;
//var starttime;
//var endtime;
var percentage;
var increment;
var lastFullCheck = null;
var lastTickCheck = 0; // time of last tick check
var tickups = 0;

function debug(x) {
    return;
    //alert(x);
    $('#debuglog').append('<hr/>');
    $('#debuglog').append(x);
}

function tickProgressbar() {

    // see if we need to refresh the whole thing
    // TODO a better way to do this may be to keep
    // track of when we expect the current song to be over.
    tickups++;
    if (tickups > 15) {
        tickups = 0;
        var now = (new Date()).getTime();
        if ((now - lastTickCheck) > 300) {
            updateNowPlaying();
        }
    }

    if (playing) {
        
//        if (starttime === undefined || endtime === undefined)
//            return;
        if (percentage === undefined || increment === undefined)
            return;
        if (percentage >= 100)
            return;
        //var time = (new Date()).getTime() / 1000;
        //var percentage = ((time - starttime) * 100) / (endtime - starttime);
        percentage += increment;
        $('#progressbar').progressbar("option", "value", percentage);
    }
    // else do nothing
}

function stopplaying() {
    playing = false;
    $('#NowPlaying .album,.title,.artist,.filename').text('');
    $('#coverthumbnailholder').text('');
    $('#progressbar').progressbar("option", "value", 0);
}

function updateNowPlaying() {
    // keep it from doing too much work
    var now = (new Date()).getTime();
    if (lastFullCheck != null && (now - lastFullCheck) < 3000) {
        debug('skipping: now: ' + now + "; lastFullCheck: " + lastFullCheck);
        return;
    }
    lastFullCheck = now;
    lastTickCheck = now;
    debug('not skipping: now: ' + now + "; lastFullCheck: " + lastFullCheck);

    $.getJSON("/control.cgi?do=nowplaying", function(data) {
        if (data['filename']) {
            debug('got a fileanme');

            var shit = '';
            for (x in data) {
                shit += x + ": " + data[x] + "; ";
            }
            debug("data: " + shit);

            $('#NowPlaying .filename').text(data['filename']);
//            if (data['meta_title']) {
//                debug("got a meta_title");
                $('#NowPlaying .title').text(data['meta_title']);
                $('#NowPlaying .artist').text(data['meta_artist']);
                $('#NowPlaying .album').text(data['meta_album']);
//            }

            if (data['cover']) {
                $('#coverthumbnailholder').html('<img id="coverthumbnail" src="/cover.cgi?dir=' + encodeURI(data['cover']) + '" />');
            } else {
                $('#coverthumbnailholder').text('');
            }

            // set progbar to current time, set percentage
            percentage = parseInt(data['percent_position']);
            $('#progressbar').progressbar("option", "value", percentage);
            //var now = (new Date()).getTime() / 1000;
            //starttime = now - parseInt(data['time_position']);
            //endtime = starttime + parseInt(data['length']);
            increment = 100 / parseInt(data['length']);

            playing = (data['pause'] != 'yes');
            // TODO use this and above to make play/pause button reflect status
            // (i.e., display differently when playing)

        } else {
            debug("no filename");
            // looks like nothing's playing...
            stopplaying();
        }
        // some available fields:
        // filename
        // meta_album
        // meta_artist
        // meta_comment
        // meta_genre
        // meta_title
        // meta_track
        // meta_year
        // percent_position
        // length
        // time_position
    });
}


/** Takes a URI-encoded path */
function showListing(path) {
    // get the data, insert into div
    $.getJSON("/lister.cgi?dir=" + path, function(data) {

        // set current directory display
        $('#dirname').text(data['directory']);

        // set up directory name and value (or unset if at top)
        if (data['directory']) {
            var idx = data['directory'].lastIndexOf('/');
            var parentDir = data['directory'].substr(0, idx);
            $('#up').text('UP').attr('dir', encodeURI(parentDir));
        } else {
            $('#up').text('').attr('dir', '');
        }

        // subdirs
        if (data['subdirs'].length > 0) {
            $('#subdirs').text('');
            for(var i = 0; i < data['subdirs'].length; i++) {
                $('#subdirs').append('<div class="button subdir" dir="' + encodeURI(data['directory'] + '/' + data['subdirs'][i]) + '">' + data['subdirs'][i] + '</div>');
            }
        } else if (data['cover']) {
            $('#subdirs').html('<img id="coverart" src="/cover.cgi?dir=' + path + '" />');
        } else {
            $('#subdirs').text('');
        }

        // files
        if (data['files'].length > 0) {
            $('#files').html('<div class="dirsongs"></div>');

            if (data['types'].length > 1) {
                $('#files').append('<div id="showtypes"></div>');
                $('#files #showtypes').append('<div id="all" class="button">Show All</div>');
                $('#files #showtypes #all').click(function(evt) {
                        $('#files .song').fadeIn();
                });
                for (var i = 0; i < data['types'].length; i++) {
                    var the_type = data['types'][i];
                    $('#files #showtypes').append('<div id="' + the_type + '" class="button">Show only ' + the_type + '</div>');
                    $('#files #showtypes #' + the_type).click(make_fader_in(the_type));
                    $('#files .dirsongs').append('<span class="playall button" dir="' + encodeURI('/' + the_type + data['directory']) + '">Play all ' + the_type + '</span>'); 
                    $('#files .dirsongs').append('<span class="queueall button" dir="' + encodeURI('/' + the_type + data['directory']) + '">Queue all ' + the_type + '</span>'); 
//                    $('#files .dirsongs').append('<div class="clear"></div>');
                    $('#files .dirsongs').append('<br/><br/>');
                }
            } else {
                $('#files .dirsongs').append('<span class="playall button" dir="' + encodeURI('/' + data['types'][0] + data['directory']) + '">Play all</span>'); 
                $('#files .dirsongs').append('<span class="queueall button" dir="' + encodeURI('/' + data['types'][0] + data['directory']) + '">Queue all</span>'); 
            }

            for(var i = 0; i < data['files'].length; i++) {
                $('#files').append('<div class="song ' + data['files'][i]['type'] + '"></div>');

                // TODO are we sure we can't get the song div above
                // and reuse it below rather than looking it up each time???
                $('#files .song').last().append('<div class="playfile button" file="' + encodeURI('/' + data['files'][i]['type'] + data['directory'] + '/' + data['files'][i]['name']) + '">Play now</div>');
                $('#files .song').last().append('<div class="queuefile button" file="' + encodeURI('/' + data['files'][i]['type'] + data['directory'] + '/' + data['files'][i]['name']) + '">Enqueue</div>');
                $('#files .song').last().append('<div class="listingfilename">' + data['files'][i]['name'] + '</div>'); // why not "filename"? it's used in NowPlaying
                $('#files .song').last().append('<div class="clear"></div>');
            }
        } else {
            $('#files').text('');
        }

        // attach functions

        $('#directories #subdirs .subdir').click(function (evt) {
            //showListing($(this).attr('dir')); // this stopped working mysteriously, even though the equivalent for file elements still works just fine.
            showListing(evt.target.getAttribute('dir'));
        });
        $('#directories #up').click(function (evt) {
            //showListing($(this).attr('dir')); // see above
            showListing(evt.target.getAttribute('dir'));
        });
        // TODO i could probably make that one above by being smarter with classes

        $('#files .playall').click(function (evt) {
            $.post("/control.cgi", {
                       'do': 'playdir',
                       'dir': decodeURI($(this).attr('dir'))
                   }, function(data) {
                //debug('msg:' + data['msg'] + ';error:' + data['error'] + ';stopped:' + data['stopped'] + ';skipped:' + data['skipped'] + ';queue:' + data['queue']);
                   }
            );
            //$.post("/control.cgi?do=playdir&dir=" + $(this).attr('dir'));
            lastFullCheck = null;
            setTimeout(updateNowPlaying, 1000);
            playing = true;
        });
        $('#files .queueall').click(function (evt) {
            $.post("/control.cgi?do=queuedir&dir=" + $(this).attr('dir'));
            if (!playing)
                setTimeout(updateNowPlaying, 1000);
        });
        $('#files .playfile').click(function (evt) {
            $.post("/control.cgi?do=playfile&file=" + $(this).attr('file'));
            lastFullCheck = null;
            setTimeout(updateNowPlaying, 1000);
            playing = true;
        });
        $('#files .queuefile').click(function (evt) {
            $.post("/control.cgi?do=queuefile&file=" + $(this).attr('file'));
            if (!playing)
                setTimeout(updateNowPlaying, 1000);
        });
    });

}

$(document).ready(function () {

    // attach the control functions
    // TODO could I make this smarter, with a single command but using div id as arg? woudl it even be worth it?
    $('#stop').click(function(evt){
        $.post("/control.cgi", {"do":"stop"});
        stopplaying();
    });
    $('#pause').click(function(evt){
        $.post("/control.cgi", {"do":"pause"});
        playing = !playing;
    });
    $('#skipforward').click(function(evt){
        $.post("/control.cgi", {"do":"skipforward"});
        lastFullCheck = null;
        setTimeout(updateNowPlaying, 1000);
        playing = true;
    });
    $('#skipback').click(function(evt){
        $.post("/control.cgi", {"do":"skipback"});
        lastFullCheck = null;
        setTimeout(updateNowPlaying, 1000);
        playing = true;
    });

    // create now playing progressbar
    $("#progressbar").progressbar({
        complete: function(event, ui) { setTimeout(updateNowPlaying, 1000); }
    });
    setInterval(tickProgressbar, 1000);

    $('#directories #toplink').click(function (evt) {
        showListing('');
    });

    // show what's currently playing
    updateNowPlaying();

    // preload the data section
    showListing('');
});

/**
 * to allow us to write music type fade in/out functions
 * the tricky part is that javascript seems to have one giant
 * environment, and "var" does NOT define something within
 * a smaller, limited scope.  So closures don't really act
 * like closures sometimes.
 */
function make_fader_in(the_type) {
    return function(evt) {
        $('#files .song').fadeOut();
        $('#files .' + the_type).fadeIn();
    };
}

