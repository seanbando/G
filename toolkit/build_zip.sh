#!/usr/bin/env bash
# Rebuilds cashley_tools.zip from this repo. Usage: bash toolkit/build_zip.sh <out-dir>
set -e
OUT=${1:-.}; B=$(mktemp -d)/cashley_tools
mkdir -p $B/tools $B/kit $B/docs $B/templates/hyperframes-scene/assets
cp tools/qa_narration.py tools/frame_check.js tools/build_track.py tools/generate_voiceovers.py tools/make_voiceover.py tools/make_voiceover_v2.py tools/check_script.py $B/tools/
cp -r kit/characters kit/props $B/kit/
cp docs/script-system.md docs/script-format-guide.md docs/video-variety-log.md docs/ai-detection-notes.md $B/docs/
cp experiments/hyperframes-test/index.html experiments/hyperframes-test/package.json experiments/hyperframes-test/hyperframes.json $B/templates/hyperframes-scene/
cp experiments/hyperframes-test/assets/gsap.min.js $B/templates/hyperframes-scene/assets/
cp requirements.txt toolkit/setup.sh toolkit/setup.ps1 toolkit/SETUP.md toolkit/package.json $B/
(cd $(dirname $B) && zip -qr cashley_tools.zip cashley_tools) && mv $(dirname $B)/cashley_tools.zip $OUT/
echo "wrote $OUT/cashley_tools.zip"
