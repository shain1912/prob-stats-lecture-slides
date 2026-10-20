"""완성된 PPTX를 PowerPoint로 렌더링해서 슬라이드 6장씩 모은 확인용 이미지 생성

    python preview.py <pptx 절대경로> <출력 폴더>
결과: <출력 폴더>/s1.png …, sheet_1.png, sheet_2.png … (Read로 열어 겹침·잘림 확인)
"""
import subprocess
import sys
from pathlib import Path
from PIL import Image

pptx, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
ps = f"""
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open('{pptx}', $true, $false, $false)
for ($i=1; $i -le $pres.Slides.Count; $i++) {{ $pres.Slides.Item($i).Export('{out}\\s' + $i + '.png', 'PNG', 1280, 720) }}
$pres.Slides.Count
$pres.Close(); $ppt.Quit()
"""
r = subprocess.run(["powershell.exe", "-NoProfile", "-Command", ps], capture_output=True, text=True)
n = int(r.stdout.strip().splitlines()[-1])
W, H = 640, 360
for page in range((n + 5) // 6):
    idx = range(page * 6 + 1, min(n, page * 6 + 6) + 1)
    sheet = Image.new("RGB", (W * 2 + 10, (H + 10) * 3), "#888")
    for k, i in enumerate(idx):
        sheet.paste(Image.open(out / f"s{i}.png").convert("RGB").resize((W, H)), ((k % 2) * (W + 10), (k // 2) * (H + 10)))
    sheet.save(out / f"sheet_{page + 1}.png")
    print(f"sheet_{page + 1}.png: slides {idx.start}-{idx.stop - 1}")
