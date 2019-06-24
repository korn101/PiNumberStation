#!/bin/bash
echo "Name of playlist"
read -r playlist_name

echo "Search mp3 in:"
echo "	directory: $(pwd)/music"
echo "	playlist: ${playlist_name}"
echo "-----------------------------"

find "$(pwd)/music" -name '*.mp3' > "${playlist_name}.lst"
echo "√ Playlist created ($(cat "${playlist_name}.lst" | wc -l) audio)"
