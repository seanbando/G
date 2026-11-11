#!/usr/bin/env bash
# Stitch per-line voice-over clips into one tight preview track.
# Usage: tools/build_preview.sh <clips_dir> <output.mp3>
# - trims leading/trailing silence from every clip
# - caps pauses inside a clip at ~0.45 s
# - 0.12 s between pieces of one line (VO-13a, VO-13b), 0.3 s between lines
#   from the same voice, 0.4 s when the speaker changes
# Trimmed copies are written to <clips_dir>/trimmed/ for use in the video editor.
set -euo pipefail
dir=$1; out=$2
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
mkdir -p "$dir/trimmed"
trim="silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse,silenceremove=stop_periods=-1:stop_duration=0.45:stop_threshold=-45dB:stop_silence=0.4"
for g in 0.12 0.3 0.4; do
  ffmpeg -v error -y -f lavfi -i anullsrc=r=44100:cl=mono -t $g -c:a pcm_s16le "$tmp/gap_$g.wav"
done
prev=""; prev_line=""; : > "$tmp/list.txt"
for f in "$dir"/VO-*.mp3; do
  name=$(basename "$f" .mp3); voice=${name#*_}; line=${name:0:5}
  ffmpeg -v error -y -i "$f" -af "$trim" -ac 1 -ar 44100 -c:a pcm_s16le "$tmp/$name.wav"
  ffmpeg -v error -y -i "$tmp/$name.wav" -c:a libmp3lame -b:a 128k "$dir/trimmed/$name.mp3"
  if [ -n "$prev" ]; then
    gap=0.4
    [ "$voice" = "$prev" ] && gap=0.3
    [ "$line" = "$prev_line" ] && gap=0.12
    echo "file '$tmp/gap_$gap.wav'" >> "$tmp/list.txt"
  fi
  echo "file '$tmp/$name.wav'" >> "$tmp/list.txt"
  prev=$voice; prev_line=$line
done
ffmpeg -v error -y -f concat -safe 0 -i "$tmp/list.txt" -c:a libmp3lame -b:a 128k "$out"
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out")
python3 -c "d=$d; print(f'{\"$out\"}: {int(d//60)}m {d%60:.0f}s')"
