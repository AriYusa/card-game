from manim import *


class Act2SubagentsAsTools(Scene):
    def construct(self):
        self.scene_2_1()
        self.wait(0.5)
        self.scene_2_2()
        self.wait(0.5)
        self.scene_2_3()
        self.wait(0.5)
        self.scene_2_4()
        self.wait(0.5)
        self.scene_2_5()
        self.wait(0.5)
        self.scene_2_6()

    # ─── helpers ──────────────────────────────────────────────────────────────

    def make_caption(self, text, font_size=20):
        return Text(text, font_size=font_size, color=WHITE).to_edge(DOWN, buff=0.35)

    def swap_caption(self, old, new, run_time=0.7):
        self.play(ReplacementTransform(old, new), run_time=run_time)

    def make_coord_box(self, width=3.0, height=3.2):
        box = RoundedRectangle(
            corner_radius=0.2, width=width, height=height,
            color=BLUE, fill_color=BLUE, fill_opacity=0.15, stroke_width=2.5,
        )
        label = Text("Coordinator", font_size=18, color=BLUE, weight=BOLD).next_to(
            box.get_top(), DOWN, buff=0.22
        )
        bars = VGroup(*[
            Rectangle(
                width=width - 0.6, height=0.28,
                fill_color=GREY_B, fill_opacity=0.6, stroke_width=0,
            )
            for _ in range(4)
        ]).arrange(DOWN, buff=0.1).next_to(label, DOWN, buff=0.15)
        return VGroup(box, label, bars)

    def make_pool(self, name, color, n=3):
        """Stack of n slightly offset rounded rectangles to suggest a pool of agents."""
        figures = VGroup()
        for i in range(n):
            fig = RoundedRectangle(
                corner_radius=0.18, width=2.2, height=1.5,
                color=color, fill_color=color, fill_opacity=0.12, stroke_width=2,
            ).shift(RIGHT * i * 0.09 + UP * i * 0.09)
            figures.add(fig)
        label = Text(name, font_size=14, color=color, weight=BOLD).next_to(
            figures, UP, buff=0.12
        )
        gear = Text("⚙", font_size=18, color=color).next_to(label, RIGHT, buff=0.1)
        return VGroup(figures, label, gear)

    def make_tool_bubble(self, text, width=4.2):
        bg = RoundedRectangle(
            corner_radius=0.18, width=width, height=0.75,
            fill_color="#1a3a1a", fill_opacity=1,
            stroke_color=GREEN, stroke_width=2,
        )
        t = Text(text, font_size=9, color=GREEN).move_to(bg)
        return VGroup(bg, t)

    def make_result_bubble(self, text):
        bg = RoundedRectangle(
            corner_radius=0.18, width=4.0, height=0.6,
            fill_color="#0d1b2a", fill_opacity=1,
            stroke_color=TEAL, stroke_width=2,
        )
        t = Text(text, font_size=9, color=TEAL).move_to(bg)
        return VGroup(bg, t)

    def make_mini_context(self, lines, color=WHITE, width=3.2):
        row_h = 0.36
        bg = RoundedRectangle(
            corner_radius=0.15, width=width, height=len(lines) * row_h + 0.3,
            fill_color=DARKER_GREY, fill_opacity=0.95,
            stroke_color=color, stroke_width=1.5,
        )
        texts = VGroup(*[
            Text(line, font_size=9, color=GREY_A).move_to(
                bg.get_top() + DOWN * (0.26 + i * row_h)
            ).align_to(bg.get_left() + RIGHT * 0.12, LEFT)
            for i, line in enumerate(lines)
        ])
        return VGroup(bg, texts)

    # ─── Scene 2.1 — Architecture overview ────────────────────────────────────

    def scene_2_1(self):
        title = Text("ACT 2: Subagents as Tools", font_size=26, color=BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(FadeIn(title), run_time=0.8)
        self.wait(0.4)

        coord = self.make_coord_box().move_to(LEFT * 3.8)
        social_pool = self.make_pool("Social Media\nExperts", PURPLE).move_to(RIGHT * 2.8 + UP * 1.6)
        math_pool   = self.make_pool("Mathematicians", ORANGE).move_to(RIGHT * 2.8 + DOWN * 1.6)

        self.play(FadeIn(coord), run_time=0.8)
        self.play(FadeIn(social_pool), run_time=0.7)
        self.play(FadeIn(math_pool), run_time=0.7)

        arr_social = Arrow(
            coord.get_right(), social_pool[0][0].get_left(),
            color=GREEN, buff=0.15, stroke_width=2.5,
        )
        arr_math = Arrow(
            coord.get_right(), math_pool[0][0].get_left(),
            color=GREEN, buff=0.15, stroke_width=2.5,
        )
        lbl_s = Text("tool call", font_size=12, color=GREEN).next_to(arr_social, UP, buff=0.06)
        lbl_m = Text("tool call", font_size=12, color=GREEN).next_to(arr_math, DOWN, buff=0.06)

        self.play(GrowArrow(arr_social), FadeIn(lbl_s), run_time=0.6)
        self.play(GrowArrow(arr_math),   FadeIn(lbl_m), run_time=0.6)

        cap = self.make_caption(
            "The Coordinator treats subagents like tools — like pressing a button to get a result"
        )
        self.play(FadeIn(cap))
        self.wait(2.5)

        self.play(
            FadeOut(VGroup(coord, social_pool, math_pool,
                           arr_social, arr_math, lbl_s, lbl_m, cap, title)),
            run_time=0.8,
        )

    # ─── Scene 2.2 — Coordinator's context window zooms in ────────────────────

    def scene_2_2(self):
        coord = self.make_coord_box(width=3.4, height=3.5).move_to(LEFT * 3.5)
        self.play(FadeIn(coord), run_time=0.6)

        cap = self.make_caption("The Coordinator sees the task and knows which tools it can call")
        self.play(FadeIn(cap))

        bar_data = [
            ("System: you are a coordinator agent...", BLUE_D),
            ("User: Research advertising strategies,\nestimate CR, calculate CAC and ROI...", YELLOW_D),
            ("Tools: ask_social_expert(...),\nask_mathematician(...)", GREEN_D),
            ("Conversation so far: [empty]", GREY_B),
        ]
        bars = coord[2]
        bar_labels = VGroup()

        for i, (text, color) in enumerate(bar_data):
            self.play(bars[i].animate.set_fill(color, opacity=0.75), run_time=0.3)
            t = Text(text, font_size=8, color=WHITE).move_to(bars[i])
            self.play(FadeIn(t), run_time=0.3)
            bar_labels.add(t)
            self.wait(0.5)

        self.wait(1.5)
        self.play(FadeOut(VGroup(coord, bar_labels, cap)), run_time=0.7)

    # ─── Scene 2.3 — First tool call: Social Media Expert ─────────────────────

    def scene_2_3(self):
        coord = self.make_coord_box().move_to(LEFT * 4.2)
        social_pool = self.make_pool("Social Media\nExperts", PURPLE).move_to(RIGHT * 2.8 + UP * 1.5)

        self.play(FadeIn(coord), FadeIn(social_pool), run_time=0.7)

        bubble = self.make_tool_bubble(
            'ask_social_expert("Research advertising strategies\nand estimate conversion rates for each")',
            width=5.2,
        ).move_to(coord.get_right() + RIGHT * 0.5 + UP * 1.5)

        self.play(FadeIn(bubble, scale=0.85), run_time=0.5)
        self.play(
            bubble.animate.move_to(social_pool[0][0].get_center()),
            run_time=1.2, rate_func=smooth,
        )
        self.play(FadeOut(bubble), run_time=0.3)

        # Front figure lights up
        front = social_pool[0][2]
        self.play(
            front.animate.set_fill(PURPLE, opacity=0.55).set_stroke(PURPLE_A, width=3),
            run_time=0.4,
        )

        # Fresh empty context window
        ctx = self.make_mini_context(
            [
                "System: you are a social media expert...",
                "User: Research advertising strategies",
                "      and estimate conversion rates",
            ],
            color=PURPLE,
        ).next_to(social_pool, RIGHT, buff=0.3)

        cap = self.make_caption(
            "The subagent wakes up with no memory. It only sees this one question."
        )
        self.play(FadeIn(ctx), FadeIn(cap), run_time=0.6)
        self.wait(2.0)

        # Search tool animates briefly
        search = Text("\U0001f50d", font_size=22).next_to(ctx, DOWN, buff=0.2)
        self.play(FadeIn(search, shift=UP * 0.15), run_time=0.4)
        self.wait(0.4)
        self.play(FadeOut(search), run_time=0.3)

        # Result bubble travels back to coordinator
        result = self.make_result_bubble("SEO: CR 3%  |  Paid Social: CR 5%  |  Email: CR 8%")
        result.move_to(social_pool[0][0].get_center())
        self.play(FadeIn(result, scale=0.85), run_time=0.4)
        self.play(
            result.animate.move_to(coord.get_right() + RIGHT * 1.0 + UP * 0.5),
            run_time=1.0,
        )

        # Expert fades — it's done
        self.play(FadeOut(social_pool), FadeOut(ctx), run_time=0.6)
        self.play(FadeOut(result), run_time=0.3)

        # Coordinator bar 4 updates
        bars = coord[2]
        self.play(bars[3].animate.set_fill(TEAL_D, opacity=0.75), run_time=0.4)
        bar_txt = Text(
            "Tool result: SEO 3%, Paid Social 5%, Email 8%", font_size=8, color=WHITE
        ).move_to(bars[3])
        self.play(FadeIn(bar_txt), run_time=0.3)

        self.play(FadeOut(cap), run_time=0.4)
        self.wait(0.5)
        self.play(FadeOut(VGroup(coord, bar_txt)), run_time=0.6)

    # ─── Scene 2.4 — Second tool call: Mathematician ──────────────────────────

    def scene_2_4(self):
        coord = self.make_coord_box().move_to(LEFT * 4.2)
        math_pool = self.make_pool("Mathematicians", ORANGE).move_to(RIGHT * 2.8 + DOWN * 1.2)

        self.play(FadeIn(coord), FadeIn(math_pool), run_time=0.7)

        bubble = self.make_tool_bubble(
            'ask_mathematician("Calculate CAC and ROI for:\nSEO CR 3%, Paid Social CR 5%, Email CR 8%")',
            width=5.2,
        ).move_to(coord.get_right() + RIGHT * 0.5 + DOWN * 1.2)

        self.play(FadeIn(bubble, scale=0.85), run_time=0.5)
        self.play(
            bubble.animate.move_to(math_pool[0][0].get_center()),
            run_time=1.2, rate_func=smooth,
        )
        self.play(FadeOut(bubble), run_time=0.3)

        front = math_pool[0][2]
        self.play(
            front.animate.set_fill(ORANGE, opacity=0.55).set_stroke(ORANGE, width=3),
            run_time=0.4,
        )

        ctx = self.make_mini_context(
            [
                "System: you are a mathematician...",
                "User: Calculate CAC and ROI for",
                "      SEO CR 3%...",
            ],
            color=ORANGE,
        ).next_to(math_pool, RIGHT, buff=0.3)

        cap = self.make_caption(
            "Again — a brand new instance. No knowledge of the Social Media Expert's process."
        )
        self.play(FadeIn(ctx), FadeIn(cap), run_time=0.6)
        self.wait(2.5)

        result = self.make_result_bubble(
            "SEO CAC $48 ROI 120%  |  Social CAC $32 ROI 180%  |  Email CAC $15 ROI 310%"
        )
        result.move_to(math_pool[0][0].get_center())
        self.play(FadeIn(result, scale=0.85), run_time=0.4)
        self.play(
            result.animate.move_to(coord.get_right() + RIGHT * 1.0 + DOWN * 0.5),
            run_time=1.0,
        )

        self.play(FadeOut(math_pool), FadeOut(ctx), run_time=0.6)
        self.play(FadeOut(result), run_time=0.3)

        self.play(FadeOut(cap), run_time=0.4)
        self.wait(0.3)
        self.play(FadeOut(coord), run_time=0.6)

    # ─── Scene 2.5 — Coordinator assembles the answer ─────────────────────────

    def scene_2_5(self):
        coord = self.make_coord_box(width=3.6, height=3.8).move_to(ORIGIN)
        self.play(FadeIn(coord), run_time=0.6)

        bar_data = [
            ("User: Research advertising strategies...", YELLOW_D),
            ("Tool call 1: ask_social_expert(...)", GREEN_D),
            ("Result 1: SEO 3%  Paid 5%  Email 8%", TEAL_D),
            ("Tool call 2 + Result 2: CAC & ROI done", ORANGE),
        ]
        bars = coord[2]
        bar_labels = VGroup()

        for i, (text, color) in enumerate(bar_data):
            self.play(bars[i].animate.set_fill(color, opacity=0.75), run_time=0.25)
            t = Text(text, font_size=8, color=WHITE).move_to(bars[i])
            self.play(FadeIn(t), run_time=0.25)
            bar_labels.add(t)

        self.wait(0.8)

        # Final answer exits left to user
        final_bg = RoundedRectangle(
            corner_radius=0.15, width=3.6, height=1.0,
            fill_color="#0a0a18", fill_opacity=1,
            stroke_color=WHITE, stroke_width=2,
        ).move_to(LEFT * 5.2)
        final_txt = Text(
            "Final report:\nstrategies + CAC & ROI for each",
            font_size=11, color=WHITE,
        ).move_to(final_bg)
        final_grp = VGroup(final_bg, final_txt)

        arr = Arrow(coord.get_left(), final_bg.get_right(), color=WHITE, buff=0.1, stroke_width=2.5)
        self.play(GrowArrow(arr), run_time=0.6)
        self.play(FadeIn(final_grp), run_time=0.5)

        cap = self.make_caption(
            "The Coordinator holds all the memory. Subagents are stateless — each one forgets everything when it's done."
        )
        self.play(FadeIn(cap))
        self.wait(3.0)

        self.play(FadeOut(VGroup(coord, bar_labels, arr, final_grp, cap)), run_time=0.8)

    # ─── Scene 2.6 — "Team of strangers" summary visual ───────────────────────

    def scene_2_6(self):

        # Summary box
        summary_bg = RoundedRectangle(
            corner_radius=0.2, width=7.0, height=3.0,
            fill_color=DARKER_GREY, fill_opacity=0.95,
            stroke_color=BLUE, stroke_width=2,
        ).move_to(UP * 0.8)
        box_title = Text("Subagents as Tools", font_size=18, color=BLUE, weight=BOLD).next_to(
            summary_bg.get_top(), DOWN, buff=0.25
        )
        items = VGroup(
            Text("✅ Simple and predictable", font_size=14, color=GREEN),
            Text("✅ Easy to run calls in parallel", font_size=14, color=GREEN),
            Text("⚠️  Subagents cannot build on each other's work directly", font_size=14, color=YELLOW),
            Text("⚠️  Coordinator must pass all relevant context manually", font_size=14, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(box_title, DOWN, buff=0.22)

        summary = VGroup(summary_bg, box_title, items)

        cap2 = self.make_caption("Strategy summary")
        self.swap_caption(cap, cap2)
        self.play(FadeIn(summary, shift=UP * 0.15), run_time=0.8)
        self.wait(4.0)

        self.play(FadeOut(VGroup(summary, cap2)), run_time=1.0)
