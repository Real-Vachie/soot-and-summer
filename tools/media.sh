#!/bin/bash
# Web-sized clips + posters + pet sprites for the site (docs/media). Re-run after a short or moment changes.
# Clips: 540x960 H.264, no end card on app moments (it says "Coming soon", the page says that itself).
set -e
cd "$(dirname "$0")/.."
M=docs/media; mkdir -p $M/clips $M/pets $M/shots
SH=~/Projects/sns-shorts/out; V=~/Videos; F=~/Projects/summer-phone/promo/frames; S=~/Projects/summer-phone/store
clip() { # name src trim_end_seconds
  local d; d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$2")
  local t; t=$(python3 -c "print(max(1,$d-$3))")
  ffmpeg -v error -y -i "$2" -t "$t" -vf scale=540:960 -c:v libx264 -crf 27 -preset slow -profile:v high -pix_fmt yuv420p \
    -c:a aac -b:a 96k -movflags +faststart "$M/clips/$1.mp4"
}
# cartoon shorts (Vachie OK'd; Rainy day held back, Game night not posted yet, Milk + Yapapa use others' songs)
clip notice-me   $SH/headbump/headbump.mp4 0
clip sunbeam     $SH/sunbeam/sunbeam.mp4 0
clip say-cheese  $SH/photobooth/photobooth.mp4 0
clip if-it-fits  $SH/box/box.mp4 0
# app moments (real footage)
for m in wx dress park game tap tile; do clip moment-$m $V/soot-and-summer-moment-$m.mp4 2.5; done
python3 tools/images.py
python3 tools/posters.py
du -sh $M
