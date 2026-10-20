"""1강 확률변수와 확률분포 — 슬라이드용 그림 생성"""
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
RED, RED_L, GRAY, GRAY_L, INK = "#E22B2D", "#F6C4C5", "#8C8C8C", "#D9D9D9", "#3F3F3F"
plt.rcParams.update({"font.family": "Malgun Gothic", "axes.unicode_minus": False,
                     "mathtext.fontset": "cm", "font.size": 15, "text.color": INK,
                     "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
                     "axes.edgecolor": INK})


def clean(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# 표지 그림: 히스토그램 + 정규곡선
rng = np.random.default_rng(3)
data = rng.normal(0, 1, 4000)
fig, ax = plt.subplots(figsize=(5.2, 5.6))
ax.hist(data, bins=np.linspace(-3.5, 3.5, 22), density=True, color=GRAY_L, edgecolor="white")
x = np.linspace(-3.6, 3.6, 300)
y = np.exp(-x**2 / 2) / np.sqrt(2 * np.pi)
ax.fill_between(x, y, where=(x > -1) & (x < 1), color=RED_L)
ax.plot(x, y, color=RED, lw=4)
ax.axis("off")
save(fig, "cover.png")

# 학습 목표 그림: 이산 vs 연속
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.2, 3.9))
k = np.arange(0, 6)
p = np.array([1, 5, 10, 10, 5, 1]) / 32
a1.vlines(k, 0, p, color=RED, lw=5)
a1.plot(k, p, "o", color=RED, ms=8)
a1.set_title("이산", fontsize=18)
a1.set_xticks(k); a1.set_yticks([]); a1.set_ylim(0, .38); clean(a1)
y = np.exp(-x**2 / 2)
a2.fill_between(x, y, where=(x > -.6) & (x < .9), color=RED_L)
a2.plot(x, y, color=RED, lw=3)
a2.set_title("연속", fontsize=18)
a2.set_xticks([]); a2.set_yticks([]); a2.set_ylim(0, 1.15); clean(a2)
fig.tight_layout()
save(fig, "goal.png")

# 확률변수: 근원사건 → 실수 대응
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
ax.add_patch(Ellipse((2.5, 2.8), 3.2, 5, fc="#F7F7F7", ec=INK, lw=1.5))
ax.add_patch(Ellipse((7.6, 2.8), 2.0, 4.4, fc="#FDECEC", ec=RED, lw=1.5))
ax.text(2.5, 5.65, "표본공간 $S$", ha="center", fontsize=17)
ax.text(7.6, 5.65, "$X$의 값 (실수)", ha="center", fontsize=17, color=RED)
events = ["(H, H)", "(H, T)", "(T, H)", "(T, T)"]
ey = [4.4, 3.35, 2.3, 1.25]
vals = {2: 4.1, 1: 2.8, 0: 1.5}
for e, yy, v in zip(events, ey, [2, 1, 1, 0]):
    ax.text(2.5, yy, e, ha="center", va="center", fontsize=17)
    ax.add_patch(FancyArrowPatch((3.55, yy), (7.2, vals[v]), arrowstyle="-|>",
                                 mutation_scale=16, color=GRAY, lw=1.6))
for v, yy in vals.items():
    ax.text(7.6, yy, str(v), ha="center", va="center", fontsize=22, color=RED, weight="bold")
ax.text(5.15, 0.05, "$X$ = 앞면(H)이 나온 횟수", ha="center", fontsize=15, color=GRAY)
save(fig, "random_variable.png")

# 이산 vs 연속 미리보기
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.0))
for a in (a1, a2):
    a.set_ylim(-1, 1.6); a.axis("off"); a.axhline(0, color=INK, lw=1.5)
a1.set_xlim(-0.6, 3.8)
for v in range(4):
    a1.plot(v, 0, "o", ms=16, color=RED)
    a1.text(v, -0.6, str(v), ha="center", fontsize=17)
a1.text(1.6, 1.15, "검사한 부품 3개 중 불량품 수", ha="center", fontsize=17, weight="bold")
a1.text(1.6, 0.55, "0, 1, 2, 3 → 하나씩 셀 수 있는 값", ha="center", fontsize=15, color=GRAY)
a2.set_xlim(-1, 11.5)
a2.plot([0, 10], [0, 0], color=RED, lw=9, solid_capstyle="butt")
a2.plot([0, 10], [0, 0], "|", ms=22, mew=3, color=RED)
for v in (0, 5, 10):
    a2.text(v, -0.6, str(v), ha="center", fontsize=17)
a2.text(11.0, -0.6, "(분)", fontsize=14, color=GRAY)
a2.text(5, 1.15, "지하철 대기 시간", ha="center", fontsize=17, weight="bold")
a2.text(5, 0.55, "0 이상 10 이하의 모든 실수", ha="center", fontsize=15, color=GRAY)
fig.tight_layout(w_pad=4)
save(fig, "discrete_vs_continuous.png")

# 동전 예: 확률분포 표 + 그래프
fig, (at, ag) = plt.subplots(1, 2, figsize=(11, 3.8), gridspec_kw={"width_ratios": [1.25, 1]})
at.axis("off")
cells = [["$X$", "0", "1", "2", "합계"],
         ["$P(X=x)$", r"$\frac{1}{4}$", r"$\frac{1}{2}$", r"$\frac{1}{4}$", "1"]]
tb = at.table(cellText=cells, loc="center", cellLoc="center")
tb.scale(1, 3.6); tb.auto_set_font_size(False); tb.set_fontsize(18)
for (r, c), cell in tb.get_celld().items():
    cell.set_edgecolor(GRAY_L)
    if c == 0:
        cell.set_facecolor("#FDECEC")
xs = [0, 1, 2]; ps = [.25, .5, .25]
ag.vlines(xs, 0, ps, color=RED, lw=6)
ag.plot(xs, ps, "o", color=RED, ms=9)
for xx, pp, lab in zip(xs, ps, ["1/4", "1/2", "1/4"]):
    ag.text(xx, pp + .04, lab, ha="center", fontsize=15)
ag.set_xticks(xs); ag.set_yticks([0, .25, .5]); ag.set_ylim(0, .62); ag.set_xlim(-.6, 2.6)
ag.set_xlabel("$x$"); ag.set_ylabel("$P(X=x)$"); clean(ag)
fig.tight_layout()
save(fig, "pmf_coin.png")

# 불량품 예: 10개 중 불량 2개, 3개 임의 추출 (C(10,3)=120)
num = [56, 56, 8]
fig, ax = plt.subplots(figsize=(6.4, 4.4))
ax.bar(xs, [n / 120 for n in num], width=.5, color=RED)
for xx, n in zip(xs, num):
    ax.text(xx, n / 120 + .015, f"{n}/120", ha="center", fontsize=16)
ax.set_xticks(xs); ax.set_xticklabels(["0개", "1개", "2개"]); ax.set_yticks([])
ax.set_xlabel("뽑은 3개 중 불량품 수 $X$"); ax.set_ylim(0, .6)
clean(ax); ax.spines["left"].set_visible(False)
ax.text(1, .55, "합계 = 120/120 = 1", ha="center", fontsize=16, color=RED, weight="bold")
save(fig, "pmf_defect.png")

# 연속: 지하철 대기 시간 (교과서 예)
fig, ax = plt.subplots(figsize=(6.6, 4.0))
ax.plot([0, 10], [.1, .1], color=RED, lw=3.5)
ax.plot([10, 10], [0, .1], color=RED, lw=1.2, ls="--")
ax.fill_between([3, 7], 0, .1, color=RED_L)
ax.text(5, .05, "$P(3 \\leq X \\leq 7)$\n$= \\frac{7-3}{10}$", ha="center", va="center", fontsize=16)
ax.text(10.3, .1, r"$f(x)=\frac{1}{10}$", va="center", fontsize=17, color=RED)
ax.set_xlim(0, 12.6); ax.set_ylim(0, .15)
ax.set_xticks([0, 3, 7, 10]); ax.set_yticks([.1]); ax.set_yticklabels([r"$\frac{1}{10}$"])
ax.set_xlabel("대기 시간 $x$ (분)"); clean(ax)
save(fig, "uniform_subway.png")

# 확률밀도함수의 성질
xx = np.linspace(0, 10, 400)
f = np.exp(-(xx - 5)**2 / (2 * 1.6**2))
fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.fill_between(xx, f, color="#F2F2F2")
ax.fill_between(xx, f, where=(xx >= 4.2) & (xx <= 6.3), color=RED_L)
ax.plot(xx, f, color=RED, lw=3)
ax.annotate("$P(a \\leq X \\leq b)$\n= 색칠한 넓이", xy=(5.3, .5), xytext=(7.4, .95), fontsize=15,
            arrowprops=dict(arrowstyle="-", color=GRAY))
ax.text(0.2, .92, "전체 넓이 = 1", fontsize=15, color=GRAY)
ax.set_xticks([4.2, 6.3]); ax.set_xticklabels(["$a$", "$b$"], fontsize=18); ax.set_yticks([])
ax.set_ylim(0, 1.2); ax.text(8.4, .14, "$y=f(x)$", fontsize=16, color=RED); clean(ax)
save(fig, "pdf_area.png")

# 정리: 이산 vs 연속 비교
fig = plt.figure(figsize=(11.5, 5.2))
for i, (title, sub) in enumerate([("이산확률변수", "셀 수 있는 값"), ("연속확률변수", "어떤 범위의 모든 실수")]):
    ax = fig.add_axes([0.03 + i * 0.5, 0.42, 0.44, 0.48])
    if i == 0:
        ax.vlines([0, 1, 2], 0, [.25, .5, .25], color=RED, lw=6)
        ax.plot([0, 1, 2], [.25, .5, .25], "o", color=RED, ms=9)
        ax.set_xlim(-.7, 2.7); ax.set_ylim(0, .6)
    else:
        ax.fill_between(xx, f, where=(xx >= 4.2) & (xx <= 6.3), color=RED_L)
        ax.plot(xx, f, color=RED, lw=3); ax.set_ylim(0, 1.2)
    ax.set_xticks([]); ax.set_yticks([]); clean(ax)
    ax.set_title(f"{title}  ·  {sub}", fontsize=18, weight="bold")
rows = [("확률을 나타내는 함수", "확률질량함수  $P(X=x_i)=p_i$", "확률밀도함수  $y=f(x)$"),
        ("확률의 의미", "막대의 높이", "그래프 아래의 넓이"),
        ("전체 확률", "$p_1+p_2+\\cdots+p_n=1$", "전체 넓이 = 1")]
for j, (lab, d, c) in enumerate(rows):
    yy = 0.27 - j * 0.11
    fig.text(0.22, yy, d, ha="center", va="center", fontsize=16)
    fig.text(0.78, yy, c, ha="center", va="center", fontsize=16)
    fig.text(0.5, yy, lab, ha="center", va="center", fontsize=13, color="white",
             bbox=dict(boxstyle="round,pad=0.35", fc=GRAY, ec="none"))
save(fig, "summary_compare.png")

# 확인 문제: f(x)=kx (교과서 문제 3)
fig, ax = plt.subplots(figsize=(4.6, 3.8))
ax.fill_between([0, 2], [0, 0], [0, 2], color=RED_L)
ax.plot([0, 4, 4], [0, 4, 0], color=RED, lw=3)
ax.plot([0, 4], [4, 4], color=GRAY, ls=":", lw=1.2)
ax.text(0.9, 3.0, "$y=f(x)=kx$", fontsize=16, color=RED)
ax.set_xticks([0, 2, 4]); ax.set_yticks([4]); ax.set_yticklabels(["$4k$"])
ax.set_xlim(0, 5); ax.set_ylim(0, 4.8); clean(ax)
save(fig, "quiz_triangle.png")
print("ok")
