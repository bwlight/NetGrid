⚔️ BATTLE ENGINE BIBLE
“The complete ruleset governing turn order, action flow, damage, AI hooks, and combat logic in Netgrid.”
⭐ I. Purpose of the Battle Engine
The Battle Engine is the central orchestrator of all combat interactions.
It governs:

turn order

action resolution

damage calculation

status resolution

cooldowns

terrain effects

synergy triggers

corruption anomalies

AI decision-making

logging & debugging

It ensures every battle is fair, predictable, strategic, and fun.

⭐ II. Core Components of the Battle Engine
The engine is composed of modular subsystems:

1. Turn Manager
Controls turn order, priority, and action queue.

2. Ability Resolver
Executes abilities, calculates damage, applies effects.

3. Status Engine
Handles DOTs, HOTs, buffs, debuffs, control effects, and terrain.

4. Cooldown Manager
Tracks ability cooldowns and energy regeneration.

5. AI Controller
Makes decisions for enemy Cyberkin.

6. Battle Manager
Top‑level orchestrator that coordinates all subsystems.

Each module is independent and upgradeable.

⭐ III. Turn Order System
Turn order is determined by:

Turn Priority
=
Speed
+
Ability Priority
Rules:

Higher priority acts first.

Ties are broken by raw Speed.

If still tied, random 50/50.

Statuses like Stun override priority.

Corruption anomalies may reorder turns.

⭐ IV. Action Flow (Canonical Sequence)
Every turn follows this exact order:

1. Start‑of‑Turn Status Resolution
DOTs

HOTs

buffs/debuffs

corruption mutations

terrain effects

2. Action Selection
Player chooses ability

AI chooses ability

Priority determines order

3. Ability Execution
Accuracy check

Damage calculation

Secondary effects

Status application

Terrain changes

Synergy triggers

4. On‑Action Status Hooks
Echo resonance

Dream illusions

Corruption recursion

Glyph marks

5. End‑of‑Turn Status Resolution
DOTs

HOTs

lingering effects

6. Cooldown & Duration Reduction
Cooldowns tick down

Status durations decrease

7. Victory Check
If all enemies faint → win

If all allies faint → loss

This sequence is canon and must not change.

⭐ V. Damage Calculation
The engine uses the Ability Bible’s formula:

Damage
=
(
𝑃
×
𝑆
)
×
𝑀
×
𝑅
Where:

P = base power

S = stat scaling

M = elemental multiplier

R = random variance (0.90–1.10)

Elemental Multipliers
Strong: ×1.5

Weak: ×0.5

Neutral: ×1.0

Immune: ×0.0

Void and Corrupt have special rules:

Void ignores illusions

Corrupt may override multipliers

⭐ VI. Accuracy & Evasion
Accuracy check:

Hit Chance
=
Accuracy
−
Target Evasion
Rules:

Minimum hit chance: 10%

Maximum hit chance: 95%

Guaranteed hit abilities bypass the check

Dream Fog reduces accuracy

Cloud Drift increases evasion

Corruption anomalies may force a miss or force a hit

⭐ VII. Status Resolution Engine
Statuses resolve in this order:

Start‑of‑turn

On‑action

End‑of‑turn

Duration reduction

Expiration hooks

The Status Engine handles:

DOT/HOT

buffs/debuffs

control effects

terrain

illusions

glyphs

corruption mutations

⭐ VIII. Terrain System
Only one terrain can be active at a time.

Examples:

Rootfield → healing vines

Firewall Dome → purification

Pulse Circuit → speed boost

Dream Fog → illusion chance

Archive Crystal Field → glyph amplification

Cloud Drift → evasion boost

Echo Chamber → resonance loops

Void Silence → no healing

Corrupt Zone → mutation chance

Terrain lasts:

a fixed number of turns

or until overwritten

⭐ IX. Cooldown & Energy System
Cooldown Rules
Cooldowns start after use

Tick down at end of user’s turn

Cannot go below 0

Energy Rules
Base regen: 10% per turn

Cloud & Pulse regen faster

Corrupt abilities cost more

⭐ X. Synergy System
Synergies occur when:

two abilities share a tag

two Cyberkin share a bond

terrain matches ability element

statuses interact

corruption anomalies trigger

Examples:

Pulse + Echo → resonance chain

Root + Cloud → healing mist

Void + Corrupt → entropy rupture

Synergies are optional but supported.

⭐ XI. Corruption Anomalies
Corruption can:

mutate abilities

reorder turn order

override accuracy

override cooldowns

spread to terrain

cause recursion loops

apply random statuses

increase or decrease power

Corruption level ranges from 0–100.

At high levels, corruption becomes unpredictable.

⭐ XII. AI Integration Hooks
The Battle Engine exposes hooks for the AI:

on_turn_start

on_turn_end

on_status_apply

on_status_expire

on_damage_taken

on_ally_faint

on_enemy_faint

on_corruption_trigger

These allow the AI to react dynamically.

⭐ XIII. Logging & Debugging
Every action is logged:

ability used

damage dealt

statuses applied

terrain changes

corruption anomalies

AI decisions

Logs can be toggled:

silent

minimal

verbose

debug

⭐ XIV. Battle File Structure
Battle engine files live in:

Code
/core/systems/battle/
    battle_manager.py
    turn_manager.py
    ability_resolver.py
    status_engine.py
    cooldown_manager.py
    ai_controller.py
Each module is independent and replaceable.

⭐ XV. Future‑Proofing Hooks
The engine supports:

multi‑Cyberkin parties

tag‑based synergy expansions

corruption evolution

terrain stacking (future)

combo chains

ultimate abilities

boss‑tier mechanics

⚔️ Battle Engine Bible is complete.