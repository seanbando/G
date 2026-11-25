# Cashley tools setup for Windows. Run in PowerShell from this folder:
#   powershell -ExecutionPolicy Bypass -File setup.ps1
$ErrorActionPreference = "Stop"
Write-Host "== Checking requirements"
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw "Install Python 3.10+ first: https://www.python.org/downloads/ (tick 'Add to PATH')" }
if (-not (Get-Command node -ErrorAction SilentlyContinue)) { throw "Install Node.js 22+ first: https://nodejs.org/" }
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { throw "Install FFmpeg first: winget install Gyan.FFmpeg (then reopen PowerShell)" }
$nodeMajor = [int](node -e "console.log(process.versions.node.split('.')[0])")
if ($nodeMajor -lt 22) { throw "Node.js 22 or newer is needed for HyperFrames" }

Write-Host "== Python packages (Whisper narration check, ElevenLabs voices)"
python -m pip install --upgrade -r requirements.txt

Write-Host "== Whisper model (downloads about 250 MB once)"
python -c "from faster_whisper import WhisperModel; WhisperModel('small.en', device='cpu', compute_type='int8'); print('Whisper ready')"

Write-Host "== Node packages (frame check, character sheets)"
npm install
npx playwright install chromium

Write-Host "== HyperFrames (renders scenes to video; usage tracking off)"
$env:DO_NOT_TRACK = "1"; $env:HYPERFRAMES_NO_TELEMETRY = "1"
npx --yes hyperframes@0.9.92 --version

Write-Host ""
Write-Host "All set. See SETUP.md for how to use each tool."
