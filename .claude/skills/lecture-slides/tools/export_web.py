"""웹 버전(GitHub Pages)에 쓸 강의 자산 복사

사용법: python export_web.py <LEC 폴더> <docs/NN 폴더>
  LEC/assets/*.png, photos/*.jpg(+credits.json), flow/*, anim/*.mp4·*_poster.png → docs/NN/assets/
"""
import shutil
import sys
from pathlib import Path

src = Path(sys.argv[1]) / "assets"
dst = Path(sys.argv[2]) / "assets"
patterns = ["*.png", "photos/*.jpg", "photos/credits.json", "flow/*.jpg", "flow/*.mp4", "flow/*.png",
            "anim/*.mp4", "anim/*_poster.png"]
n = 0
for pat in patterns:
    for f in src.glob(pat):
        out = dst / f.relative_to(src)
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, out)
        n += 1
print(f"copied {n} files → {dst}")
