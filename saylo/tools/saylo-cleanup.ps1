# Saylo cleanup for Windows
# What it does:
#   1. Finds the big Olympic Bomber leftovers in Downloads\Olympic Bomber
#      (full-length source videos + AI stock clips), shows them with sizes,
#      and moves them to the Recycle Bin ONLY if you type YES.
#      Keeps: numbered clips ("05 save a lot clip.mp4"...), voiceover, photos.
#   2. Lists the 25 biggest files on your user folder (over 500 MB) so you can decide.
#   3. Opens the Downloads folder and Windows Storage settings.
# Nothing is permanently deleted. Empty the Recycle Bin yourself when happy.
#
# Run: right-click this file -> "Run with PowerShell"
#  or: powershell -ExecutionPolicy Bypass -File .\saylo-cleanup.ps1

Add-Type -AssemblyName Microsoft.VisualBasic

function Size($b) { if ($b -ge 1GB) { "{0:N1} GB" -f ($b/1GB) } else { "{0:N0} MB" -f ($b/1MB) } }

$folder = Join-Path $env:USERPROFILE 'Downloads\Olympic Bomber'
$patterns = @(
  '*_1080p*.mp4',                 # AI stock clips (Fog_rolling..._1080p.mp4)
  '*Forgotten History*',          # full-length source videos
  '*RETRO REPORT*',
  '*Richard Jewell Movie*',
  '*WYFF News 4*',
  '*AP Archive*',
  '*CENTENNIAL OLYMPIC PARK BOMBING - CNN*'
)

Write-Host "`n=== Step 1: Olympic Bomber leftovers ===" -ForegroundColor Cyan
if (Test-Path $folder) {
  $files = foreach ($p in $patterns) { Get-ChildItem -Path $folder -Filter $p -File -ErrorAction SilentlyContinue }
  $files = $files | Sort-Object FullName -Unique
  if ($files) {
    $files | ForEach-Object { "{0,10}  {1}" -f (Size $_.Length), $_.Name }
    $total = ($files | Measure-Object Length -Sum).Sum
    Write-Host ("`n{0} files, {1} total" -f $files.Count, (Size $total)) -ForegroundColor Yellow
    $answer = Read-Host "Type YES to move these to the Recycle Bin"
    if ($answer -eq 'YES') {
      foreach ($f in $files) {
        [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile($f.FullName, 'OnlyErrorDialogs', 'SendToRecycleBin')
      }
      Write-Host "Moved to the Recycle Bin." -ForegroundColor Green
    } else { Write-Host "Skipped. Nothing moved." }
  } else { Write-Host "None of the big leftovers are here (already cleaned)." -ForegroundColor Green }
} else {
  Write-Host "Folder not found: $folder" -ForegroundColor Yellow
  Write-Host "If your clips are somewhere else, open that folder and delete the same files by hand."
}

Write-Host "`n=== Step 2: biggest files in your user folder (over 500 MB) ===" -ForegroundColor Cyan
Write-Host "Scanning, this can take a minute..."
Get-ChildItem -Path $env:USERPROFILE -Recurse -File -ErrorAction SilentlyContinue |
  Where-Object { $_.Length -gt 500MB } |
  Sort-Object Length -Descending |
  Select-Object -First 25 |
  ForEach-Object { "{0,10}  {1}" -f (Size $_.Length), $_.FullName }
Write-Host "Delete any of these you don't need (old exports, raw downloads, installers)."

Write-Host "`n=== Step 3: opening Downloads and Storage settings ===" -ForegroundColor Cyan
Start-Process explorer.exe (Join-Path $env:USERPROFILE 'Downloads')
Start-Process "ms-settings:storagesense"
Write-Host "In Storage: Temporary files -> tick Temporary files + Recycle Bin -> Remove files. Turn on Storage Sense."
Write-Host "`nDone. Empty the Recycle Bin when you're sure." -ForegroundColor Green
Read-Host "Press Enter to close"
