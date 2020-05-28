#!/usr/bin/bin/liquidsoap --verbose
%include "config.liq"


stream = fallback(track_sensitive=false, [number_station_playlist, number_station_fallback])
stream = add([stream, number_station_scheduled])

# This function is called when
# a new metadata block is passed in
# the stream.
#
#def apply_metadata(m) =
#    title  = m["title"]
#    artist = m["artist"]
#    print("Now playing: #{title} by #{artist}")
#end
#stream = on_metadata(apply_metadata, stream)

output.icecast(
    %mp3(bitrate=256,samplerate=44100,stereo=true),
    name=stream_name,
    mount=stream_mount,
    url=icecast_url, 
    host=icecast_host,
    port=icecast_port, 
    password=icecast_pass,
    fallible=true,
    icy_metadata="true",
    stream
)
