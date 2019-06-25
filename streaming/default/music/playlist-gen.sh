#!/bin/bash
# Update your playlist.lst with all files into music/ directory

echo "Playlist name? [empty = playlist]"
read -r playlist

if [[ $playlist == "" ]]; then
	playlist="playlist"
fi

find $(pwd) -name '*.mp3' -or -name '*.ogg' -or -name '*.flac' > ${playlist}.lst
files=$(cat "${playlist}.lst" | wc -l)

echo "√ ${playlist}.lst updated (${files} files)"
