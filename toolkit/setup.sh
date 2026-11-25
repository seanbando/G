#!/usr/bin/env bash
# Cashley tools setup for macOS and Linux. Run from this folder: bash setup.sh
set -e
echo "== Checking requirements"
command -v python3 >/dev/null || { echo "Install Python 3.10+ first: https://www.python.org/downloads/"; exit 1; }
command -v node >/dev/null || { echo "Install Node.js 22+ first: https://nodejs.org/"; exit 1; }
command -v ffmpeg >/dev/null || { echo "Install FFmpeg first (macOS: brew install ffmpeg)"; exit 1; }
node -e 'process.exit(parseInt(process.versions.node) >= 22 ? 0 : 1)' || { echo "Node.js 22 or newer is needed for HyperFrames"; exit 1; }

echo "== Python packages (Whisper narration check, ElevenLabs voices)"
python3 -m pip install --upgrade -r requirements.txt

echo "== Whisper model (downloads about 250 MB once)"
python3 -c "from faster_whisper import WhisperModel; WhisperModel('small.en', device='cpu', compute_type='int8'); print('Whisper ready')"

echo "== Node packages (frame check, character sheets)"
npm install
npx playwright install chromium

echo "== HyperFrames (renders scenes to video; usage tracking off)"
export DO_NOT_TRACK=1 HYPERFRAMES_NO_TELEMETRY=1
npx --yes hyperframes@0.9.92 --version

echo
echo "All set. See SETUP.md for how to use each tool."
