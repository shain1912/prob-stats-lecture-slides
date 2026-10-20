"""manim 애니메이션 파일의 Scene을 렌더링해서 assets/anim에 mp4 + _poster.png(마지막 프레임) 저장

    python render_animations.py <NN_animations.py> <assets/anim> <임시 media 폴더> [Scene ...]
Scene을 생략하면 파일 안의 모든 Scene 클래스를 렌더링. 확인용 마지막 프레임 모음은 <anim>/_posters.png.
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
import av
from PIL import Image

src, out, media = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
scenes = sys.argv[4:] or re.findall(r"^class (\w+)\(Scene\)", src.read_text(encoding="utf-8"), re.M)
out.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, PYTHONIOENCODING="utf-8")
posters = []
for sc in scenes:
    r = subprocess.run([sys.executable, "-m", "manim", "-qh", "--disable_caching", "--progress_bar", "none",
                        "--media_dir", str(media), "-o", f"{sc}.mp4", str(src), sc],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    if r.returncode != 0:
        print(f"{sc} FAIL\n" + (r.stdout + r.stderr)[-2500:])
        continue
    mp4 = next(media.rglob(f"videos/**/{sc}.mp4"))
    shutil.copy(mp4, out / f"{sc}.mp4")
    c = av.open(str(out / f"{sc}.mp4"))
    frame = None
    for frame in c.decode(video=0):
        pass
    dur = float(c.streams.video[0].duration * c.streams.video[0].time_base)
    c.close()
    frame.to_image().save(out / f"{sc}_poster.png")
    posters.append(out / f"{sc}_poster.png")
    print(f"{sc} ok {dur:.1f}s")

if posters:
    W, H = 800, 400
    sheet = Image.new("RGB", (W * 2 + 10, (H + 10) * ((len(posters) + 1) // 2)), "#888")
    for k, p in enumerate(posters):
        sheet.paste(Image.open(p).convert("RGB").resize((W, H)), ((k % 2) * (W + 10), (k // 2) * (H + 10)))
    sheet.save(out / "_posters.png")
    print("posters:", out / "_posters.png")
