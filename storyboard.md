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
- Social Media Expert: `PURPLE`
- Mathematician: `ORANGE`
- Context window background: `GREY_A`
- Tool call bubbles: `GREEN`
- Handoff transfer: `YELLOW` / `GOLD`
- Context layers in Handoff: tinted fills matching the agent who wrote them

**Pacing:** ~2 seconds per caption, `FadeTransform` or `ReplacementTransform` between scenes, smooth `MoveAlongPath` for the traveling scroll in Act 3

## Overall Structure
Three acts, ~3-4 minutes total. Narration-style pacing. Each scene fades or transitions cleanly.

---

## ACT 1: Setting the Stage (~45 seconds)

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
- Caption: *"This needs marketing knowledge AND mathematical expertise"*

### Scene 1.3 — Introducing the cast
- Three boxes appear:
  - **Coordinator** (blue, center-left) — *"Manages the overall task"*
  - **Social Media Expert** (purple, top-right) — *"Knows advertising strategies and conversion rates"*
  - **Mathematician** (orange, bottom-right) — *"Calculates CAC and ROI"*
- Caption: *"We split the work across specialized agents — but how do they communicate?"*
- Screen splits with a vertical dotted line
- Left label: **"Strategy 1: Subagents as Tools"**
- Right label: **"Strategy 2: Handoff"**
- Both sides fade to gray. Left side brightens. Begin Act 2.

---

## ACT 2: Subagents as Tools (~80 seconds)



### Scene 2.1 — Coordinator's context window zooms in
- Start from the exact way scene_1_3 ended
- Coordinator box become bigger and the tools box also. Names of subagents appear in coordinators tool lost like call_social_expert(...), call_mathematician(...)"

### Scene 2.3 — First tool call: Social Media Expert
- Coordinator generates a glowing green tool call bubble:
  `ask_social_expert("Research advertising strategies and estimate conversion rates for each")`
- Bubble travels right toward the Social Media Expert group
- Social Media Expert works (add like a loading sign near it), small arrows (if possible curmed abbed between Social Media Expert's "LLM" and "Tools" boxes)
- Returns a result bubble: *"SEO: CR 3%, Paid Social: CR 5%, Email: CR 8%"*

### Scene 2.4 — Second tool call: Mathematician (not so deteiled as Social Media Expert)
- Coordinator's context window updates — bar 4 now shows the received result
- Coordinator generates second tool call:
  `ask_mathematician("Calculate CAC and ROI for: SEO CR 3%, Paid Social CR 5%, Email CR 8%")`
- Bubble travels to Mathematician group
- Loading sign for 2 secs
- Mathematician returns structures result bubble (make some small mock)



## ACT 3: Handoff Strategy (~90 seconds)

### Scene 3.1 — Architecture overview
- New full screen scene
- Same three agents: **Coordinator** (blue, center), **Social Media Expert** (purple, top-right), **Mathematician** (orange, bottom-right)
- Draw **double-headed arrows** between all three pairs:
  - Coordinator ↔ Social Media Expert
  - Coordinator ↔ Mathematician
  - Social Media Expert ↔ Mathematician
- Each agent has only **one figure** — not a pool, not a team of strangers
- Caption: *"In the Handoff strategy, there is one instance of each agent — and any agent can pass control to any other, in any direction"*

### Scene 3.2 — The baton is the context
- A glowing scroll/document icon appears near the Coordinator
- Caption: *"Instead of passing a question and getting an answer back, agents pass the entire conversation history forward"*
- The scroll visually grows as it moves between agents
- Caption: *"Whoever holds the scroll is in control — and they can see everything that happened before"*

### Scene 3.3 — Coordinator starts
- Coordinator's context window shown filling:
  - *"Global system prompt"*
  - *"Social Media Expert-specific prompt"* ← will update per agent
  - *"User turn: Research advertising strategies, estimate CR, calculate CAC and ROI..."*
- Coordinator generates text, then calls: `transfer_to_agent('SocialMediaExpert')`
- Caption: *"The Coordinator doesn't ask for a result — it hands over control entirely"*

### Scene 3.4 — Context travels to Social Media Expert
- **Key animation**: Coordinator's context window "folds" into the scroll and travels to Social Media Expert
- Social Media Expert's context window unfolds. Show it filling with color-coded layers:
  - 🔵 *"Global system prompt"*
  - 🟣 *"Social Media Expert-specific prompt"*
  - 🔵 *"User turn: original task"*
  - 🔵 *"[CoordinatorAgent] said: ... and called transfer_to_agent('SocialMediaExpert')"* ← highlighted
- Caption: *"The Social Media Expert sees the original task AND what the Coordinator said and did"*

### Scene 3.5 — Social Media Expert works, then hands off directly to Mathematician
- Social Media Expert uses its own tools, adds results to context
- Then — **key moment** — it calls: `transfer_to_agent('Mathematician')` directly
- Bold highlighted arrow appears **directly between Social Media Expert and Mathematician**, bypassing Coordinator
- Caption: *"Agents can hand off directly to each other — the Coordinator doesn't need to be in the loop"*
- The scroll grows longer and travels to Mathematician

### Scene 3.6 — Mathematician receives the full history
- Mathematician's context window unfolds with **all three accumulated layers** visible and color-coded:
  - 🔵 Coordinator's messages
  - 🟣 Social Media Expert's messages, tool calls, and results — full detail
  - 🟠 Mathematician-specific prompt
- Caption: *"The Mathematician sees everything — the original task, the Coordinator's reasoning, and all of the Social Media Expert's research"*
- Emphasize: the Mathematician doesn't need to be told "SEO has 3% CR" — it can read the full reasoning behind that number
- Mathematician calculates CAC and ROI with full context, then calls: `transfer_to_agent('Coordinator')`

### Scene 3.7 — Coordinator receives the completed scroll
- Coordinator's context now contains the full history from all three agents
- Coordinator produces final answer → back to user
- Caption: *"The Coordinator now has a complete, integrated picture — and so did every agent along the way"*

### Scene 3.8 — Handoff summary
- Pull back, show the triangle of agents with the scroll visibly traveling between them, growing
- Arrows are bold and bidirectional, showing the mesh topology
- Summary box:
  - ✅ Agents build directly on each other's full work
  - ✅ Any agent can reach any other — flexible routing
  - ⚠️ Context window grows with each handoff
  - ⚠️ More complex to design and debug

---

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
- Right (Handoff): Mathematician read the Social Media Expert's full reasoning before calculating — the ROI numbers are grounded in the actual strategy details
- Caption: *"For tasks where understanding context matters — not just the numbers — Handoff produces richer results"*

### Scene 4.4 — When to use which
- Two columns:
  - 🔧 **Subagents as Tools**: independent tasks, parallel work, simple lookups, when you want predictability
  - 🔀 **Handoff**: sequential reasoning, tasks that build on each other, when agents need the full picture
- Final caption: *"Choose your strategy based on whether your agents need to remember each other"*

---
