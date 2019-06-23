#!/Users/mirkopapella/.opam/default/bin/liquidsoap -v
%include "config.liq"

radio_station  = playlist("/Users/mirkopapella/Desktop/py-numberstation-v2/playlist.m3u")
number_station = audio_to_stereo(single("/Users/mirkopapella/Desktop/py-numberstation-v2/PiNumberStation/message.wav"))
radio_fallback = single("/Users/mirkopapella/Desktop/py-numberstation-v2/fail.mp3")


number_station_scheduled=switch([ 
	({ 0m-5m },   delay(5., number_station)),
	({ 30m-35m }, delay(5., number_station))
])


radio = fallback(
	track_sensitive=false, 
	[radio_station, radio_fallback]
)
radio = add([radio, number_station_scheduled])

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
	radio
)