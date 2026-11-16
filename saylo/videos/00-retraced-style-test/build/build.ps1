# Retraced style test: render every shot of S_cold_open.py through the Documentary Pro runner (one at a time),
# then assemble with assemble_test.py.
#   powershell -File saylo/videos/00-retraced-style-test/build/build.ps1            # all shots + assemble
#   powershell -File saylo/videos/00-retraced-style-test/build/build.ps1 -Stills    # one mid still per shot
#   powershell -File saylo/videos/00-retraced-style-test/build/build.ps1 -Only 3,11 # just these shots
param([switch]$Stills, [string]$Only = "")
$pick = @($Only -split '[,\s]+' | Where-Object { $_ } | ForEach-Object { [int]$_ })
$env:Path = [Environment]::GetEnvironmentVariable('Path','User') + ';' + [Environment]::GetEnvironmentVariable('Path','Machine')
$build = $PSScriptRoot
$vid = Split-Path $build
$repo = Split-Path (Split-Path (Split-Path $vid))
$studio = Join-Path $repo "_kit\docpro\Faceless Studio"
$runner = Join-Path $studio ".claude\skills\documentary-pro\scripts\render_blender.py"
$cfg = Get-Content (Join-Path $build "shots.json") -Raw | ConvertFrom-Json
$out = Join-Path $vid "render\shots"
New-Item -ItemType Directory -Force $out | Out-Null
Push-Location $studio
foreach ($s in $cfg.shots) {
    if ($pick.Count -and ($pick -notcontains [int]$s.id)) { continue }
    $n = [int][math]::Round(($s.end - $s.start) * $cfg.fps)
    $name = "S{0:D2}" -f $s.id
    # the runner reuses %TEMP%\faceless-studio-shot-* frames for the same output name: clear them (PROGRESS gotcha)
    Get-ChildItem $env:TEMP -Directory -Filter "faceless-studio-shot-*" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    # shot 11 has its own hero set (S11_hero.py); every other shot comes from the shared world
    $script = if ([int]$s.id -eq 11) { "S11_hero.py" } else { "S_cold_open.py" }
    $a = @($runner, (Join-Path $build $script), "--out", (Join-Path $out "$name.mp4"), "--frames", $n, "--arg", "shot=$($s.id)")
    if ($Stills) { $a += @("--stills", [string][int]($n * 0.7)) }
    Write-Host "== $name ($n frames)"
    python @a
}
Pop-Location
if (-not $Stills -and -not $pick.Count) { python (Join-Path $build "assemble_test.py") }
