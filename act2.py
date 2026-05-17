from manim import *

from shared import (
    make_agent_box,
    make_bubble,
    make_caption,
    make_context_bar,
    pulse_subagent,
    swap_caption,
)


COORD = BLUE
SOCIAL = PURPLE
MATH = ORANGE


class Act2SubagentsAsTools(Scene):
    def construct(self):
        coordinator = make_agent_box("Coordinator Agent", COORD).move_to(LEFT * 3.5)
        social = make_agent_box("Social Media Agent", SOCIAL).move_to(RIGHT * 2.5 + UP * 1.5)
        math_agent = make_agent_box("Mathematician", MATH).move_to(RIGHT * 2.5 + DOWN * 1.5)

        self.add(coordinator, social, math_agent)
        self.wait(0.4)

        parts = self.scene_2_1(coordinator)
        self.scene_2_2(coordinator, social, parts)
        self.scene_2_3(coordinator, math_agent, parts)

    # ─── Scene 2.1 — Coordinator expands and exposes its tools ────────────────

    def scene_2_1(self, coordinator):
        cap = make_caption(
            "Strategy 1: Subagents as Tools — Coordinator calls each one as a function"
        )
        self.play(FadeIn(cap), run_time=0.6)
        self.wait(0.4)

        new_center = LEFT * 3.2
        new_width = 5.0
        new_height = 4.5
        sub_w = new_width / 2 - 0.35
        sub_h = new_height - 1.0

        target_outer = RoundedRectangle(
            corner_radius=0.2, width=new_width, height=new_height,
            color=COORD, fill_color=COORD, fill_opacity=0.15, stroke_width=2.5,
        ).move_to(new_center)
        target_label = Text(
            "Coordinator Agent", font_size=22, color=COORD, weight=BOLD
        ).next_to(target_outer, UP, buff=0.15)

        llm_target = RoundedRectangle(
            corner_radius=0.12, width=sub_w, height=sub_h,
            color=COORD, fill_color=COORD, fill_opacity=0.10, stroke_width=1.5,
        ).move_to(target_outer.get_center() + LEFT * (sub_w / 2 + 0.15) + DOWN * 0.2)
        llm_text_target = Text(
            "LLM", font_size=14, color=COORD, weight=BOLD
        ).next_to(llm_target.get_top(), DOWN, buff=0.10)

        tools_target = RoundedRectangle(
            corner_radius=0.12, width=sub_w, height=sub_h,
            color=COORD, fill_color=COORD, fill_opacity=0.10, stroke_width=1.5,
        ).move_to(target_outer.get_center() + RIGHT * (sub_w / 2 + 0.15) + DOWN * 0.2)
        tools_text_target = Text(
            "Tools", font_size=14, color=COORD, weight=BOLD
        ).next_to(tools_target.get_top(), DOWN, buff=0.10)

        self.play(
            Transform(coordinator[0], target_outer),
            Transform(coordinator[1], target_label),
            Transform(coordinator[2], llm_target),
            Transform(coordinator[3], llm_text_target),
            Transform(coordinator[4], tools_target),
            Transform(coordinator[5], tools_text_target),
            run_time=0.9,
        )
        self.wait(0.3)

        cap2 = make_caption("Each subagent appears in the Coordinator's tool list")
        swap_caption(self, cap, cap2)

        tool1 = Text(
            "call_social_agent(...)",
            font_size=9, color=SOCIAL, weight=BOLD, font="Monospace",
        )
        tool2 = Text(
            "ask_mathematician(...)",
            font_size=9, color=MATH, weight=BOLD, font="Monospace",
        )
        tool_list = VGroup(tool1, tool2).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        tool_list.move_to(tools_target.get_center() + DOWN * 0.1)

        self.play(FadeIn(tool1, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(tool2, shift=UP * 0.1), run_time=0.5)
        self.wait(0.5)

        sys_bar = make_context_bar(
            "System Prompt",
            width=sub_w - 0.25, height=0.30,
            fill_color="#1a3a5c", stroke_color=BLUE_B, text_color=BLUE_C,
            font_size=10, stroke_width=1.2,
        ).move_to(llm_target.get_center() + UP * 1.30)
        user_bar = make_context_bar(
            "User Query: ad strategies + ROI",
            width=sub_w - 0.25, height=0.30,
            fill_color="#1a3a2c", stroke_color=GREEN_B, text_color=GREEN_C,
            font_size=9, stroke_width=1.2,
        ).move_to(llm_target.get_center() + UP * 0.95)

        self.play(FadeIn(sys_bar), run_time=0.4)
        self.play(FadeIn(user_bar), run_time=0.4)
        self.wait(0.8)

        self.play(FadeOut(cap2), run_time=0.4)

        return {
            "outer_ref": target_outer,
            "llm_ref": llm_target,
            "tools_ref": tools_target,
            "tool_list": tool_list,
            "sub_w": sub_w,
            "stack_anchor_y_offset": 0.45,
        }

    # ─── Scene 2.2 — First tool call: Social Media Agent ─────────────────────

    def scene_2_2(self, coordinator, social, parts):
        tools_ref = parts["tools_ref"]
        llm_ref = parts["llm_ref"]
        sub_w = parts["sub_w"]

        cap = make_caption("Coordinator emits a tool call for the Social Media Agent")
        self.play(FadeIn(cap), run_time=0.5)

        social_tool_name = parts["tool_list"][0]
        self.play(Indicate(social_tool_name, color=GREEN_C, scale_factor=1.2), run_time=0.6)

        call_bar = make_context_bar(
            "call_social_agent(...)",
            width=sub_w - 0.25, height=0.30,
            fill_color="#1a2d1a", stroke_color=GREEN_C, text_color=GREEN_C,
            font_size=9, stroke_width=1.2,
        ).move_to(llm_ref.get_center() + UP * 0.55)
        self.play(FadeIn(call_bar), run_time=0.4)

        call_bubble = make_bubble(
            """call_social_agent("Research the advertising strategies for each channel and their costs")""",
            color=GREEN_C, font_size=11, padding_x=0.25,
        )
        call_bubble.move_to(tools_ref.get_right() + RIGHT * 0.5 + UP * 0.6)
        self.play(FadeIn(call_bubble, shift=RIGHT * 0.2, scale=0.9), run_time=0.5)
        self.wait(0.2)

        target_pos = social[0].get_left() + LEFT * 0.55
        self.play(call_bubble.animate.move_to(target_pos), run_time=0.9)
        self.play(FadeOut(call_bubble), run_time=0.3)

        cap2 = make_caption("Social Media Agent runs its own LLM + tool loop")
        swap_caption(self, cap, cap2)

        pulse_subagent(self, social, SOCIAL, repeats=2, run_time=0.35)
        self.wait(0.3)

        result_bubble = make_bubble(
            "SEO 3% / Paid 5% / Email 8%",
            color=SOCIAL, font_size=11, padding_x=0.25,
        )
        result_bubble.move_to(social[0].get_left() + LEFT * 0.55)
        self.play(FadeIn(result_bubble, scale=0.9), run_time=0.45)

        cap3 = make_caption("Result returns and is stored in the Coordinator's context")
        swap_caption(self, cap2, cap3)

        social_bar = make_context_bar(
            "SEO 3% / Paid 5% / Email 8%",
            width=sub_w - 0.25, height=0.30,
            fill_color="#2a1a3c", stroke_color=PURPLE_B, text_color=PURPLE_A,
            font_size=9, stroke_width=1.2,
        ).move_to(llm_ref.get_center() + UP * 0.20)

        self.play(
            result_bubble.animate.move_to(social_bar.get_center()).scale(0.6),
            run_time=0.9,
        )
        self.play(
            FadeOut(result_bubble),
            FadeIn(social_bar),
            run_time=0.4,
        )
        self.play(Indicate(social_bar, color=PURPLE_A, scale_factor=1.06), run_time=0.6)
        self.wait(0.6)

        self.play(FadeOut(cap3), run_time=0.3)

        parts["social_bar"] = social_bar

    # ─── Scene 2.3 — Second tool call: Mathematician ─────────────────────────

    def scene_2_3(self, coordinator, math_agent, parts):
        tools_ref = parts["tools_ref"]
        llm_ref = parts["llm_ref"]
        sub_w = parts["sub_w"]

        cap = make_caption("Coordinator calls the Mathematician with the new numbers")
        self.play(FadeIn(cap), run_time=0.5)

        math_tool_name = parts["tool_list"][1]
        self.play(Indicate(math_tool_name, color=GREEN_C, scale_factor=1.2), run_time=0.5)

        call_bar = make_context_bar(
            "→ ask_mathematician(CAC + ROI)",
            width=sub_w - 0.25, height=0.30,
            fill_color="#1a2d1a", stroke_color=GREEN_C, text_color=GREEN_C,
            font_size=9, stroke_width=1.2,
        ).move_to(llm_ref.get_center() + DOWN * 0.15)
        self.play(FadeIn(call_bar), run_time=0.4)

        call_bubble = make_bubble(
            "ask_mathematician(CAC + ROI)",
            color=GREEN_C, font_size=11, padding_x=0.25,
        )
        call_bubble.move_to(tools_ref.get_right() + RIGHT * 0.5 + DOWN * 0.6)
        self.play(FadeIn(call_bubble, shift=RIGHT * 0.2, scale=0.9), run_time=0.5)

        target_pos = math_agent[0].get_left() + LEFT * 0.55
        self.play(call_bubble.animate.move_to(target_pos), run_time=0.9)
        self.play(FadeOut(call_bubble), run_time=0.3)

        cap2 = make_caption("Mathematician computes — same internal loop, hidden from Coordinator")
        swap_caption(self, cap, cap2)

        pulse_subagent(self, math_agent, MATH, repeats=1, run_time=0.35)
        self.wait(0.2)

        result_lines = VGroup(
            Text("CAC: $15 / $22 / $9", font_size=11, color=MATH, weight=BOLD, font="Monospace"),
            Text("ROI: 1.9× / 2.1× / 4.8×", font_size=11, color=MATH, weight=BOLD, font="Monospace"),
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        result_bg = RoundedRectangle(
            corner_radius=0.18,
            width=result_lines.width + 0.5,
            height=result_lines.height + 0.35,
            color=MATH, fill_color="#15151f", fill_opacity=0.95, stroke_width=2.5,
        ).move_to(result_lines)
        result_bubble = VGroup(result_bg, result_lines)
        result_bubble.move_to(math_agent[0].get_left() + LEFT * 0.75)

        self.play(FadeIn(result_bubble, scale=0.9), run_time=0.45)

        cap3 = make_caption("Result returns — Coordinator now holds both pieces")
        swap_caption(self, cap2, cap3)

        math_bar = make_context_bar(
            "Math: CAC + ROI per channel",
            width=sub_w - 0.25, height=0.30,
            fill_color="#3a2a0c", stroke_color=ORANGE, text_color=ORANGE,
            font_size=9, stroke_width=1.2,
        ).move_to(llm_ref.get_center() + DOWN * 0.50)

        self.play(
            result_bubble.animate.move_to(math_bar.get_center()).scale(0.5),
            run_time=0.9,
        )
        self.play(
            FadeOut(result_bubble),
            FadeIn(math_bar),
            run_time=0.4,
        )
        self.play(Indicate(math_bar, color=ORANGE, scale_factor=1.06), run_time=0.6)
        self.wait(1.5)
