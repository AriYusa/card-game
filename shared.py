import numpy as np
from manim import *


def make_caption(text, font_size=22, color=WHITE, buff=0.35):
    return Text(text, font_size=font_size, color=color).to_edge(DOWN, buff=buff)


def swap_caption(scene, old, new, run_time=0.7):
    scene.play(ReplacementTransform(old, new), run_time=run_time)


def make_agent_box(name, color, width=2.8, height=2.45):
    box = RoundedRectangle(
        corner_radius=0.2,
        width=width,
        height=height,
        color=color,
        fill_color=color,
        fill_opacity=0.15,
        stroke_width=2.5,
    )
    label = Text(name, font_size=19, color=color, weight=BOLD).next_to(
        box, UP, buff=0.15
    )
    sub_box_width = width / 2 - 0.25
    llm_bar = RoundedRectangle(
        corner_radius=0.08,
        width=sub_box_width,
        height=0.5,
        color=color,
        fill_color=color,
        fill_opacity=0.18,
        stroke_width=1.5,
    ).move_to(box.get_center() + LEFT * (sub_box_width / 2 + 0.05))
    llm_text = Text("LLM", font_size=12, color=color, weight=BOLD).move_to(llm_bar)
    tools_bar = RoundedRectangle(
        corner_radius=0.08,
        width=sub_box_width,
        height=0.5,
        color=color,
        fill_color=color,
        fill_opacity=0.18,
        stroke_width=1.5,
    ).move_to(box.get_center() + RIGHT * (sub_box_width / 2 + 0.05))
    tools_text = Text("Tools", font_size=12, color=color, weight=BOLD).move_to(tools_bar)
    return VGroup(box, label, llm_bar, llm_text, tools_bar, tools_text)


def make_user_icon(color=BLUE_C, label="User"):
    head = Circle(
        radius=0.25,
        color=color,
        fill_color=color,
        fill_opacity=0.9,
        stroke_width=2,
    )
    body = RoundedRectangle(
        corner_radius=0.12,
        width=0.55,
        height=0.6,
        color=color,
        fill_color=color,
        fill_opacity=0.9,
        stroke_width=2,
    ).next_to(head, DOWN, buff=0.05)
    icon = VGroup(head, body)
    lbl = Text(label, font_size=16, color=color).next_to(icon, DOWN, buff=0.1)
    return VGroup(icon, lbl)


def make_context_bar(
    text,
    *,
    width=2.4,
    height=0.42,
    fill_color="#1a3a5c",
    stroke_color=BLUE_B,
    text_color=WHITE,
    font_size=11,
    stroke_width=1.0,
    corner_radius=0.08,
    fill_opacity=1,
):
    bar = RoundedRectangle(
        corner_radius=corner_radius,
        width=width,
        height=height,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
        stroke_color=stroke_color,
        stroke_width=stroke_width,
    )
    label = Text(text, font_size=font_size, color=text_color).move_to(bar)
    return VGroup(bar, label)


def make_bubble(
    text,
    *,
    color=GREEN_C,
    fill_color="#15151f",
    font_size=12,
    weight=BOLD,
    width=None,
    height=None,
    padding_x=0.3,
    padding_y=0.18,
    fill_opacity=0.95,
    stroke_width=2.5,
    corner_radius=0.18,
):
    """Solid rounded bubble (dark fill, colored border + text) for tool calls and results."""
    label = Text(text, font_size=font_size, color=color, weight=weight)
    box_width = width if width is not None else max(label.width + 2 * padding_x, 1.0)
    box_height = height if height is not None else max(label.height + 2 * padding_y, 0.5)
    bg = RoundedRectangle(
        corner_radius=corner_radius,
        width=box_width,
        height=box_height,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
        stroke_color=color,
        stroke_width=stroke_width,
    )
    label.move_to(bg)
    return VGroup(bg, label)


def pulse_subagent(scene, agent, color, repeats=2, run_time=0.35):
    """Pulse an agent's outer box with curved arrows looping between LLM and Tools sub-bars."""
    outer = agent[0]
    llm_bar = agent[2]
    tools_bar = agent[4]

    base_stroke = outer.get_stroke_width() or 2.5
    for _ in range(repeats):
        curve_out = CurvedArrow(
            llm_bar.get_top() + UP * 0.04,
            tools_bar.get_top() + UP * 0.04,
            color=color,
            stroke_width=2.5,
            angle=-PI / 2.5,
        )
        curve_back = CurvedArrow(
            tools_bar.get_bottom() + DOWN * 0.04,
            llm_bar.get_bottom() + DOWN * 0.04,
            color=color,
            stroke_width=2.5,
            angle=-PI / 2.5,
        )
        scene.play(
            outer.animate.set_stroke(width=base_stroke + 2),
            Create(curve_out),
            run_time=run_time,
        )
        scene.play(Create(curve_back), run_time=run_time)
        scene.play(
            outer.animate.set_stroke(width=base_stroke),
            FadeOut(curve_out),
            FadeOut(curve_back),
            run_time=run_time,
        )


_OWNER_BAR_STYLE = {
    "BLUE": ("#1a3a5c", BLUE_B, BLUE_C),
    "PURPLE": ("#2a1a3c", PURPLE_B, PURPLE_A),
    "ORANGE": ("#3a2a0c", ORANGE, ORANGE),
}


def _owner_style(owner_color):
    if owner_color is BLUE:
        return _OWNER_BAR_STYLE["BLUE"]
    if owner_color is PURPLE:
        return _OWNER_BAR_STYLE["PURPLE"]
    if owner_color is ORANGE:
        return _OWNER_BAR_STYLE["ORANGE"]
    return ("#202020", owner_color, owner_color)


def tinted_bar(
    text,
    owner_color,
    *,
    width=2.0,
    height=0.28,
    font_size=9,
    weight=None,
):
    """Context bar visually tinted by the agent that authored it.
    Use for handoff-strategy stacks so layers retain provenance."""
    fill, stroke, text_color = _owner_style(owner_color)
    bar = RoundedRectangle(
        corner_radius=0.08,
        width=width,
        height=height,
        fill_color=fill,
        fill_opacity=1.0,
        stroke_color=stroke,
        stroke_width=1.2,
    )
    kwargs = {"font_size": font_size, "color": text_color}
    if weight is not None:
        kwargs["weight"] = weight
    label = Text(text, **kwargs).move_to(bar)
    return VGroup(bar, label)


def expanded_agent_targets(name, color, center, *, width=4.5, height=3.8, label_font_size=20):
    """Mirror of make_agent_box's 6-element shape at expanded size.
    Pair with Transform(...) to grow/shrink an agent in place.
    Returns VGroup(outer, label, llm_bar, llm_text, tools_bar, tools_text)."""
    outer = RoundedRectangle(
        corner_radius=0.2,
        width=width,
        height=height,
        color=color,
        fill_color=color,
        fill_opacity=0.12,
        stroke_width=2.5,
    ).move_to(center)
    label = Text(name, font_size=label_font_size, color=color, weight=BOLD).next_to(
        outer, UP, buff=0.15
    )
    sub_w = width / 2 - 0.30
    sub_h = height - 0.85
    llm = RoundedRectangle(
        corner_radius=0.12,
        width=sub_w,
        height=sub_h,
        color=color,
        fill_color=color,
        fill_opacity=0.10,
        stroke_width=1.5,
    ).move_to(outer.get_center() + LEFT * (sub_w / 2 + 0.15) + DOWN * 0.20)
    llm_text = Text("LLM", font_size=12, color=color, weight=BOLD).next_to(
        llm.get_top(), DOWN, buff=0.08
    )
    tools = RoundedRectangle(
        corner_radius=0.12,
        width=sub_w,
        height=sub_h,
        color=color,
        fill_color=color,
        fill_opacity=0.10,
        stroke_width=1.5,
    ).move_to(outer.get_center() + RIGHT * (sub_w / 2 + 0.15) + DOWN * 0.20)
    tools_text = Text("Tools", font_size=12, color=color, weight=BOLD).next_to(
        tools.get_top(), DOWN, buff=0.08
    )
    return VGroup(outer, label, llm, llm_text, tools, tools_text)


def llm_stack_positions(llm_box, n, *, top_buff=0.40, slot_height=0.34, center_x=None):
    """Generate n vertical slot centers inside an LLM sub-box, top-down."""
    top_y = llm_box.get_top()[1] - top_buff
    x = llm_box.get_center()[0] if center_x is None else center_x
    return [np.array([x, top_y - i * slot_height, 0]) for i in range(n)]


def fly_copy_bars(scene, source_bars, target_positions, *, run_time=1.0, arc=PI / 3, lag_ratio=0.0):
    """Duplicate bars and animate the copies along arc paths to target_positions.
    Originals stay in place. Returns the copies so callers can keep references.
    Default lag_ratio=0.0 moves all copies together; raise it to stagger them."""
    copies = []
    moves = []
    for bar, pos in zip(source_bars, target_positions):
        c = bar.copy()
        scene.add(c)
        copies.append(c)
        path = ArcBetweenPoints(c.get_center(), pos, angle=arc)
        moves.append(MoveAlongPath(c, path))
    scene.play(AnimationGroup(*moves, lag_ratio=lag_ratio), run_time=run_time)
    return copies