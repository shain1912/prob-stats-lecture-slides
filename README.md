# 확률과 통계 강의자료

대학교 1학년 공대생 대상 「확률과 통계」 강의 슬라이드(PPTX) 제작 프로젝트.
개념마다 [비유] 사진 슬라이드 + manim 애니메이션 슬라이드로 구성.

## 구조
- `CLAUDE.md` — 강의 정보·작성 원칙 (명사형 종결, 그림 위주)
- `.claude/skills/lecture-slides/` — 제작 스킬 (슬라이드 조립 라이브러리, manim 스타일, Openverse 사진 검색, 렌더·검수 도구)
- `scripts/NN_*.py` — 강의별 그림·애니메이션·조립 스크립트
- `lectures/NN-주제/` — 강의별 outline, assets(그림·사진), output(완성본, 저장소 제외)

## 저장소에 없는 파일
- `references/1.pptx`(양식), `references/*.pdf`(교과서): 저작권 자료라 제외 — 직접 넣어야 빌드 가능
- `assets/anim/*.mp4`, `output/*.pptx`: 스크립트로 재생성

## 빌드 (1강)
```
python .claude/skills/lecture-slides/tools/render_animations.py scripts/01_animations.py lectures/01-introduction/assets/anim <임시폴더>
python scripts/01_build.py
powershell -File .claude/skills/lecture-slides/tools/autoplay.ps1 <pptx 절대경로>
```
필요: Python 3.10+, python-pptx, manim, matplotlib, PyMuPDF, Pillow, PowerPoint(Windows)

비유 사진 출처는 `lectures/*/assets/photos/credits.json` 참고 (CC0 / CC BY / CC BY-SA).
