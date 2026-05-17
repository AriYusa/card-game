# Manim Animation Storyboard: Multi-Agent Communication Strategies

## Technical Notes for the Coding Agent

**Manim objects:**
- `RoundedRectangle` for agent boxes and context windows
- `VGroup` of small flat rectangles for context window "bars"
- `Text` + `FadeIn` / `Write` for labels and captions
- `Arrow` / `DoubleArrow` — single-headed for Tools strategy, double-headed for Handoff
- `CurvedArrow` for the scroll traveling between agents
- Stick figures via `SVGMobject` or `Circle` + `Line` composites; offset copies using `.shift()` for the pool effect
- `ScrollingText` or stacked `VGroup` bars with color fills for the layered context window
- `SurroundingRectangle` with color highlight for specific context layers

**Color scheme:**
- Coordinator: `BLUE`
- Social Media Agent: `PURPLE`
- Mathematician: `ORANGE`
- Context window background: `GREY_A`
- Tool call bubbles: `GREEN`
- Handoff transfer: `YELLOW` / `GOLD`
- Context layers in Handoff: tinted fills matching the agent who wrote them

**Pacing:** ~2 seconds per caption, `FadeTransform` or `ReplacementTransform` between scenes, smooth `MoveAlongPath` for the traveling scroll in Act 3

## Overall Structure
Three acts, ~3-4 minutes total. Narration-style pacing. Each scene fades or transitions cleanly.

---

## ACT 1: Setting the Stage (~60 seconds)

### Scene 1.1 — What is an LLM agent?
- A single rectangle appears in the center, labeled **"Agent"**
- Inside it: a small scrolling list of text representing a context window
- Caption: *"An AI agent reads text in, writes text out"*
- Arrow enters from left: **"Input (prompt)"** → box → **"Output (response)"** exits right
- Brief pause. Then caption: *"But what if the task is too big for one agent?"*

### Scene 1.2 — The task arrives
- A message bubble drifts in from the left, containing the task:
  > *"Research different advertising strategies for our website, estimate the potential Conversion Rate and calculate Customer Acquisition Cost and Return on Investment for each type"*
- The single Agent box looks at it, then visually "strains" — a question mark appears, it wobbles slightly
- Caption: *"This needs marketing knowledge AND mathematical Agentise"*

### Scene 1.3 — Introducing the cast
- Three boxes appear:
  - **Coordinator** (blue, center-left) — *"Manages the overall task"*
  - **Social Media Agent** (purple, top-right) — *"Knows advertising strategies and conversion rates"*
  - **Mathematician** (orange, bottom-right) — *"Calculates CAC and ROI"*

---

## ACT 2: Subagents as Tools (~80 seconds)

### Scene 2.1 — Coordinator's context window zooms in
- Start from the exact way Scene 1.3 ended
- Coordinator box becomes bigger and the Tools box as well. Names of subagents appear in the Coordinator's tool list like `call_social_agent(...)`, `call_mathematician(...)`

### Scene 2.2 — First tool call: Social Media Agent
- Coordinator generates a glowing green tool call bubble:
  `call_social_agent("Research advertising strategies and estimate conversion rates for each")`
- Bubble travels right toward the Social Media Agent group
- Social Media Agent works (add a loading sign indicator near it). With small arrows (if possible, curved) going between Social Media Agent's "LLM" and "Tools" boxes, show that some interanl process is going inside the Social Media Agent
- Returns a result bubble: *"SEO: CR 3%, Paid Social: CR 5%, Email: CR 8%"*

### Scene 2.3 — Second tool call: Mathematician (not as detailed as Social Media Agent)
- Coordinator's context window updates — box "LLM" now has new box with the received result
- Coordinator generates second tool call:
  `ask_mathematician("Calculate CAC and ROI for: SEO CR 3%, Paid Social CR 5%, Email CR 8%")`
- Bubble travels to Mathematician group
- Similar to 2.2 some internal process if going
- Mathematician returns a structured result bubble (add a small mock)

 "How should the Coordinator's expansion in Scene 2.1 look? (It currently ends Act 1 as a compact box with LLM+Tools sub-bars in blue.)"="Hybrid", 
 
 "When a subagent works (Social Media Agent in 2.2, Mathematician in 2.3), how should the 'internal processing' look?"="Pulse + curved arrows only", 

 "How should the Coordinator's context grow between tool calls in 2.3? (Storyboard: 'context window updates — LLM box now has new box with the received result')"="Stack + final summary",
 
  "For the result bubble texts: should I use exact storyboard mocks or expand slightly for clarity?"="Shorter, punchier". You can now continue with the user's answers in mind.


## ACT 3: Handoff Strategy (~90 seconds)

### Scene 3.1 — Social Media Agent
- Exact state as Act 1.3 ended
- Caption: *"In the Handoff strategy, there is one instance of each agent — and any agent can pass control to any other, in any direction"*
- Coordinator agent expands, with both boxes. LLM box gets the same sub-boxes as the agent in Scene 1.2 (system prompt, tools, user prompt, selected tools — all in the Coordinator's color).
  Then copies the "user prompt" and "Coordinator transfers to Social Media Agent" boxes and passes them to the Social Media Expert. Social Media Expert also appears in expanded form with its own system prompt and own tools (in its own color); the "user query" and "Coordinator transfers to Social Media Agent" items from the Coordinator are placed in the Social Media Expert's LLM context. Coordinator shrinks to contracted form.
- Social Media Agent calls tools (arrows back and forth to Tools)

### Scene 3.2 — Mathematician
- As a result, Social Media Agent copies and moves to Mathematician: "user query", "Coordinator transfers to Social Media Agent", "Social Media Expert called tools", "Social Media Agent tool results", "Social Media Agent transfers to Mathematician". Social Media Agent shrinks to contracted form.
- Caption: *"Agents can hand off directly to each other — the Coordinator doesn't need to be in the loop"*
- Mathematician's context window unfolds with LLM box having:
  - its own system prompt and own tools (in its own color)
  - all items passed from Social Media Agent
- Caption: *"The Mathematician sees everything — the original task, the Coordinator's reasoning, and all of the Social Media Agent's research"*
- Mathematician uses tools.
- Then adds "Mathematician transfers to Coordinator"
- And transfers the relevant parts ("User query"
"Coordinator transfers to Social Media Agent"
"Social Media Expert called tools"
"Social Media Agent tool results"
"Social Media Agent transfers to Mathematician"
"Mathematician called tools"
"Mathematician tool results"
"Mathematician transfers to Coordinator") to the Coordinator

## ACT 4: Side-by-Side Comparison (~35 seconds)

### Scene 4.1 — Split screen topology
- Screen splits. Left: **Subagents as Tools**, Right: **Handoff**
- Left: **star topology** — all arrows point out from and back to Coordinator only
- Right: **mesh topology** — double-headed arrows between all three agents
- Caption: *"The key structural difference: who can talk to whom"*

### Scene 4.2 — Memory comparison
- Both sides show context windows simultaneously
- Left: each subagent window flashes in small and empty, then disappears (reset animation)
- Right: the single scroll grows and grows, accumulating colored layers
- Caption: *"In Tools, each subagent gets only what the Coordinator decides to tell it. In Handoff, every agent inherits the full story."*

### Scene 4.3 — Quality difference for our task
- Show two final answer boxes side by side
- Left (Tools): Coordinator assembled the answer from two separate results — correct but stitched together
- Right (Handoff): Mathematician read the Social Media Agent's full reasoning before calculating — the ROI numbers are grounded in the actual strategy details
- Caption: *"For tasks where understanding context matters — not just the numbers — Handoff produces richer results"*

### Scene 4.4 — When to use which
- Two columns:
  - 🔧 **Subagents as Tools**: independent tasks, parallel work, simple lookups, when you want predictability
  - 🔀 **Handoff**: sequential reasoning, tasks that build on each other, when agents need the full picture
- Final caption: *"Choose your strategy based on whether your agents need to remember each other"*

---
