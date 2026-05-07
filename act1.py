from manim import *


class Act1SettingTheStage(Scene):
    def construct(self):
        user, llm_box, llm_label = self.scene_1_1()
        self.wait(0.5)
        self.scene_1_2(user, llm_box, llm_label)
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

    def make_user_icon(self, color=BLUE_C):
        head = Circle(radius=0.25, color=color, fill_color=color, fill_opacity=0.9, stroke_width=2)
        body = RoundedRectangle(
            corner_radius=0.12, width=0.55, height=0.6,
            color=color, fill_color=color, fill_opacity=0.9, stroke_width=2,
        ).next_to(head, DOWN, buff=0.05)
        icon = VGroup(head, body)
        lbl = Text("User", font_size=16, color=color).next_to(icon, DOWN, buff=0.1)
        return VGroup(icon, lbl)

    # ─── Scene 1.1 — Simplest LLM-based agent ────────────────────────────────

    def scene_1_1(self):
        user = self.make_user_icon().move_to(LEFT * 4.8)

        llm_box = RoundedRectangle(
            corner_radius=0.2, width=3.2, height=2.4,
            color=BLUE, fill_color=DARK_GREY, fill_opacity=0.4, stroke_width=2.5,
        ).move_to(RIGHT * 1.0)
        llm_label = Text("LLM", font_size=26, color=BLUE, weight=BOLD).next_to(
            llm_box.get_top(), DOWN, buff=0.25
        )

        cap1 = self.make_caption("The simplest agent: user sends a prompt, LLM responds")
        self.play(FadeIn(user), FadeIn(VGroup(llm_box, llm_label)), run_time=0.8)
        self.play(FadeIn(cap1))
        self.wait(0.8)

        prompt_arr = Arrow(user.get_right(), llm_box.get_left(), color=YELLOW, buff=0.1, stroke_width=3)
        prompt_lbl = Text("Prompt", font_size=16, color=YELLOW).next_to(prompt_arr, UP, buff=0.1)
        resp_arr = Arrow(
            llm_box.get_left(), user.get_right(), color=GREEN_C, buff=0.1, stroke_width=3
        ).shift(DOWN * 0.4)
        resp_lbl = Text("Response", font_size=16, color=GREEN_C).next_to(resp_arr, DOWN, buff=0.1)

        self.play(GrowArrow(prompt_arr), FadeIn(prompt_lbl), run_time=0.7)
        self.play(GrowArrow(resp_arr), FadeIn(resp_lbl), run_time=0.7)
        self.wait(1.0)

        # Zoom into LLM internals
        cap2 = self.make_caption("Inside the LLM: system prompt + user prompt")
        self.swap_caption(cap1, cap2)

        large_box = RoundedRectangle(
            corner_radius=0.2, width=5.8, height=4.8,
            color=BLUE, fill_color=DARK_GREY, fill_opacity=0.4, stroke_width=2.5,
        ).move_to(RIGHT * 0.8)
        large_label = Text("LLM", font_size=26, color=BLUE, weight=BOLD).next_to(
            large_box.get_top(), DOWN, buff=0.25
        )

        self.play(
            Transform(llm_box, large_box),
            Transform(llm_label, large_label),
            FadeOut(prompt_arr), FadeOut(prompt_lbl),
            FadeOut(resp_arr), FadeOut(resp_lbl),
            user.animate.move_to(LEFT * 5.8),
            run_time=1.0,
        )

        # ── Round 1:──────────────────────
        c = large_box.get_center()
        user_query1_text = "When Klagenfurt became a city?"
        user_response1_text = "Around the late 12th and mid-13th century."

        sys_box = RoundedRectangle(
            corner_radius=0.1, width=4.8, height=0.65,
            fill_color="#1a3a5c", fill_opacity=1,
            stroke_color=BLUE_B, stroke_width=1.5,
        ).move_to(c + UP * 1.4)
        sys_lbl = Text("System Prompt", font_size=16, color=BLUE_C, weight=BOLD).move_to(sys_box)
        self.play(FadeIn(sys_box), FadeIn(sys_lbl), run_time=0.6)
        self.wait(1)
        
        usr_box = RoundedRectangle(
            corner_radius=0.1, width=4.8, height=0.65,
            fill_color="#1a3a2c", fill_opacity=1,
            stroke_color=GREEN_B, stroke_width=1.5,
        ).move_to(c + UP * 0.55)
        usr_lbl = Text(user_query1_text, font_size=16, color=GREEN_C, weight=BOLD).move_to(usr_box)

        p_arr = Arrow(
            user.get_right(), usr_box.get_left(),
            color=RED_B, buff=0, stroke_width=3,
        )
        q1_lbl = Text(user_query1_text, font_size=13, color=RED_B).next_to(
            p_arr, UP, buff=0.12
        )
        self.play(
            GrowArrow(p_arr), FadeIn(q1_lbl),
            run_time=0.5,
        )
        self.wait(1)
        # return prompt arrow to previous color
        self.play(
            p_arr.animate.set_color(GREEN_C),
            q1_lbl.animate.set_color(GREEN_C),
            run_time=0.5,
        )
        self.wait(0.3)

        # LLM box outline pulses red then returns to default
        self.play(FadeIn(usr_box), FadeIn(usr_lbl), run_time=0.6)
        self.wait(0.5)

        self.play(llm_box.animate.set_stroke(color=RED_C, width=3.5), run_time=0.4)
        self.wait(2)
        self.play(llm_box.animate.set_stroke(color=BLUE, width=2.5), run_time=0.4)
        self.wait(0.3)

        # Response arrow → red + user_response1_text, then returns to default
        r_arr = Arrow(
            llm_box.get_left() + DOWN * 0.6, user.get_right() + DOWN * 0.3,
            color=RED_B, buff=0.05, stroke_width=3,
        )
        
        r1_lbl = Text(user_response1_text, font_size=13, color=RED_B).next_to(r_arr, DOWN, buff=0.1)
        self.play(
            GrowArrow(r_arr), FadeIn(r1_lbl),
            run_time=0.5,
        )
        self.wait(1)
        self.play(
            r_arr.animate.set_color(GREEN_C),
            r1_lbl.animate.set_color(GREEN_C),
            run_time=0.5,
        )
        self.wait(0.4)

        # ── Round 2: history appears only NOW ───────────
        
        user_query2_text = "What about Vienna?"
        response2_text = "Vienna received city rights in 1221."

        self.play(
            FadeOut(p_arr, q1_lbl, r_arr, r1_lbl),
            run_time=0.5)

        # User Prompt fades out first to make room
        self.play(FadeOut(usr_box), FadeOut(usr_lbl), run_time=0.5)
        
        cap3 = self.make_caption("2nd turn: previous messages included as conversation history")
        self.swap_caption(cap2, cap3)
        
        # Conversation History appears where User Prompt was
        hist_box = RoundedRectangle(
            corner_radius=0.1, width=4.8, height=1.1,
            fill_color="#2a1a3c", fill_opacity=1,
            stroke_color=PURPLE_B, stroke_width=2,
        ).move_to(c + UP * 0.35)
        hist_title = Text("Conversation History", font_size=13, color=PURPLE_C, weight=BOLD).next_to(
            hist_box.get_top(), DOWN, buff=0.12
        )
        hist_q = Text(f"User: {user_query1_text}", font_size=10, color=GREY_A).next_to(
            hist_title, DOWN, buff=0.08
        )
        hist_a = Text(f"Assistant: {user_response1_text}", font_size=10, color=GREY_B).next_to(
            hist_q, DOWN, buff=0.06
        )
        self.play(
            FadeIn(hist_box), 
            FadeIn(VGroup(hist_title, hist_q, hist_a)), run_time=0.7)

        # User Prompt reappears below Conversation History
        new_usr_box = RoundedRectangle(
            corner_radius=0.1, width=4.8, height=0.65,
            fill_color="#1a3a2c", fill_opacity=1,
            stroke_color=GREEN_B, stroke_width=1.5,
        ).move_to(c + DOWN * 0.65)
        new_usr_lbl = Text(f"User Prompt: {user_query2_text}", font_size=16, color=GREEN_C, weight=BOLD).move_to(new_usr_box)
        
        p_arr1 = Arrow(
            user.get_right(), new_usr_box.get_left(),
            color=RED_B, buff=0, stroke_width=3,
        )
        q2_lbl = Text(user_query2_text, font_size=13, color=RED_B).next_to(p_arr1, UP, buff=0.12)
        self.play(
            GrowArrow(p_arr1), FadeIn(q2_lbl),
            run_time=0.5,
        )
        self.wait(0.5)

        self.play(
            FadeIn(new_usr_box), 
            FadeIn(new_usr_lbl),
        )
        self.play(hist_box.animate.set_stroke(color=YELLOW, width=3), run_time=0.4)
        self.play(Indicate(hist_box, color=YELLOW, scale_factor=1.03), run_time=1.0)
        self.wait(5.0)

        # make llm box red to indicate it's "thinking" about the new prompt + history
        self.play(llm_box.animate.set_stroke(color=RED_C, width=3.5), run_time=0.4)
        self.wait(2.0)

        # Response arrow → red + response2_text, then returns to default
        r_arr2 = Arrow(
            llm_box.get_left() + DOWN * 0.6, user.get_right() + DOWN * 0.6,
            color=RED_B, buff=0.05, stroke_width=3,
        )
        r2_lbl = Text(response2_text, font_size=13, color=RED_B).next_to(r_arr2, DOWN, buff=0.1)
        self.play(
            GrowArrow(r_arr2), FadeIn(r2_lbl),
            run_time=0.5,
        )
        self.wait(1)

        # Fade out only the content inside the box and the arrows/caption.
        # The user icon and LLM box itself persist into scene 1.2.
        self.play(
            FadeOut(VGroup(
                sys_box, sys_lbl, new_usr_box, new_usr_lbl,
                p_arr1, q2_lbl, r_arr2, r2_lbl,
                hist_box, hist_title, hist_q, hist_a, cap3,
            )),
            run_time=0.8,
        )

        # Resize LLM box and move user to match the scene 1.2 layout.
        target_box = RoundedRectangle(
            corner_radius=0.2, width=3.0, height=3.2,
            color=BLUE, fill_color=DARK_GREY, fill_opacity=0.4, stroke_width=2.5,
        ).move_to(LEFT * 0.5)
        target_label = Text("LLM", font_size=24, color=BLUE, weight=BOLD).next_to(
            target_box.get_top(), DOWN, buff=0.2
        )
        self.play(
            Transform(llm_box, target_box),
            Transform(llm_label, target_label),
            user.animate.move_to(LEFT * 5.5),
            run_time=0.8,
        )
        return user, llm_box, llm_label

    # ─── Scene 1.2 — LLM-based agent with tools ──────────────────────────────

    def scene_1_2(self, user=None, llm_box=None, llm_label=None):
        is_continuation = user is not None

        if not is_continuation:
            user = self.make_user_icon().move_to(LEFT * 5.5)
            llm_box = RoundedRectangle(
                corner_radius=0.2, width=3.0, height=3.2,
                color=BLUE, fill_color=DARK_GREY, fill_opacity=0.4, stroke_width=2.5,
            ).move_to(LEFT * 0.5)
            llm_label = Text("LLM", font_size=24, color=BLUE, weight=BOLD).next_to(
                llm_box.get_top(), DOWN, buff=0.2
            )

        tools_box = RoundedRectangle(
            corner_radius=0.2, width=3.0, height=3.2,
            color=ORANGE, fill_color=DARK_GREY, fill_opacity=0.4, stroke_width=2.5,
        ).move_to(RIGHT * 4.0)
        tools_header = Text("⚙  Tools", font_size=20, color=ORANGE, weight=BOLD).next_to(
            tools_box.get_top(), DOWN, buff=0.25
        )
        tool_items = VGroup(
            Text("Web Search", font_size=14, color=WHITE),
            Text("Edit File", font_size=14, color=WHITE),
            Text("Calculate", font_size=14, color=WHITE),
        ).arrange(DOWN, buff=0.22).next_to(tools_header, DOWN, buff=0.25)
        tools_grp = VGroup(tools_box, tools_header, tool_items)
        
        # agent box - rectangle that includes both the LLM and the tools, to show they're part of the same agent
        agent_box = RoundedRectangle(
            corner_radius=0.3, width=8.0, height=4.0,
            color=GREY_B, fill_color=GREY_B, fill_opacity=0.1, stroke_width=2,
        ).move_to(RIGHT * 1.75)
        agent_lbl = Text("Agent", font_size=22, color=GREY_B, weight=BOLD).next_to(
            agent_box.get_top(), DOWN, buff=0.2
        )
        self.play(FadeIn(VGroup(agent_box, agent_lbl)), run_time=0.8)

        cap1 = self.make_caption("An LLM agent can call tools to act on the world")
        if not is_continuation:
            self.play(FadeIn(user), FadeIn(VGroup(llm_box, llm_label)), run_time=0.8)
        self.play(FadeIn(tools_grp), run_time=0.8)
        self.play(FadeIn(cap1))
        self.wait(1.0)

        # Tool descriptions injected into LLM context
        cap2 = self.make_caption("Tool descriptions are injected after the system prompt")
        self.swap_caption(cap1, cap2)

        c = llm_box.get_center()
        sys_bar = RoundedRectangle(
            corner_radius=0.08, width=2.4, height=0.42,
            fill_color="#1a3a5c", fill_opacity=1, stroke_color=BLUE_B, stroke_width=1,
        ).move_to(c + UP * 0.9)
        sys_lbl = Text("System Prompt", font_size=11, color=BLUE_C).move_to(sys_bar)

        tool_bar = RoundedRectangle(
            corner_radius=0.08, width=2.4, height=0.42,
            fill_color="#2a2500", fill_opacity=1, stroke_color=ORANGE, stroke_width=1.8,
        ).move_to(c + UP * 0.35)
        tool_bar_lbl = Text("Tool Descriptions", font_size=11, color=ORANGE).move_to(tool_bar)

        usr_bar = RoundedRectangle(
            corner_radius=0.08, width=2.4, height=0.42,
            fill_color="#1a3a2c", fill_opacity=1, stroke_color=GREEN_B, stroke_width=1,
        ).move_to(c + DOWN * 0.2)
        usr_lbl = Text("User Prompt", font_size=11, color=GREEN_C).move_to(usr_bar)

        self.play(FadeIn(sys_bar), FadeIn(sys_lbl), run_time=0.4)
        self.play(FadeIn(tool_bar), FadeIn(tool_bar_lbl), run_time=0.5)
        self.play(FadeIn(usr_bar), FadeIn(usr_lbl), run_time=0.4)

        inject_line = DashedLine(
            tools_box.get_left() + UP * 0.35,
            tool_bar.get_right(),
            color=ORANGE, dash_length=0.15, dashed_ratio=0.55, stroke_width=2,
        )
        self.play(Create(inject_line), run_time=0.7)
        self.play(Indicate(tool_bar, color=YELLOW, scale_factor=1.05), run_time=0.8)
        self.wait(1.0)

        # User → LLM
        cap3 = self.make_caption("LLM selects a tool instead of responding directly")
        self.swap_caption(cap2, cap3)

        prompt_arr = Arrow(user.get_right(), llm_box.get_left(), color=YELLOW, buff=0.1, stroke_width=2.5)
        prompt_lbl = Text("Prompt", font_size=13, color=YELLOW).next_to(prompt_arr, UP, buff=0.08)
        self.play(GrowArrow(prompt_arr), FadeIn(prompt_lbl), run_time=0.6)
        self.wait(0.4)

        # LLM → tools (tool call)
        tool_call_arr = Arrow(
            llm_box.get_right(), tools_box.get_left(),
            color=RED_C, buff=0.1, stroke_width=2.5,
        )
        tool_call_lbl = Text("Tool Call", font_size=13, color=RED_C).next_to(tool_call_arr, UP, buff=0.08)
        self.play(GrowArrow(tool_call_arr), FadeIn(tool_call_lbl), run_time=0.7)
        self.wait(0.5)

        # Tools → LLM (result)
        cap4 = self.make_caption("Tool result returns to LLM, which responds to the user")
        self.swap_caption(cap3, cap4)

        result_arr = Arrow(
            tools_box.get_left(), llm_box.get_right(),
            color=GREEN_C, buff=0.1, stroke_width=2.5,
        ).shift(DOWN * 0.45)
        result_lbl = Text("Tool Result", font_size=13, color=GREEN_C).next_to(result_arr, DOWN, buff=0.08)
        self.play(GrowArrow(result_arr), FadeIn(result_lbl), run_time=0.7)
        self.wait(0.4)

        # LLM → user (final response)
        resp_arr = Arrow(
            llm_box.get_left(), user.get_right(),
            color=GREEN_B, buff=0.1, stroke_width=2.5,
        ).shift(DOWN * 0.45)
        resp_lbl = Text("Response", font_size=13, color=GREEN_B).next_to(resp_arr, DOWN, buff=0.08)
        self.play(GrowArrow(resp_arr), FadeIn(resp_lbl), run_time=0.7)
        self.wait(2.0)

        self.play(
            FadeOut(VGroup(
                agent_box, agent_lbl,
                user, llm_box, llm_label, tools_grp,
                sys_bar, sys_lbl, tool_bar, tool_bar_lbl, usr_bar, usr_lbl,
                inject_line,
                prompt_arr, prompt_lbl,
                tool_call_arr, tool_call_lbl,
                result_arr, result_lbl,
                resp_arr, resp_lbl, cap4,
            )),
            run_time=1.0,
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


# to do 1.2
# add boxes to llm: "Selected tool and arguments", then arrow to tools, arrow from tools, added box "Tool Result", add 3 dots under the box, and redrew a few times arroeto tolls and back (showing tools can be called sever times untill llm decides to respond to user)