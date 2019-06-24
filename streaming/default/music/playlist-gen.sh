#!/bin/bash
find $(pwd) -name '*.mp3' -or -name '*.ogg' -or -name '*.flac' > playlist.lst
echo "√ Playlist created ($(cat "${playlist_name}.lst" | wc -l) audio)"
