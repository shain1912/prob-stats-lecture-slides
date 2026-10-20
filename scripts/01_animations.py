"""1강 확률변수와 확률분포 — manim 애니메이션

렌더: python .claude/skills/lecture-slides/tools/render_animations.py scripts/01_animations.py lectures/01-introduction/assets/anim <임시폴더>
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".claude/skills/lecture-slides/lib"))
from manim_style import *


class RandomVariable(Scene):
    """근원사건 → 실수 대응"""
    def construct(self):
        title = T("표본공간의 각 결과 → 실수 하나로 대응", 40).to_edge(UP, buff=0.4)
        left = Ellipse(width=3.6, height=5.4, color=INK, fill_color="#F7F7F7", fill_opacity=1).shift(LEFT * 3.6 + DOWN * 0.5)
        right = Ellipse(width=2.4, height=4.6, color=RED_, fill_color="#FDECEC", fill_opacity=1).shift(RIGHT * 3.6 + DOWN * 0.5)
        lt = T("표본공간 S", 32).next_to(left, UP, buff=0.2)
        rt = T("X의 값 (실수)", 32, RED_).next_to(right, UP, buff=0.2)
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.play(Create(left), Create(right), FadeIn(lt), FadeIn(rt))

        events = ["(H, H)", "(H, T)", "(T, H)", "(T, T)"]
        evs = VGroup(*[T(e, 34) for e in events]).arrange(DOWN, buff=0.55).move_to(left)
        nums = {v: T(str(v), 48, RED_, weight=BOLD) for v in (2, 1, 0)}
        VGroup(*nums.values()).arrange(DOWN, buff=1.0).move_to(right)
        self.play(LaggedStart(*[FadeIn(e, shift=RIGHT * 0.2) for e in evs], lag_ratio=0.25))
        self.play(LaggedStart(*[FadeIn(n, scale=0.5) for n in nums.values()], lag_ratio=0.2))
        for e, v in zip(evs, [2, 1, 1, 0]):
            arrow = Arrow(e.get_right(), nums[v].get_left(), buff=0.25, color=GRAY_, stroke_width=4,
                          max_tip_length_to_length_ratio=0.06)
            self.play(Indicate(e, color=RED_, scale_factor=1.15), GrowArrow(arrow), run_time=0.8)
            self.play(Indicate(nums[v], scale_factor=1.4), run_time=0.5)
        cap = T("X = 앞면(H)이 나온 횟수  →  확률변수", 34, RED_).to_edge(DOWN, buff=0.3)
        self.play(Write(cap))
        self.wait(1.5)


class DiscreteContinuous(Scene):
    """셀 수 있는 값 vs 범위 안의 모든 실수"""
    def construct(self):
        div = Line(UP * 3.6, DOWN * 3.6, color=GRAY_L)
        lt = T("이산: 불량품 수", 38, weight=BOLD).move_to(LEFT * 4 + UP * 2.8)
        rt = T("연속: 지하철 대기 시간", 38, weight=BOLD).move_to(RIGHT * 4 + UP * 2.8)
        self.play(Create(div), FadeIn(lt), FadeIn(rt))

        nl = NumberLine(x_range=[0, 3, 1], length=5.5, color=INK, include_numbers=False).move_to(LEFT * 4)
        nl_lab = VGroup(*[T(str(i), 32).next_to(nl.n2p(i), DOWN, buff=0.3) for i in range(4)])
        self.play(Create(nl), FadeIn(nl_lab))
        dots = VGroup(*[Dot(nl.n2p(i), radius=0.18, color=RED_) for i in range(4)])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.35))
        lcap = T("하나씩 셀 수 있는 값", 32, GRAY_).next_to(nl, DOWN, buff=1.2)
        self.play(FadeIn(lcap))

        nr = NumberLine(x_range=[0, 10, 1], length=6, color=INK, include_numbers=False).move_to(RIGHT * 4)
        nr_lab = VGroup(*[T(str(i), 32).next_to(nr.n2p(i), DOWN, buff=0.3) for i in (0, 5, 10)])
        unit = T("(분)", 26, GRAY_).next_to(nr, RIGHT, buff=0.45).shift(DOWN * 0.45)
        self.play(Create(nr), FadeIn(nr_lab), FadeIn(unit))
        seg = Line(nr.n2p(0), nr.n2p(10), color=RED_, stroke_width=14)
        self.play(Create(seg), run_time=1.5)
        t = ValueTracker(0.0)
        dot = always_redraw(lambda: Dot(nr.n2p(t.get_value()), radius=0.16, color=INK))
        val = always_redraw(lambda: T(f"{t.get_value():.2f}분", 30).next_to(dot, UP, buff=0.3))
        self.add(dot, val)
        for target in (3.71, 8.26, 1.05, 6.48):
            self.play(t.animate.set_value(target), run_time=0.9)
        rcap = T("0~10 사이의 모든 실수", 32, GRAY_).next_to(nr, DOWN, buff=1.2)
        self.play(FadeIn(rcap))
        self.wait(1.5)


class PmfCoin(Scene):
    """확률질량함수: 막대 높이 = 확률, 합 = 1"""
    def construct(self):
        title = T("동전 2번 던지기: 앞면이 나온 횟수 X", 38).to_edge(UP, buff=0.4)
        self.play(FadeIn(title))
        ax = axes([0, 3.2, 1], [0, 1.05, 0.25], 6.5, 5).shift(LEFT * 2.6 + DOWN * 0.5)
        ylab = VGroup(*[T(t, 26).next_to(ax.c2p(0, v), LEFT, buff=0.15) for v, t in [(0.25, "1/4"), (0.5, "1/2"), (1, "1")]])
        self.play(Create(ax), FadeIn(x_labels(ax, [0.6, 1.6, 2.6], texts=["0", "1", "2"])), FadeIn(ylab))
        ps = [0.25, 0.5, 0.25]
        cols = [RED_, ManimColor("#F08A8B"), ManimColor("#B51F21")]
        stems = VGroup()
        for x, p, c in zip([0, 1, 2], ps, cols):
            bar = Rectangle(width=0.55, height=ax.c2p(0, p)[1] - ax.c2p(0, 0)[1], fill_color=c, fill_opacity=1, stroke_width=0)
            bar.move_to(ax.c2p(x + 0.6, 0), aligned_edge=DOWN)
            lab = T(["1/4", "1/2", "1/4"][x], 30).next_to(bar, UP, buff=0.15)
            self.play(GrowFromEdge(bar, DOWN), FadeIn(lab), run_time=0.8)
            stems.add(bar)
        self.wait(0.5)
        # 막대를 오른쪽에 쌓아 합 = 1 보여주기
        base = ax.c2p(0, 0)[1]
        stack_x = RIGHT * 4.6
        guide = DashedLine(ax.c2p(0, 1), stack_x + UP * (ax.c2p(0, 1)[1]) + RIGHT * 0.6, color=GRAY_)
        y = base
        moves = []
        for bar in stems:
            c = bar.copy()
            moves.append(c.animate.move_to(stack_x + UP * y, aligned_edge=DOWN))
            self.add(c)
            y += bar.height
        self.play(LaggedStart(*moves, lag_ratio=0.4), run_time=2)
        self.play(Create(guide))
        cap = T("1/4 + 1/2 + 1/4 = 1", 34, RED_, weight=BOLD).next_to(stack_x + UP * ax.c2p(0, 1)[1], UP, buff=0.3)
        self.play(Write(cap))
        self.wait(1.5)


class PmfDefect(Scene):
    """부품 10개(불량 2개) 중 3개 추출 시 불량품 수"""
    def construct(self):
        title = T("부품 10개 (불량품 2개) 중 3개를 임의로 뽑을 때 불량품 수 X", 34).to_edge(UP, buff=0.4)
        self.play(FadeIn(title))
        boxes = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.6, height=0.6, stroke_width=0,
                                          fill_color=RED_ if i in (2, 7) else GRAY_L, fill_opacity=1) for i in range(10)])
        boxes.arrange(RIGHT, buff=0.15).next_to(title, DOWN, buff=0.5)
        self.play(LaggedStart(*[FadeIn(b, scale=0.6) for b in boxes], lag_ratio=0.08))
        for pick in ([0, 4, 8], [2, 5, 9], [1, 3, 6]):
            rings = VGroup(*[SurroundingRectangle(boxes[i], color=INK, buff=0.07, stroke_width=4) for i in pick])
            self.play(Create(rings), run_time=0.4)
            self.wait(0.3)
            self.play(FadeOut(rings), run_time=0.3)

        ax = axes([0, 3.2, 1], [0, 0.55, 0.1], 8, 3.6).shift(DOWN * 1.6 + LEFT * 2)
        self.play(Create(ax), FadeIn(x_labels(ax, [0.6, 1.6, 2.6], texts=["0개", "1개", "2개"])))
        for x, n, f in [(0, 56, "₈C₃ / ₁₀C₃"), (1, 56, "₂C₁·₈C₂ / ₁₀C₃"), (2, 8, "₂C₂·₈C₁ / ₁₀C₃")]:
            bar = Rectangle(width=1.1, height=ax.c2p(0, n / 120)[1] - ax.c2p(0, 0)[1], fill_color=RED_, fill_opacity=1, stroke_width=0)
            bar.move_to(ax.c2p(x + 0.6, 0), aligned_edge=DOWN)
            lab = T(f"{n}/120", 30, weight=BOLD).next_to(bar, UP, buff=0.12)
            formula = T(f, 22, GRAY_).next_to(lab, UP, buff=0.08)
            self.play(GrowFromEdge(bar, DOWN), FadeIn(lab), FadeIn(formula), run_time=0.9)
        total = VGroup(T("56 + 56 + 8 = 120", 32, INK), T("→ 확률의 합 = 1", 34, RED_, weight=BOLD)).arrange(DOWN, buff=0.3).move_to(RIGHT * 5 + DOWN * 1.4)
        self.play(Write(total))
        self.wait(1.5)


class UniformSubway(Scene):
    """연속확률변수: 확률 = 그래프 아래 넓이"""
    def construct(self):
        title = T("10분 간격 지하철, 대기 시간 X의 확률밀도함수 f(x) = 1/10", 34).to_edge(UP, buff=0.4)
        self.play(FadeIn(title))
        ax = axes([0, 11, 1], [0, 0.15, 0.05], 12, 4.6).shift(DOWN * 0.6)
        self.play(Create(ax), FadeIn(x_labels(ax, [0, 5, 10])),
                  FadeIn(T("1/10", 28).next_to(ax.c2p(0, 0.1), LEFT, buff=0.15)),
                  FadeIn(T("대기 시간 (분)", 26, GRAY_).next_to(ax.c2p(5, 0), DOWN, buff=0.6)))
        f_line = Line(ax.c2p(0, 0.1), ax.c2p(10, 0.1), color=RED_, stroke_width=6)
        self.play(Create(f_line))

        b = ValueTracker(0.001)
        area = always_redraw(lambda: Polygon(ax.c2p(0, 0), ax.c2p(0, 0.1), ax.c2p(b.get_value(), 0.1), ax.c2p(b.get_value(), 0),
                                             stroke_width=0, fill_color=RED_L, fill_opacity=1))
        edge = always_redraw(lambda: DashedLine(ax.c2p(b.get_value(), 0), ax.c2p(b.get_value(), 0.13), color=INK))
        lab = always_redraw(lambda: T(f"P(0 ≤ X ≤ {b.get_value():.1f}) = {b.get_value():.1f} × 1/10 = {b.get_value() / 10:.2f}",
                                      32, RED_, weight=BOLD).next_to(ax.c2p(5, 0.135), UP, buff=0.1))
        self.add(area, edge, lab)
        self.bring_to_front(f_line)
        self.play(b.animate.set_value(10), run_time=3, rate_func=linear)
        whole = T("전체 넓이 = 1", 32, INK).move_to(ax.c2p(5, 0.05))
        self.play(FadeIn(whole)); self.wait(0.8); self.play(FadeOut(whole))
        self.play(b.animate.set_value(5), run_time=1.5)
        cap = T("5분 이하로\n기다릴 확률 = 1/2", 32, INK, line_spacing=1.2).move_to(ax.c2p(2.5, 0.05))
        self.play(FadeIn(cap))
        self.wait(1.5)


class DensityCurve(Scene):
    """히스토그램 → 확률밀도함수, 넓이 = 확률, 한 점의 확률 = 0"""
    def construct(self):
        mu, sd = 5, 1.6
        cdf = lambda x: 0.5 * (1 + math.erf((x - mu) / (sd * math.sqrt(2))))
        pdf = lambda x: math.exp(-(x - mu) ** 2 / (2 * sd ** 2)) / (sd * math.sqrt(2 * math.pi))
        ax = axes([0, 10, 1], [0, 0.3, 0.1], 12, 5).shift(DOWN * 0.7)
        title = T("계급의 크기를 줄이면 히스토그램 → 매끄러운 곡선", 36).to_edge(UP, buff=0.4)
        self.play(FadeIn(title), Create(ax))

        def hist(w):
            bars = VGroup()
            for k in range(int(10 / w)):
                l = k * w
                h = (cdf(l + w) - cdf(l)) / w
                bars.add(Polygon(ax.c2p(l, 0), ax.c2p(l, h), ax.c2p(l + w, h), ax.c2p(l + w, 0),
                                 fill_color=GRAY_L, fill_opacity=1, stroke_color=WHITE, stroke_width=2))
            return bars
        h = hist(2)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in h], lag_ratio=0.1))
        for w in (1, 0.5, 0.25):
            self.play(Transform(h, hist(w)), run_time=1)
        curve = ax.plot(pdf, x_range=[0, 10], color=RED_, stroke_width=6)
        self.play(Create(curve), run_time=1.5)
        self.play(FadeOut(h))
        fx = T("y = f(x)  확률밀도함수", 30, RED_).next_to(ax.c2p(7.0, pdf(7.0)), UR, buff=0.15)
        self.play(FadeIn(fx))

        a, b = ValueTracker(3.8), ValueTracker(6.4)
        area = always_redraw(lambda: ax.get_area(curve, x_range=[a.get_value(), b.get_value()], color=RED_L, opacity=1))
        lab = always_redraw(lambda: T(f"P(a ≤ X ≤ b) = 넓이 = {cdf(b.get_value()) - cdf(a.get_value()):.3f}", 32, INK, weight=BOLD)
                            .next_to(title, DOWN, buff=0.35))
        new_title = T("확률 = 곡선 아래 넓이", 36).to_edge(UP, buff=0.4)
        self.play(Transform(title, new_title))
        self.add(area); self.bring_to_front(curve)
        self.play(FadeIn(lab))
        self.wait(1)
        # 구간을 한 점으로 좁히기
        self.play(a.animate.set_value(4.999), b.animate.set_value(5.001), run_time=2.5)
        zero = T("구간 → 한 점: 넓이 0  →  P(X = b) = 0", 34, RED_, weight=BOLD).to_edge(DOWN, buff=0.15)
        self.play(Write(zero))
        self.wait(1.5)
