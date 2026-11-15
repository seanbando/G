# Transcribe a video's speech to an .srt next to the output folder, using ffmpeg's whisper filter (whisper.cpp).
#   powershell -File saylo/tools/transcribe.ps1 <video> <out.srt> [model]
# Model default: <repo>/_kit/whisper/ggml-base.en.bin (not in git; https://huggingface.co/ggerganov/whisper.cpp).
param([Parameter(Mandatory)][string]$Video, [Parameter(Mandatory)][string]$Out, [string]$Model)
if (-not $Model) { $Model = Join-Path $PSScriptRoot "..\..\_kit\whisper\ggml-base.en.bin" }
$Model = (Resolve-Path $Model).Path -replace '\\', '/' -replace ':', '\:'
$Dest = [IO.Path]::GetFullPath($Out) -replace '\\', '/' -replace ':', '\:'
ffmpeg -hide_banner -loglevel error -y -i $Video -vn -af "aresample=16000,whisper=model='$Model':language=en:queue=10:destination='$Dest':format=srt" -f null -
