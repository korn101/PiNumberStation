#!/bin/bash
# Update your playlist.lst with all files into music/ directory

echo "Playlist name? [empty = playlist]"
read -r playlist

if [[ $playlist == "" ]]; then
	playlist="playlist"
fi

find $(pwd) -type f \( -name '*.mp3' -or -name '*.ogg' -or -name '*.flac' \) | sort > "$playlist.lst"

cat $playlist.lst | head -5
echo "..."

files=$(cat "$playlist.lst" | wc -l)
echo "√ ${playlist}.lst updated (${files} files)"
