"""1강 확률변수와 확률분포 — 슬라이드 조립 (lecture-slides 스킬의 Deck 사용)

사용법: python scripts/01_build.py [출력 경로]
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".claude/skills/lecture-slides/lib"))
from deck import Deck

LEC = ROOT / "lectures/01-introduction"
d = Deck(ROOT / "references/1.pptx", LEC / "assets")

FLOW = LEC / "assets/flow"   # Google Flow로 생성한 AI 이미지·영상

d.cover("01", "확률과 통계", "확률변수와 확률분포", "강사 : ○○○", "flow/cover.jpg")
d.intro_video(FLOW / "intro.mp4", FLOW / "intro_poster.png", position=1)   # 표지 바로 다음
d.contents("확률변수와 확률분포", ["확률변수란?", "이산확률변수와 확률분포", "연속확률변수와 확률밀도함수", "정리 및 확인 문제"])
d.goals("flow/goals.jpg", "확률변수와 확률분포의 뜻 이해", "이산·연속확률변수의 구분과 확률분포의 성질 활용")

# ── 1-1 확률변수 ────────────────────────────────────
d.analogy("1-1", "확률변수란?", "바코드 스캐너", [("barcode", 3.3)], [
    ("h", "바코드 스캐너 = 확률변수"),
    "물건 → 숫자(가격)로 바꾸는 장치",
    "실험 결과 → 실수로 바꾸는 규칙",
    "동전 2번 던지기: (H, T) → 앞면 횟수 1",
    "결과는 글자·그림이어도 확률변수의 값은 항상 실수",
])
d.video_page("1-1", "확률변수란?", "확률변수(random variable): 각 근원사건 → 실수 하나", "RandomVariable")

d.analogy("1-1", "확률변수란?", "계단과 미끄럼틀", [("stairs", 3.6), ("slide", 3.6)], [
    ("h", "계단 = 이산"),
    "정해진 칸에만 서기",
    "0, 1, 2, 3 … 셀 수 있는 값",
    ("h", "미끄럼틀 = 연속"),
    "어느 높이에서나 멈추기",
    "범위 안의 모든 실수",
])
d.video_page("1-1", "확률변수란?", "확률변수의 두 종류: 셀 수 있는 값 vs 범위 안의 모든 실수", "DiscreteContinuous")

# ── 1-2 이산확률변수 ────────────────────────────────
d.analogy("1-2", "이산확률변수와 확률분포", "피자 한 판 나누기", [("pizza", 5.2)], [
    ("h", "피자 한 판 = 전체 확률 1"),
    "조각 하나 = X의 값 하나",
    "조각 크기 = 그 값의 확률",
    "조각 크기는 음수 불가 → 0 ≤ 확률 ≤ 1",
    "조각을 모두 모으면 한 판 → 확률의 합 = 1",
])
d.video_page("1-2", "이산확률변수와 확률분포", "이산확률변수(discrete random variable)", "PmfCoin", lead=[
    "이산확률변수: 취하는 값이 유한개이거나 자연수처럼 셀 수 있는 확률변수",
    "확률질량함수(probability mass function): P(X = x₁) = p₁, …, P(X = xₙ) = pₙ",
])

s = d.page("1-2", "이산확률변수와 확률분포", "이산확률변수의 확률분포의 성질")
d.text(s, 1.2, 1.7, 6.8, 5.4, [
    ("h", "성질"),
    ("m", "①  0 ≤ p₁, p₂, …, pₙ ≤ 1"),
    ("m", "②  p₁ + p₂ + … + pₙ = 1"),
    ("h", "예: 부품 품질 검사"),
    "생산된 부품 10개 중 불량품 2개",
    "임의로 3개를 뽑아 검사할 때 불량품 수 X",
    "X가 취하는 값: 0, 1, 2",
    "각 확률과 합 = 1 확인",
])
d.photo(s, "factory", 8.6, 1.75, height=4.9)
d.video_page("1-2", "이산확률변수와 확률분포", "예: 불량품 수 X의 확률분포", "PmfDefect")

# ── 1-3 연속확률변수 ────────────────────────────────
d.analogy("1-3", "연속확률변수와 확률밀도함수", "지하철 기다리기", [("subway", 5.4)], [
    ("h", "10분 간격 지하철"),
    "아무 때나 역에 도착",
    "대기 시간 X: 0분 ~ 10분",
    "3분, 3.5분, 3.27분 … 어떤 실수든 가능",
    "셀 수 없는 값 → 연속확률변수",
])
d.video_page("1-3", "연속확률변수와 확률밀도함수", "연속확률변수(continuous random variable)", "UniformSubway", lead=[
    "연속확률변수: 취하는 값이 어떤 범위에 속하는 모든 실수인 확률변수",
    "확률 P(a ≤ X ≤ b) = 그래프 아래 넓이",
])

d.analogy("1-3", "연속확률변수와 확률밀도함수", "모래 더미", [("sand", 5.4)], [
    ("h", "모래 더미 = 확률밀도함수의 그래프"),
    "전체 모래 양 = 1",
    "a ~ b 구간 위의 모래 양 = P(a ≤ X ≤ b)",
    "바늘 끝 한 점 위의 모래 양 = 0",
    "→ 한 점의 확률 P(X = a) = 0",
])
d.video_page("1-3", "연속확률변수와 확률밀도함수", "확률밀도함수(probability density function)", "DensityCurve")

s = d.page("1-3", "연속확률변수와 확률밀도함수", "확률밀도함수의 성질")
d.text(s, 1.2, 1.7, 5.6, 5.4, [
    ("h", "α ≤ X ≤ β에서 정의된 y = f(x)"),
    ("m", "①  f(x) ≥ 0"),
    ("m", "②  그래프 아래 전체 넓이 = 1"),
    ("m", "③  P(a ≤ X ≤ b) = a~b 구간의 넓이"),
    ("h", "주의"),
    "한 점에서의 확률은 0: P(X = b) = 0",
    "P(a ≤ X ≤ b) = P(a < X < b)",
], size=18)
d.pic(s, LEC / "assets/pdf_area.png", 6.9, 2.2, width=6.0)

# ── 1-4 정리 ────────────────────────────────────────
s = d.page("1-4", "정리 및 확인 문제", "이산확률변수 vs 연속확률변수")
d.pic(s, LEC / "assets/summary_compare.png", 1.1, 1.8, width=11.1)

s = d.page("1-4", "정리 및 확인 문제", "확인 문제")
d.pic(s, FLOW / "quiz.jpg", 1.6, 4.4, width=2.6)
d.text(s, 1.2, 1.7, 6.9, 2.7, [
    ("h", "문제 1"),
    "100원짜리 동전 3개를 동시에 던질 때, 앞면이 나오는 개수 X가 취하는 모든 값",
    ("h", "문제 2"),
    "X의 범위 0 ≤ X ≤ 4, 확률밀도함수 f(x) = kx",
    "상수 k의 값과 P(0 ≤ X ≤ 2)",
], size=18)
d.pic(s, LEC / "assets/quiz_triangle.png", 8.2, 2.2, width=4.4)
s.notes_slide.notes_text_frame.text = (
    "[정답] 문제 1: 0, 1, 2, 3\n"
    "문제 2: 전체 넓이 ½·4·4k = 8k = 1 → k = 1/8,  P(0 ≤ X ≤ 2) = ½·2·(2/8) = 1/4"
)

s = d.page("1-4", "정리 및 확인 문제", "마무리")
d.pic(s, FLOW / "closing.jpg", 3.4, 1.75, width=9.3)
d.text(s, 1.1, 1.9, 5.0, 5.0, [
    ("h", "오늘 배운 것"),
    "확률변수 = 결과 → 실수",
    "이산: 확률질량함수, 막대 높이",
    "연속: 확률밀도함수, 그래프 아래 넓이",
    ("h", "다음 시간"),
    "이산확률변수의 기댓값과 표준편차",
], size=18)

d.credits_page(extra=["AI 생성 이미지·영상 (표지, 인트로 영상, 학습 목표, 확인 문제, 마무리) — Google Flow (Nano Banana 2.1, Omni 1.1 Flash)"])
d.save(sys.argv[1] if len(sys.argv) > 1 else LEC / "output/01-introduction.pptx")
