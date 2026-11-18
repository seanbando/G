# Render one Blender hero through the Documentary Pro runner (one at a time; stills first).
#   powershell -File build/blender/render.ps1 <script.py> <name> <frames> [stills] [--arg k=v ...]
#   stills e.g. "1,60,120"; omit or "-" to render the clip, which is then copied to media/blender <name>.mp4
param([string]$Script, [string]$Name, [int]$Frames, [string]$Stills = "-", [Parameter(ValueFromRemainingArguments)]$Rest)
$vid = Split-Path (Split-Path $PSScriptRoot)
$repo = Split-Path (Split-Path (Split-Path $vid))
$studio = Join-Path $repo "_kit\docpro\Faceless Studio"
$runner = Join-Path $studio ".claude\skills\documentary-pro\scripts\render_blender.py"
$out = Join-Path $vid "render\blender\$Name.mp4"
New-Item -ItemType Directory -Force (Split-Path $out) | Out-Null
$a = @($runner, (Join-Path $PSScriptRoot $Script), "--out", $out, "--frames", $Frames)
if ($Stills -ne "-") { $a += @("--stills", $Stills) }
Push-Location $studio
python @a @Rest
Pop-Location
if ($Stills -eq "-" -and (Test-Path $out)) { Copy-Item $out (Join-Path $vid "media\blender $Name.mp4") -Force }
