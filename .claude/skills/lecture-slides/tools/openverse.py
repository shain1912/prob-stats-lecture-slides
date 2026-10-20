"""비유 사진 검색·저장 (Openverse API, CC0·PDM·CC BY·CC BY-SA만)

검색 + 후보 썸네일 한 장으로 모아 보기:
    python openverse.py search "staircase" <sheet.png> [개수]
선택한 사진 저장 (자르기·축소 + credits.json 갱신):
    python openverse.py fetch <id> <저장이름> <assets/photos> [4:3]
"""
import io
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

API = "https://api.openverse.org/v1/images/"
UA = {"User-Agent": "Mozilla/5.0 (lecture-slides)"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def search(query, sheet, n=10):
    q = urllib.parse.urlencode({"q": query, "license": "cc0,pdm,by,by-sa", "page_size": n, "mature": "false"})
    results = json.loads(get(f"{API}?{q}"))["results"]
    W, H, cols = 300, 220, 5
    rows = (len(results) + cols - 1) // cols
    img = Image.new("RGB", (W * cols, (H + 36) * max(rows, 1)), "white")
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("malgun.ttf", 13)
    except OSError:
        font = None
    for k, r in enumerate(results):
        x, y = (k % cols) * W, (k // cols) * (H + 36)
        try:
            th = Image.open(io.BytesIO(get(r["thumbnail"]))).convert("RGB")
            th.thumbnail((W - 6, H - 6))
            img.paste(th, (x + 3, y + 3))
        except Exception:
            d.text((x + 10, y + 100), "(썸네일 실패)", fill="red", font=font)
        d.text((x + 4, y + H), f"#{k} {r['license']} {r.get('width')}x{r.get('height')}", fill="black", font=font)
        d.text((x + 4, y + H + 16), (r.get("title") or "")[:38], fill="gray", font=font)
        print(f"#{k} {r['id']} {r['license']} {r.get('width')}x{r.get('height')} | {r.get('creator')} | {(r.get('title') or '')[:60]}")
    img.save(sheet)
    print("sheet:", sheet)


def fetch(image_id, name, photos_dir, ratio=None):
    photos = Path(photos_dir)
    photos.mkdir(parents=True, exist_ok=True)
    meta = json.loads(get(f"{API}{image_id}/"))
    im = Image.open(io.BytesIO(get(meta["url"]))).convert("RGB")
    if ratio:
        a, b = map(float, ratio.split(":"))
        r, (w, h) = a / b, im.size
        if w / h > r:
            nw = int(h * r); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else:
            nh = int(w / r); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im.thumbnail((1600, 1600))
    im.save(photos / f"{name}.jpg", quality=88)
    cred_path = photos / "credits.json"
    credits = json.loads(cred_path.read_text(encoding="utf-8")) if cred_path.exists() else {}
    credits[name] = {k: meta.get(k) for k in ("title", "creator", "license", "license_version", "license_url")}
    credits[name]["source"] = meta.get("foreign_landing_url")
    credits[name]["provider"] = meta.get("source")
    cred_path.write_text(json.dumps(credits, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"saved {name}.jpg {im.size} — {meta.get('creator')}, {meta['license']} {meta.get('license_version')}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "search":
        search(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 10)
    elif cmd == "fetch":
        fetch(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else None)
