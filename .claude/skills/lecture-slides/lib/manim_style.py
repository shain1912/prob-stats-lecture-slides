"""manim 공통 스타일 — 강의 애니메이션 파일 맨 위에서 import

    import sys; sys.path.insert(0, r"<skill>/lib")
    from manim_style import *

화면 1600×800(2:1, 좌표 16×8), 흰 배경, 양식 색상, 맑은 고딕.
LaTeX가 없으므로 MathTex·DecimalNumber·Axes 숫자 라벨을 쓰지 말고 T()와 x_labels()를 사용.
"""
from manim import *

config.pixel_width = 1600
config.pixel_height = 800
config.frame_height = 8
config.frame_width = 16
config.frame_rate = 30
config.background_color = WHITE

RED_ = ManimColor("#E22B2D")
RED_L = ManimColor("#F6C4C5")
GRAY_ = ManimColor("#8C8C8C")
GRAY_L = ManimColor("#D9D9D9")
INK = ManimColor("#3F3F3F")
FONT = "Malgun Gothic"


def T(s, size=36, color=INK, **kw):
    """한글·수식 공용 텍스트. 줄바꿈은 \\n, 굵게는 weight=BOLD"""
    return Text(s, font=FONT, font_size=size, color=color, **kw)


def axes(x_range, y_range, x_len, y_len):
    """숫자 라벨 없는 축. y축은 x=0에 그려지므로 막대는 x=0.6부터 배치"""
    return Axes(x_range=x_range, y_range=y_range, x_length=x_len, y_length=y_len,
                axis_config={"color": INK, "include_tip": False, "include_numbers": False,
                             "stroke_width": 3})


def x_labels(ax, values, size=30, texts=None):
    texts = texts or [str(v) for v in values]
    return VGroup(*[T(t, size).next_to(ax.c2p(v, 0), DOWN, buff=0.2) for v, t in zip(values, texts)])
