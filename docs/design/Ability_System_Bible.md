🧩 ABILITY SYSTEM BIBLE
“The complete ruleset governing every ability in Netgrid.”
⭐ I. Purpose of the Ability System
The Ability System defines how Cyberkin interact with the world and each other.
It governs:

damage

healing

buffs & debuffs

status application

corruption anomalies

targeting

cooldowns

combo chains

synergy triggers

Abilities are the core verbs of Netgrid’s combat and exploration.

⭐ II. Ability Schema (Final Canon Version)
This is the authoritative schema every ability file must follow.

Code
{
  "id": "string",                     // short, unique ID (e.g., 'pulse_strike')
  "name": "string",                   // display name
  "type": "string",                   // Offense, Support, Utility, Special
  "element": "string",                // Sector element (Root, Pulse, Void, etc.)
  "power": "number|null",             // base damage (null for non-damage abilities)
  "accuracy": "number|null",          // 0–100 (null for guaranteed effects)
  "cost": "number",                   // energy cost
  "cooldown": "number",               // turns before reuse
  "target": "string",                 // single, multi, self, random, area
  "priority": "number",               // turn order modifier
  "effects": [                        // list of status or secondary effects
    {
      "status": "string",
      "chance": "number",             // 0–100
      "duration": "number|null",
      "potency": "number|null"
    }
  ],
  "scaling": {                        // stat-based scaling
    "attack": "number",
    "magic": "number",
    "speed": "number"
  },
  "description": "string",            // in-game text
  "tags": ["string"]                  // combo, synergy, corruption, etc.
}
This schema is locked and should not change unless the engine evolves.

⭐ III. Ability Categories (Canonical)
Every ability belongs to one of these categories:

1. Offense
Direct damage, multi-hit, piercing, corruption damage, etc.

2. Support
Healing, shields, buffs, cleansing, protection.

3. Utility
Movement, repositioning, escape, scouting, terrain manipulation.

4. Special
Unique mechanics, corruption anomalies, evolution triggers, story abilities.

⭐ IV. Elemental Alignment
Abilities inherit the element of their Sector:

Sector	Element Theme	Ability Flavor
Root	Life, growth	healing, vines, regeneration
Firewall	Protection, flame	shields, purify, burn
Pulse	Speed, rhythm	multi-hit, tempo, electric
Dream	Emotion, illusion	confusion, charm, mirage
Archive	Memory, crystal	glyphs, data, recall
Cloud	Air, drift	evasion, clones, wind
Echo	Resonance	soundwaves, duplicates
Void	Entropy	silence, decay
Corrupt	Viral glitch	mutation, red-static
⭐ V. Damage Formula (Final Version)
The standard damage formula is:

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

S = scaling from stats

M = elemental multiplier

R = random variance (0.90–1.10)

Scaling is calculated as:

𝑆
=
(
𝐴
×
𝑎
)
+
(
𝑀
×
𝑚
)
+
(
𝑆
𝑝
×
𝑠
)
Where:

A = Attack stat

M = Magic stat

Sp = Speed stat

a, m, s = scaling coefficients from the ability file

⭐ VI. Accuracy & Evasion Rules
Accuracy check:

Hit Chance
=
Accuracy
−
Target Evasion
Minimum hit chance is 10%, maximum is 95%, unless:

ability is tagged guaranteed_hit

target is under blind or fog status

corruption anomalies override accuracy

⭐ VII. Cooldowns & Costs
Cooldown Rules
Cooldowns begin after the ability is used.

Cooldowns tick down at the end of the user’s turn.

Abilities with cooldown 0 are spammable unless tagged otherwise.

Energy Cost Rules
Energy regenerates each turn (base 10%).

Cloud and Pulse Cyberkin regenerate faster.

Corrupt abilities cost more but hit harder.

⭐ VIII. Targeting Rules
Valid targeting modes:

self

single_enemy

multi_enemy

random_enemy

all_enemies

single_ally

multi_ally

all_allies

area (affects terrain)

global (rare, story abilities)

⭐ IX. Secondary Effects
Secondary effects include:

status application

stat buffs/debuffs

terrain changes

combo triggers

corruption anomalies

echo‑clones

dream illusions

archive glyph marks

Each effect has:

chance

duration

potency

tags

⭐ X. Synergy System (Optional but Supported)
Abilities can synergize when:

two abilities share a tag

two Cyberkin share a bond

terrain matches the ability element

corruption anomalies trigger mutations

Examples:

Pulse + Echo = multi‑hit resonance chain

Root + Cloud = healing mist

Void + Corrupt = entropy rupture

⭐ XI. Corruption Anomalies
Corrupt abilities can:

mutate mid‑battle

change power

change target

self‑damage

spread corruption to terrain

override accuracy

override cooldowns

These are controlled by the corruption_level variable.

⭐ XII. Ability Tags (Canonical List)
Tags define behavior:

combo

multi_hit

piercing

healing

shield

cleanse

corruption

illusion

glyph

wind

resonance

entropy

viral

dream

echo_clone

area

global

priority

finisher

⭐ XIII. Universal Abilities (Core Set)
These are abilities every Cyberkin family can access:

Basic Strike

Guard

Focus

Charge

Clean Hit

Quick Step

Recover

Analyze

⭐ XIV. Ability File Structure
All abilities are stored in:

Code
/data/abilities/
    basic/
    advanced/
    disruptor/
    support/
    signature

Each file is named:

Code
<id>.json

⭐ XV. Validation Rules
IDs must be unique

Power must be null for non‑damage abilities

Accuracy must be null for guaranteed abilities

Effects must match the Status Bible

Tags must be from the canonical list

Element must match a Sector

🧩 Ability System Bible is complete.