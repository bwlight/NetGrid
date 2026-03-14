“Coding Bible — Tactical AI System”

🧠 TACTICAL AI BIBLE
“The complete ruleset governing Cyberkin decision‑making, threat evaluation, personality, and adaptive combat behavior.”
⭐ I. Purpose of the Tactical AI System
The Tactical AI governs how enemy Cyberkin:

choose abilities

evaluate threats

react to statuses

adapt to player behavior

use synergy

respond to corruption

coordinate in multi‑enemy encounters

This system ensures battles feel alive, reactive, and strategic, not random.

⭐ II. Core Principles of Netgrid AI
The AI is built on four pillars:

1. Role‑Driven Behavior
Every Cyberkin has a combat role that shapes its priorities.

2. Personality Modifiers
Personalities influence risk tolerance, aggression, and unpredictability.

3. Threat Evaluation
AI constantly evaluates which target is the biggest threat.

4. Memory System
AI remembers past turns and adapts accordingly.

These four layers combine into a single decision score.

⭐ III. AI Decision Formula (Canonical)
Every ability is scored using:

Decision Score
=
(
𝑅
+
𝑃
+
𝑇
+
𝑀
+
𝑆
+
𝐶
)
Where:

R = Role priority

P = Personality modifier

T = Threat evaluation

M = Memory bias

S = Status/terrain context

C = Corruption influence

The AI selects the ability with the highest score.

⭐ IV. Combat Roles (Canonical Set)
Each Cyberkin has one primary role:

1. Aggressor
Prioritizes damage

Targets lowest‑defense enemies

Loves multi‑hit and high‑power moves

2. Defender
Protects allies

Uses shields, taunts, and purify

Targets enemies threatening allies

3. Support
Heals, buffs, cleanses

Avoids risky moves

Prioritizes ally survival

4. Disruptor
Applies debuffs, DOTs, control

Targets high‑speed or high‑damage enemies

5. Specialist
Uses unique mechanics (glyphs, illusions, clones)

Prioritizes synergy and terrain

6. Corrupted
Behavior becomes unstable

May ignore optimal choices

May self‑damage or mutate abilities

⭐ V. Personality System
Personalities modify decision‑making:

1. Brave
+10% aggression
+5% risk tolerance
Ignores low HP warnings

2. Cautious
+20% defensive choices
Avoids low‑accuracy moves
Prioritizes survival

3. Chaotic
Random +/– modifiers
May choose suboptimal moves
High synergy with Corrupt

4. Neutral
Balanced behavior
No strong biases

Personalities stack with roles to create unique AI profiles.

⭐ VI. Threat Evaluation System
AI evaluates each enemy Cyberkin using:

Threat Score
=
(
𝐷
+
𝑆
+
𝐻
+
𝐸
)
Where:

D = Damage output

S = Speed

H = Healing/support potential

E = Elemental advantage

The AI targets:

highest threat

OR lowest HP (if Aggressor)

OR ally‑threatening enemies (if Defender)

⭐ VII. Memory System
AI remembers:

last ability used

last target

last status applied

player patterns

terrain changes

corruption anomalies

Memory influences decisions:

avoids repeating ineffective moves

prioritizes finishing weakened targets

adapts to player strategies over time

Memory lasts 3 turns by default.

⭐ VIII. Status & Terrain Awareness
AI considers:

current statuses

enemy statuses

terrain effects

synergy opportunities

Examples:

If Dream Fog is active → use illusion abilities

If enemy is Burned → use multi‑hit Pulse moves

If Corrupt Zone is active → corruption abilities gain priority

⭐ IX. Corruption Influence System
Corruption modifies AI behavior based on corruption_level (0–100):

0–20: Stable
AI behaves normally.

21–50: Distorted
+10% aggression

+10% chance to ignore optimal move

+5% chance to mutate ability choice

51–80: Unstable
+25% aggression

+20% chance to self‑damage

+20% chance to override cooldown

+15% chance to target random enemy

81–100: Broken
Ignores roles

Ignores personality

Ignores threat evaluation

Chooses moves based on corruption tags

May attack allies

May skip turn

May trigger recursion loops

This is the only AI state that can break rules.

⭐ X. Ability Scoring Breakdown
Each ability receives scores based on:

1. Role Fit
Does this ability match the Cyberkin’s role?

2. Personality Fit
Does this ability match the Cyberkin’s personality?

3. Threat Impact
Does this ability meaningfully reduce enemy threat?

4. Status Impact
Does it apply or cleanse important statuses?

5. Terrain Impact
Does it create or benefit from terrain?

6. Synergy Potential
Does it combo with ally abilities?

7. Corruption Potential
Does it mutate or spread corruption?

⭐ XI. Multi‑Enemy Coordination
AI can coordinate when multiple enemies are present:

Defenders protect Aggressors

Supports heal priority allies

Disruptors target the same enemy to stack debuffs

Specialists set up terrain for the team

This creates team‑based strategy, not isolated behavior.

⭐ XII. Boss AI Enhancements
Bosses have:

multi‑phase behavior

scripted triggers

corruption surges

terrain dominance

ultimate abilities

adaptive resistances

Boss AI uses a weighted decision tree instead of the standard scoring system.

⭐ XIII. AI Hooks in the Battle Engine
The AI listens to:

on_turn_start

on_turn_end

on_status_apply

on_status_expire

on_damage_taken

on_ally_faint

on_enemy_faint

on_corruption_trigger

These hooks allow dynamic adaptation.

⭐ XIV. File Structure
AI files live in:

Code
/core/systems/ai/
    ai_controller.py
    role_profiles.json
    personality_profiles.json
    corruption_profiles.json
⭐ XV. Future‑Proofing Hooks
The AI system supports:

multi‑Cyberkin parties

bond‑based synergy

emotional states (Dream expansion)

memory persistence across battles

corruption evolution

boss‑tier scripting

faction‑based AI behavior

🧠 Tactical AI Bible is complete.