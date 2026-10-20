---
name: lecture-slides
description: 확률과 통계 강의자료(PPTX)를 양식 references/1.pptx로 만든다. 개념마다 [비유] 사진 슬라이드(Openverse CC 이미지) + manim 애니메이션 슬라이드, 명사형 종결 말투. "N강 만들어줘", "강의자료 만들어", "슬라이드 만들어", 기존 강의 수정 요청에 사용.
---

# 강의 슬라이드 제작

`CLAUDE.md`(강의 정보·작성 원칙·피드백 기록)를 먼저 읽고 그대로 따른다. 이 스킬은 **제작 절차와 도구**를 담당한다.

경로 표기: `SK` = `.claude/skills/lecture-slides`, `LEC` = `lectures/NN-주제`. 모든 명령은 프로젝트 루트(`slides/`)에서 실행한다. 임시 파일은 scratchpad에 둔다.

## 결과물 구조

```
LEC/outline.md                학습 목표·내용 순서 (없으면 교과서로 초안 작성 후 사용자 확인)
LEC/assets/*.png              정적 그림 (scripts/NN_figures.py, matplotlib)
LEC/assets/anim/*.mp4         manim 영상 + *_poster.png (scripts/NN_animations.py)
LEC/assets/photos/*.jpg       비유 사진 + credits.json
LEC/output/NN-주제.pptx       완성본
scripts/NN_figures.py · NN_animations.py · NN_build.py
```
1강(`scripts/01_*.py`, `lectures/01-introduction/`)이 완성된 참고 예시다. 새 강의는 이 파일들을 복사해서 내용만 바꾼다.

## 절차

### 1. 내용 파악
- 교과서 PDF(`references/`)에서 해당 단원 쪽을 찾는다. PDF 텍스트 추출은 수식이 깨지므로 **페이지를 이미지로 렌더링해서 읽는다** (`fitz` → `page.get_pixmap(dpi=80)` → Read).
- `LEC/outline.md`를 채운다: 학습 목표 2개, 소단원(N-1, N-2 …), 각 개념의 비유, 애니메이션 아이디어, 확인 문제.
- 용어·기호·예제는 교과서를 따른다. 교과서에 없는 공학 예제를 추가했다면 완료 보고에서 밝힌다.

### 2. 슬라이드 흐름
표지 → 목차 → 학습 목표 → [개념마다: **비유 슬라이드 → 애니메이션 슬라이드**, 필요하면 성질 정리 슬라이드] → 정리 → 확인 문제(정답은 노트) → 이미지 출처

- 말투: 모든 문장 명사형 종결 ("확률의 합 = 1", "셀 수 있는 값"). "~입니다/~한다" 금지.
- 비유는 "A = B" 형태로 대응을 명확히: 사진 속 사물 ↔ 수학 개념, 그리고 비유가 성질까지 설명하도록 (예: 피자 조각 크기는 음수 불가 → 0 ≤ 확률).

### 3. 비유 사진 (Openverse, CC 라이선스만)
```
python SK/tools/openverse.py search "<영어 검색어>" <scratchpad>/cand.png 10
```
→ `cand.png`를 Read로 보고 고른다 (사진이 개념을 바로 떠올리게 하는지, 사람 얼굴·상표가 주인공이 아닌지).
```
python SK/tools/openverse.py fetch <id> <저장이름> LEC/assets/photos 4:3
```
- 자동으로 CC0·PDM·CC BY·CC BY-SA만 검색되고, 출처는 `credits.json`에 기록된다. 다른 사이트 이미지를 임의로 쓰지 않는다.
- 두 장을 나란히 비교할 때는 같은 비율(4:3)로 자른다.

### 4. manim 애니메이션
`scripts/NN_animations.py` 맨 위:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".claude/skills/lecture-slides/lib"))
from manim_style import *     # 1600×800, 흰 배경, RED_/RED_L/GRAY_/GRAY_L/INK, T(), axes(), x_labels()
```
- 영상 하나 = 개념 하나, 10~18초. 마지막 프레임에 결론 문장이 남게 한다 (슬라이드에서는 마지막 프레임이 멈춘 채 보임).
- 움직임이 의미를 가져야 한다: 값이 변하며 확률이 갱신(ValueTracker + always_redraw), 히스토그램 → 곡선, 막대 쌓아 합 = 1 등.
- **LaTeX 없음**: `MathTex`, `Tex`, `DecimalNumber`, `Axes(include_numbers=True)` 사용 금지. 수식도 `T("P(a ≤ X ≤ b)")`, 숫자 변화는 `always_redraw(lambda: T(f"{v:.2f}"))`. 줄바꿈 `\n`은 Edit 도구로 작성 (bash heredoc은 실제 줄바꿈으로 바꿔 버림).
- `axes()`의 y축은 x=0 위치에 그려지므로 막대는 x=0.6부터 배치하고 `x_labels(ax, [0.6, 1.6, …], texts=[…])`.

렌더 (모든 Scene, 실패 시 로그 출력):
```
python SK/tools/render_animations.py scripts/NN_animations.py LEC/assets/anim <scratchpad>/media
```
→ `LEC/assets/anim/_posters.png`를 Read로 보고 글자 겹침·화면 밖 잘림을 고친 뒤 해당 Scene만 다시 렌더 (`... <media> SceneName`).

### 5. 정적 그림
정리 비교표, 확인 문제 그림, 표지·학습 목표 그림은 matplotlib(`scripts/NN_figures.py`, 1강 파일 참고). 색·글꼴은 manim과 동일.

### 6. 슬라이드 조립
`scripts/NN_build.py`에서 `SK/lib/deck.py`의 `Deck` 사용 (1강 `01_build.py` 참고):

| 메서드 | 용도 |
|---|---|
| `cover(번호, 과목, 제목, 강사, 그림)` | 표지 |
| `contents(머리글, [항목…])` | 목차 (4~5개) |
| `goals(그림, 목표1, 목표2)` | 학습 목표 |
| `analogy(번호, 제목, 비유이름, [(사진, 폭)], [줄…])` | 비유 슬라이드, 사진 출처 자동 표기 |
| `video_page(번호, 제목, 소제목, Scene, lead=[정의 1~2줄])` | 애니메이션 슬라이드 |
| `page(번호, 제목, 소제목)` + `text()`·`pic()`·`photo()`·`video()` | 자유 배치 |
| `credits_page()` / `save(경로)` | 이미지 출처 / 저장 |

`text()` 항목: `"문장"`(· bullet), `("h", "소제목")`(빨간 굵게), `("m", "①  수식")`(들여쓰기). 본문 영역은 x 1.0~12.6, y 1.65~7.2(inch).
아래첨자는 ₁₂ₙ만 (ᵢ는 맑은 고딕에서 깨짐).

```
python scripts/NN_build.py
powershell -NoProfile -ExecutionPolicy Bypass -File SK/tools/autoplay.ps1 "<LEC/output/NN-주제.pptx 절대경로>"
```
autoplay는 영상을 "슬라이드 열리면 자동 재생, 끝나면 마지막 프레임 유지"로 설정한다. build 후 매번 다시 실행.

### 7. 검수 (생략 금지)
```
python SK/tools/preview.py "<pptx 절대경로>" <scratchpad>/preview
```
→ `sheet_*.png`를 모두 Read로 확인: 글자 겹침, 어색한 줄바꿈, 화면 밖 잘림, 명사형 종결, 빈 슬라이드. 고친 뒤 build → autoplay → preview 반복.

### 8. 완료 보고
- 파일 경로, 슬라이드 수, 구성 표(개념 / 비유 / 애니메이션)
- 교과서에 없는 예제, 확인하지 못한 것(예: 슬라이드쇼 실제 재생)을 밝힌다
- 사용자 피드백은 `CLAUDE.md`의 "피드백 기록"에 규칙으로 추가한다

## 환경 메모 (이 PC)
- Python 3.10, python-pptx, manim 0.19(PyAV 내장, ffmpeg 불필요), matplotlib, PyMuPDF(fitz)
- PowerPoint 설치됨 → COM으로 렌더링·자동 재생 설정
- 스크립트 파일 이름을 표준 모듈과 겹치게 짓지 않는다 (예: `inspect.py`는 python-pptx import를 깨뜨림)
