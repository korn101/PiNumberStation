#################################################
# LiquidSoap settings
##################################################
set("log.level", 3)
set("log.stdout", true)

set("log.file", false)
set("log.file.path", "liquidsoap.log")   # filename or path/filene.log

#directory=get_process_lines("pwd")[0]
#print(directory)

#################################################
# Icecast settings
# The same of your icecast config
# /etc/icecast.xml, /usr/local/etc/icecast.xml
#################################################
icecast_host="radio17.mooo.com"
icecast_url="http://radio17.mooo.com/radio"
icecast_port=8888
icecast_pass="papella"

###################
# stream
####################

# Name of your radio
stream_name="PiNumberStation"

# URL for listen radio (icecast_url + /radio in this case)
stream_mount="radio"


######################################
# NumberStation setup
#
# NB: Use absolute path for single()
######################################
# playlist to play 
number_station_playlist = playlist("/Users/mirkopapella/Desktop/py-numberstation-v2/PiNumberStation/streaming/default/music/playlist.lst", reload=3600)

# source fallback
number_station_fallback = single("/Users/mirkopapella/Desktop/py-numberstation-v2/PiNumberStation/streaming/default/samples/fail.mp3")                   	

# audio of message (wrap into audio_to_stereo() pls)
number_station_message  = audio_to_stereo(single("message.wav"))   				    

# Scheduling message
# Syntax is 
#	({ range }, source)
# 
# 00:00 -> 01:00   
# 30:00 -> 31:00
# 
# See https://www.liquidsoap.info/doc-dev/language.html
number_station_scheduled=switch([
    ({ 0m-1m },  amplify(4., number_station_message)),
    ({ 30m-31m}, amplify(4., number_station_message))
])
