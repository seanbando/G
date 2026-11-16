# Build every finished chapter, then join them into one review file that plays from 0:00.
#   powershell -File saylo/videos/01-olympic-bomber/build/build_all.ps1
# Add a chapter: append "<name> <plan.py>" to $Chapters.
$ErrorActionPreference = "Stop"
$here = $PSScriptRoot
$render = Join-Path (Split-Path $here) "render"
$Chapters = @(
    @("part1", $null),
    @("wrong_man", "plan_wrong_man.py"),
    @("same_hands", "plan_same_hands.py"),
    @("birmingham", "plan_birmingham.py"),
    @("who_he_was", "plan_who_he_was.py"),
    @("hunt", "plan_hunt.py"),
    @("five_years", "plan_five_years.py"),
    @("stop", "plan_stop.py")
)
foreach ($c in $Chapters) {
    if ($c[1]) { python "$here\build_part1.py" $c[0] $c[1] } else { python "$here\build_part1.py" }
    if ($LASTEXITCODE) { throw "build failed: $($c[0])" }
}
$list = ($Chapters | ForEach-Object { "file '$render\$($_[0]).mp4'" }) -join "`n"
[IO.File]::WriteAllText("$render\full.list.txt", $list)
ffmpeg -v error -y -f concat -safe 0 -i "$render\full.list.txt" -c:v libx264 -crf 19 -preset medium -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 48000 "$render\olympic_bomber_full.mp4"
Write-Output "wrote $render\olympic_bomber_full.mp4"
