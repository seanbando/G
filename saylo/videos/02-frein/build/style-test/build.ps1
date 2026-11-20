# Frein cold-open style test (Retraced look): render every shot through the Documentary Pro runner, one at a time,
# then cut the real clips and assemble with assemble.py.
#   powershell -File saylo/videos/02-frein/build/style-test/build.ps1 -Plan shots2.json            # v2: everything + assemble
#   powershell -File saylo/videos/02-frein/build/style-test/build.ps1 -Plan shots2.json -Stills    # one still per 3D shot
#   powershell -File saylo/videos/02-frein/build/style-test/build.ps1 -Plan shots2.json -Only 3,11 # just these shots (no assemble)
# Without -Plan it builds the first (rejected) test from shots.json.
param([switch]$Stills, [string]$Only = "", [string]$Skip = "", [string]$Plan = "shots.json")
$pick = @($Only -split '[,\s]+' | Where-Object { $_ } | ForEach-Object { [int]$_ })
$skipIds = @($Skip -split '[,\s]+' | Where-Object { $_ } | ForEach-Object { [int]$_ })
$env:Path = [Environment]::GetEnvironmentVariable('Path','User') + ';' + [Environment]::GetEnvironmentVariable('Path','Machine')
$build = $PSScriptRoot
$vid = Split-Path (Split-Path $build)
$repo = Split-Path (Split-Path (Split-Path $vid))
$studio = Join-Path $repo "_kit\docpro\Faceless Studio"
$runner = Join-Path $studio ".claude\skills\documentary-pro\scripts\render_blender.py"
$cfg = Get-Content (Join-Path $build $Plan) -Raw -Encoding UTF8 | ConvertFrom-Json
$dir = if ($cfg.dir) { $cfg.dir } else { "shots" }
$out = Join-Path $vid "build\render\$dir"
$extra = if ($Plan -ne "shots.json") { @("--arg", "cfg=$Plan") } else { @() }
New-Item -ItemType Directory -Force $out | Out-Null
$script = @{ "3d" = "S_airfield.py"; "open" = "S_open.py"; "map" = "S_map.py"; "photo" = "S_photo.py" }
Push-Location $studio
foreach ($s in $cfg.shots) {
    if ($pick.Count -and ($pick -notcontains [int]$s.id)) { continue }
    if ($skipIds -contains [int]$s.id) { continue }
    $n = [int]([math]::Round($s.end * $cfg.fps) - [math]::Round($s.start * $cfg.fps))
    $name = "S{0:D2}" -f $s.id
    # the runner reuses %TEMP%\faceless-studio-shot-* frames for the same output name: clear them first
    Get-ChildItem $env:TEMP -Directory -Filter "faceless-studio-shot-*" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    if ($s.kind -eq "still" -or $s.kind -eq "image") { continue }              # freeze frames are cut in assemble.py
    if ($s.kind -eq "clip") {
        if ($s.nametag -and -not $Stills) {
            $a = @($runner, (Join-Path $build "O_tag.py"), "--out", (Join-Path $out "$name-tag.mov"), "--frames", $n, "--alpha",
                   "--arg", "name=$($s.nametag.name)", "--arg", "role=$($s.nametag.role)", "--arg", "at=$($s.nametag.at - $s.start)")
            Write-Host "== $name name tag ($n frames)"
            python @a
        }
        continue
    }
    $a = @($runner, (Join-Path $build $script[$s.kind]), "--out", (Join-Path $out "$name.mp4"), "--frames", $n, "--arg", "shot=$($s.id)") + $extra
    if ($Stills) { $a += @("--stills", [string][int]($n * 0.6)) }
    Write-Host "== $name ($n frames)"
    python @a
}
Pop-Location
if (-not $Stills -and -not $pick.Count -and -not $skipIds.Count) { python (Join-Path $build "assemble.py") $Plan }
