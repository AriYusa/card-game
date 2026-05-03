from manim import *


class Act1SettingTheStage(Scene):
    def construct(self):
        self.scene_1_1()
        self.wait(0.5)
        self.scene_1_2()
        self.wait(0.5)
        self.scene_1_3()

    # ─── helpers ──────────────────────────────────────────────────────────────

    def make_caption(self, text):
        return Text(text, font_size=22, color=WHITE).to_edge(DOWN, buff=0.35)

    def swap_caption(self, old, new):
        self.play(ReplacementTransform(old, new), run_time=0.7)

    def make_agent_box(self, name, color, subtitle, width=2.8, height=2.2):
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
            box.get_top(), DOWN, buff=0.25
        )
        sub = Text(subtitle, font_size=12, color=GREY_A).next_to(label, DOWN, buff=0.15)
        return VGroup(box, label, sub)

    # ─── Scene 1.1 — What is an LLM agent? ───────────────────────────────────

    def scene_1_1(self):
        box = RoundedRectangle(
            corner_radius=0.2,
            width=3.2,
            height=2.8,
            color=WHITE,
            fill_color=DARK_GREY,
            fill_opacity=0.4,
        )
        label = Text("Agent", font_size=28, color=WHITE, weight=BOLD).next_to(
            box.get_top(), DOWN, buff=0.25
        )

        # Context window bars
        bars = VGroup(
            *[
                Rectangle(
                    width=2.4,
                    height=0.22,
                    fill_color=GREY_B,
                    fill_opacity=0.8,
                    stroke_width=0,
                )
                for _ in range(4)
            ]
        ).arrange(DOWN, buff=0.13).next_to(label, DOWN, buff=0.18)

        snippets = ["system: you are an AI…", "user: help me with…", "assistant: sure!", "…"]
        bar_texts = VGroup(
            *[
                Text(s, font_size=9, color=DARK_GREY).move_to(bars[i])
                for i, s in enumerate(snippets)
            ]
        )

        agent = VGroup(box, label, bars, bar_texts)

        cap1 = self.make_caption("An AI agent reads text in, writes text out")

        self.play(Create(box), Write(label), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.2), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(t) for t in bar_texts], lag_ratio=0.2), run_time=0.5)
        self.play(FadeIn(cap1))
        self.wait(1.0)

        # Input / output arrows
        in_arr = Arrow(LEFT * 5.8, box.get_left(), color=WHITE, buff=0.05, stroke_width=3)
        out_arr = Arrow(box.get_right(), RIGHT * 5.8, color=WHITE, buff=0.05, stroke_width=3)
        in_lbl = Text("Input (prompt)", font_size=17, color=YELLOW).next_to(in_arr, UP, buff=0.1)
        out_lbl = Text("Output (response)", font_size=17, color=YELLOW).next_to(
            out_arr, UP, buff=0.1
        )

        self.play(GrowArrow(in_arr), FadeIn(in_lbl), run_time=0.8)
        self.play(GrowArrow(out_arr), FadeIn(out_lbl), run_time=0.8)
        self.wait(1.5)

        cap2 = self.make_caption("But what if the task is too big for one agent?")
        self.swap_caption(cap1, cap2)
        self.wait(2.0)

        self.play(
            FadeOut(agent),
            FadeOut(in_arr),
            FadeOut(in_lbl),
            FadeOut(out_arr),
            FadeOut(out_lbl),
            FadeOut(cap2),
            run_time=1.0,
        )

    # ─── Scene 1.2 — The task arrives ────────────────────────────────────────

    def scene_1_2(self):
        box = RoundedRectangle(
            corner_radius=0.2,
            width=3.2,
            height=2.8,
            color=WHITE,
            fill_color=DARK_GREY,
            fill_opacity=0.4,
        )
        label = Text("Agent", font_size=28, color=WHITE, weight=BOLD).next_to(
            box.get_top(), DOWN, buff=0.25
        )
        agent = VGroup(box, label)
        self.play(FadeIn(agent), run_time=0.7)

        # Task bubble — starts off-screen left, drifts in
        task_str = (
            "Research advertising strategies\n"
            "for our website, estimate CR,\n"
            "calculate CAC and ROI for each type"
        )
        bub_bg = RoundedRectangle(
            corner_radius=0.3,
            width=4.6,
            height=1.9,
            fill_color="#1e1e2e",
            fill_opacity=1,
            stroke_color=YELLOW,
            stroke_width=2.5,
        )
        bub_text = Text(task_str, font_size=14, color=WHITE, line_spacing=1.3).move_to(bub_bg)
        bubble = VGroup(bub_bg, bub_text).move_to(LEFT * 7.8 + UP * 0.6)

        self.add(bubble)
        self.play(
            bubble.animate.move_to(LEFT * 3.6 + UP * 0.6),
            rate_func=smooth,
            run_time=1.4,
        )
        self.wait(0.6)

        # Agent strains — question mark + wobble
        qmark = Text("?", font_size=56, color=RED_C, weight=BOLD).next_to(box, UP, buff=0.05)
        self.play(FadeIn(qmark, shift=UP * 0.2), run_time=0.3)
        self.play(Wiggle(agent, scale_value=1.08, rotation_angle=0.04, n_wiggles=5, run_time=1.5))

        cap = self.make_caption("This needs marketing knowledge AND mathematical expertise")
        self.play(FadeIn(cap), run_time=0.5)
        self.wait(2.0)

        self.play(
            FadeOut(agent),
            FadeOut(bubble),
            FadeOut(qmark),
            FadeOut(cap),
            run_time=0.9,
        )

    # ─── Scene 1.3 — Introducing the cast ────────────────────────────────────

    def scene_1_3(self):
        coord = self.make_agent_box(
            "Coordinator", BLUE, "Manages the overall task"
        ).move_to(LEFT * 3.5)
        social = self.make_agent_box(
            "Social Media\nExpert", PURPLE, "Advertising strategies & CR"
        ).move_to(RIGHT * 2.5 + UP * 1.5)
        math = self.make_agent_box(
            "Mathematician", ORANGE, "Calculates CAC and ROI"
        ).move_to(RIGHT * 2.5 + DOWN * 1.5)

        cap1 = self.make_caption(
            "We split the work across specialized agents — but how do they communicate?"
        )

        self.play(FadeIn(coord), run_time=0.8)
        self.play(FadeIn(social), run_time=0.7)
        self.play(FadeIn(math), run_time=0.7)
        self.play(FadeIn(cap1), run_time=0.5)
        self.wait(2.5)

        # Vertical dotted divider
        divider = DashedLine(
            UP * 3.9, DOWN * 3.9, color=GREY_B, dash_length=0.22, dashed_ratio=0.5
        )
        lbl_left = Text("Strategy 1:\nSubagents as Tools", font_size=20, color=WHITE).move_to(
            LEFT * 3.2 + UP * 3.2
        )
        lbl_right = Text("Strategy 2:\nHandoff", font_size=20, color=WHITE).move_to(
            RIGHT * 3.2 + UP * 3.2
        )

        self.play(Create(divider), FadeIn(lbl_left), FadeIn(lbl_right), run_time=1.0)
        self.wait(1.0)

        # Dim right side; left side stays bright — Act 2 begins on the left
        self.play(
            social.animate.set_opacity(0.25),
            math.animate.set_opacity(0.25),
            lbl_right.animate.set_opacity(0.25),
            run_time=1.0,
        )
        self.wait(1.5)
        self.play(FadeOut(cap1), run_time=0.5)
        self.wait(0.5)
