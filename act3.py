from manim import *

from shared import (
    expanded_agent_targets,
    fly_copy_bars,
    llm_stack_positions,
    make_agent_box,
    make_caption,
    pulse_subagent,
    swap_caption,
    tinted_bar,
)


COORD = BLUE
SOCIAL = PURPLE
MATH = ORANGE

COORD_POS = LEFT * 3.5
SOCIAL_POS = RIGHT * 2.5 + UP * 1.9
MATH_POS = RIGHT * 2.5 + DOWN * 1.9

COMPACT_W = 2.5
COMPACT_H = 2.0
EXP_W = 4.5
EXP_H = 3.4

BAR_W = 1.9
BAR_H = 0.28


def compact(name, color):
    return make_agent_box(name, color, width=COMPACT_W, height=COMPACT_H)


class Act3HandoffStrategy(Scene):
    def construct(self):
        coord = compact("Coordinator Agent", COORD).move_to(COORD_POS)
        social = compact("Social Media Agent", SOCIAL).move_to(SOCIAL_POS)
        math_a = compact("Mathematician", MATH).move_to(MATH_POS)

        self.add(coord, social, math_a)
        self.wait(0.4)

        state = {"coord": coord, "social": social, "math": math_a}
        self.scene_3_1(state)
        self.scene_3_2(state)

    # ─── Scene 3.1 — Coord expands, hands off to Social ──────────────────────

    def scene_3_1(self, state):
        coord, social = state["coord"], state["social"]

        cap = make_caption(
            "Strategy 2: Handoff — any agent can pass control to any other"
        )
        self.play(FadeIn(cap), run_time=0.6)
        self.wait(0.6)

        # Expand Coordinator in place
        coord_exp = expanded_agent_targets(
            "Coordinator Agent", COORD, COORD_POS, width=EXP_W, height=EXP_H
        )
        self.play(
            *[Transform(coord[i], coord_exp[i]) for i in range(6)],
            run_time=0.8,
        )
        self.wait(0.2)

        llm_box = coord[2]
        tools_box = coord[4]

        coord_tool_items = VGroup(
            Text("call_social_agent(...)", font_size=9, color=SOCIAL, weight=BOLD, font="Monospace"),
            Text("ask_mathematician(...)", font_size=9, color=MATH, weight=BOLD, font="Monospace"),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        coord_tool_items.move_to(tools_box.get_center() + DOWN * 0.15)
        self.play(FadeIn(coord_tool_items, shift=UP * 0.08), run_time=0.6)

        slots = llm_stack_positions(llm_box, 6, top_buff=0.45)

        sys_bar = tinted_bar("System Prompt", COORD, width=BAR_W, height=BAR_H).move_to(slots[0])
        tools_bar = tinted_bar("Tools: call_* / ask_*", COORD, width=BAR_W, height=BAR_H).move_to(slots[1])
        user_bar = tinted_bar("User Query: ad strategies + ROI", COORD, width=BAR_W, height=BAR_H, font_size=8).move_to(slots[2])

        self.play(FadeIn(sys_bar), run_time=0.35)
        self.play(FadeIn(tools_bar), run_time=0.35)
        self.play(FadeIn(user_bar), run_time=0.35)
        self.wait(0.5)

        cap2 = make_caption(
            "Coordinator reasons, then chooses to transfer to the Social Media Agent"
        )
        swap_caption(self, cap, cap2)

        pulse_subagent(self, coord, COORD, repeats=1, run_time=0.30)

        self.play(Indicate(coord_tool_items[0], color=SOCIAL, scale_factor=1.2), run_time=0.6)

        handoff_bar = tinted_bar(
            "→ Social Media Agent", COORD, width=BAR_W, height=BAR_H, weight=BOLD
        ).move_to(slots[3])
        self.play(FadeIn(handoff_bar, shift=DOWN * 0.1), run_time=0.45)
        self.wait(0.3)

        state["coord_stack"] = {
            "sys": sys_bar,
            "tools": tools_bar,
            "user": user_bar,
            "handoff_to_social": handoff_bar,
            "tool_items": coord_tool_items,
        }

        # Expand Social, then fly transferred bars into its stack
        cap3 = make_caption("Social Media Agent receives the query plus a handoff record")
        swap_caption(self, cap2, cap3)

        social_exp = expanded_agent_targets(
            "Social Media Agent", SOCIAL, SOCIAL_POS, width=EXP_W, height=EXP_H
        )
        self.play(
            *[Transform(social[i], social_exp[i]) for i in range(6)],
            run_time=0.8,
        )

        social_llm = social[2]
        social_tools = social[4]
        social_tool_items = VGroup(
            Text("web_search(...)", font_size=9, color=SOCIAL, weight=BOLD, font="Monospace"),
            Text("ask_mathematician(...)", font_size=9, color=MATH, weight=BOLD, font="Monospace"),
            Text("call_coordinator(...)", font_size=9, color=COORD, weight=BOLD, font="Monospace"),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        social_tool_items.move_to(social_tools.get_center() + DOWN * 0.10)
        self.play(FadeIn(social_tool_items, shift=UP * 0.08), run_time=0.5)

        social_slots = llm_stack_positions(social_llm, 6, top_buff=0.45)

        social_sys = tinted_bar("System Prompt", SOCIAL, width=BAR_W, height=BAR_H).move_to(social_slots[0])
        social_tools_bar = tinted_bar("Tools: search + call/ask", SOCIAL, width=BAR_W, height=BAR_H, font_size=8).move_to(social_slots[1])
        self.play(FadeIn(social_sys), FadeIn(social_tools_bar), run_time=0.5)

        landed = fly_copy_bars(
            self,
            [user_bar, handoff_bar],
            [social_slots[2], social_slots[3]],
            run_time=1.0,
            arc=PI / 4,
        )
        social_user_copy, social_handoff_copy = landed

        self.play(
            Indicate(social_user_copy, color=COORD, scale_factor=1.06),
            Indicate(social_handoff_copy, color=COORD, scale_factor=1.06),
            run_time=0.6,
        )
        self.wait(0.3)

        # Coord shrinks back to compact form
        coord_compact = compact("Coordinator Agent", COORD).move_to(COORD_POS)
        self.play(
            *[Transform(coord[i], coord_compact[i]) for i in range(6)],
            FadeOut(sys_bar),
            FadeOut(tools_bar),
            FadeOut(user_bar),
            FadeOut(handoff_bar),
            FadeOut(coord_tool_items),
            run_time=0.7,
        )

        # Social does tool work
        cap4 = make_caption("Social Media Agent runs its own tool loop")
        swap_caption(self, cap3, cap4)

        pulse_subagent(self, social, SOCIAL, repeats=2, run_time=0.30)

        social_tool_work = tinted_bar(
            "• search → channel data", SOCIAL, width=BAR_W, height=0.22, font_size=8
        ).move_to(social_slots[4])
        self.play(FadeIn(social_tool_work, shift=DOWN * 0.08), run_time=0.45)
        self.wait(0.4)

        self.play(FadeOut(cap4), run_time=0.3)

        state["social_stack"] = {
            "sys": social_sys,
            "tools": social_tools_bar,
            "user": social_user_copy,
            "from_coord": social_handoff_copy,
            "tool_work": social_tool_work,
            "tool_items": social_tool_items,
        }
        state["social_slots"] = social_slots

    # ─── Scene 3.2 — Social → Math, then Math → Coord with full stack ────────

    def scene_3_2(self, state):
        coord, social, math_a = state["coord"], state["social"], state["math"]
        social_stack = state["social_stack"]
        social_slots = state["social_slots"]

        cap = make_caption(
            "Agents hand off directly — the Coordinator stays out of the loop"
        )
        self.play(FadeIn(cap), run_time=0.5)

        # Social emits its handoff bar
        self.play(Indicate(social_stack["tool_items"][1], color=MATH, scale_factor=1.2), run_time=0.5)

        social_to_math = tinted_bar(
            "→ Mathematician", SOCIAL, width=BAR_W, height=BAR_H, weight=BOLD
        ).move_to(social_slots[5])
        self.play(FadeIn(social_to_math, shift=DOWN * 0.1), run_time=0.45)
        social_stack["to_math"] = social_to_math
        self.wait(0.3)

        # Expand Math
        math_exp = expanded_agent_targets(
            "Mathematician", MATH, MATH_POS, width=EXP_W, height=EXP_H
        )
        self.play(
            *[Transform(math_a[i], math_exp[i]) for i in range(6)],
            run_time=0.8,
        )

        math_llm = math_a[2]
        math_tools = math_a[4]
        math_tool_items = VGroup(
            Text("calculator(...)", font_size=9, color=MATH, weight=BOLD, font="Monospace"),
            Text("call_coordinator(...)", font_size=9, color=COORD, weight=BOLD, font="Monospace"),
            Text("call_social_agent(...)", font_size=9, color=SOCIAL, weight=BOLD, font="Monospace"),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        math_tool_items.move_to(math_tools.get_center() + DOWN * 0.10)
        self.play(FadeIn(math_tool_items, shift=UP * 0.08), run_time=0.5)

        math_slots = llm_stack_positions(math_llm, 8, top_buff=0.32, slot_height=0.27)

        math_sys = tinted_bar("System Prompt", MATH, width=BAR_W, height=0.24, font_size=9).move_to(math_slots[0])
        math_tools_bar = tinted_bar("Tools: calc + call_*", MATH, width=BAR_W, height=0.24, font_size=8).move_to(math_slots[1])
        self.play(FadeIn(math_sys), FadeIn(math_tools_bar), run_time=0.5)

        cap2 = make_caption(
            "Mathematician inherits every layer — original task, handoffs, all prior tool work"
        )
        swap_caption(self, cap, cap2)

        # All 4 of Social's inherited/produced items fly to Math, preserving origin tints
        sources = [
            social_stack["user"],
            social_stack["from_coord"],
            social_stack["tool_work"],
            social_stack["to_math"],
        ]
        targets = [math_slots[2], math_slots[3], math_slots[4], math_slots[5]]
        landed = fly_copy_bars(self, sources, targets, run_time=1.2, arc=PI / 4)
        math_user, math_from_coord, math_soc_work, math_from_social = landed
        self.wait(0.4)

        # Social shrinks back to compact
        social_compact = compact("Social Media Agent", SOCIAL).move_to(SOCIAL_POS)
        self.play(
            *[Transform(social[i], social_compact[i]) for i in range(6)],
            FadeOut(social_stack["sys"]),
            FadeOut(social_stack["tools"]),
            FadeOut(social_stack["user"]),
            FadeOut(social_stack["from_coord"]),
            FadeOut(social_stack["tool_work"]),
            FadeOut(social_stack["to_math"]),
            FadeOut(social_stack["tool_items"]),
            run_time=0.7,
        )

        # Math does tool work
        cap3 = make_caption("Mathematician computes CAC + ROI on top of the full context")
        swap_caption(self, cap2, cap3)
        pulse_subagent(self, math_a, MATH, repeats=2, run_time=0.30)

        math_tool_work = tinted_bar(
            "• calc → CAC + ROI", MATH, width=BAR_W, height=0.20, font_size=8
        ).move_to(math_slots[6])
        self.play(FadeIn(math_tool_work, shift=DOWN * 0.08), run_time=0.45)
        self.wait(0.4)

        math_to_coord = tinted_bar(
            "→ Coordinator", MATH, width=BAR_W, height=0.24, font_size=9, weight=BOLD
        ).move_to(math_slots[7])
        self.play(Indicate(math_tool_items[1], color=COORD, scale_factor=1.2), run_time=0.5)
        self.play(FadeIn(math_to_coord, shift=DOWN * 0.1), run_time=0.45)
        self.wait(0.3)

        # Re-expand Coord with the full inherited stack as the final payoff
        cap4 = make_caption("Coordinator receives the full story — every layer in its origin color")
        swap_caption(self, cap3, cap4)

        coord_exp = expanded_agent_targets(
            "Coordinator Agent", COORD, COORD_POS, width=EXP_W, height=EXP_H
        )
        self.play(
            *[Transform(coord[i], coord_exp[i]) for i in range(6)],
            run_time=0.8,
        )

        coord_llm = coord[2]
        coord_tools = coord[4]
        final_tool_items = VGroup(
            Text("call_social_agent(...)", font_size=9, color=SOCIAL, weight=BOLD, font="Monospace"),
            Text("ask_mathematician(...)", font_size=9, color=MATH, weight=BOLD, font="Monospace"),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        final_tool_items.move_to(coord_tools.get_center() + DOWN * 0.15)
        self.play(FadeIn(final_tool_items), run_time=0.4)

        # Final Coord stack: 7 slots — sys, tools, user, →social, • soc-work, → math, • math-work.
        # The "→ Coordinator" record is implicit (we're here), so it doesn't get its own slot.
        coord_slots = llm_stack_positions(coord_llm, 7, top_buff=0.32, slot_height=0.27)
        final_sys = tinted_bar("System Prompt", COORD, width=BAR_W, height=0.24, font_size=9).move_to(coord_slots[0])
        final_tools = tinted_bar("Tools: call_* / ask_*", COORD, width=BAR_W, height=0.24, font_size=8).move_to(coord_slots[1])
        self.play(FadeIn(final_sys), FadeIn(final_tools), run_time=0.4)

        # Fly Math's stack back to Coord. Chronological order; math_to_coord is consumed (not re-shown).
        return_sources = [
            math_user,          # original user query (blue)
            math_from_coord,    # → Social (blue handoff record)
            math_soc_work,      # • Social tool work (purple)
            math_from_social,   # → Math (purple handoff record)
            math_tool_work,     # • Math tool work (orange)
        ]
        return_targets = [
            coord_slots[2],
            coord_slots[3],
            coord_slots[4],
            coord_slots[5],
            coord_slots[6],
        ]
        landed_back = fly_copy_bars(
            self, return_sources, return_targets, run_time=1.4, arc=-PI / 4
        )
        self.wait(0.5)

        # Math shrinks back to compact
        math_compact = compact("Mathematician", MATH).move_to(MATH_POS)
        self.play(
            *[Transform(math_a[i], math_compact[i]) for i in range(6)],
            FadeOut(math_sys),
            FadeOut(math_tools_bar),
            FadeOut(math_user),
            FadeOut(math_from_coord),
            FadeOut(math_soc_work),
            FadeOut(math_from_social),
            FadeOut(math_tool_work),
            FadeOut(math_to_coord),
            FadeOut(math_tool_items),
            run_time=0.7,
        )

        # Final emphasis: pulse the multi-colored stack
        self.play(
            *[Indicate(b, scale_factor=1.04) for b in landed_back],
            run_time=0.9,
        )
        self.wait(2.0)
