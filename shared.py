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