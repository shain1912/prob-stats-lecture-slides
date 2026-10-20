# 슬라이드에 들어간 모든 영상을 "슬라이드가 열리면 자동 재생, 끝나면 마지막 프레임 유지"로 설정 (PowerPoint COM)
# 사용법: powershell -NoProfile -ExecutionPolicy Bypass -File autoplay.ps1 <pptx 절대경로>
param([string]$Path)
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open($Path, $false, $false, $false)
$n = 0
foreach ($slide in $pres.Slides) {
  foreach ($shape in $slide.Shapes) {
    if ($shape.Type -eq 16) {   # msoMedia
      $ps = $shape.AnimationSettings.PlaySettings
      $ps.PlayOnEntry = -1
      $ps.HideWhileNotPlaying = 0
      $ps.RewindMovie = 0
      $n++
    }
  }
}
$pres.Save()
$pres.Close()
$ppt.Quit()
"autoplay set on $n videos"
