🧬 CYBERKIN DATA ARCHITECTURE BIBLE
“The complete ruleset governing Cyberkin data, evolution, stats, personalities, roles, and engine integration.”

⭐ I. Purpose of the Cyberkin Architecture
Cyberkin are the living entities of Netgrid.
Their data architecture defines:

identity

stats

growth

evolution

abilities

roles

personalities

elemental alignment

corruption behavior

synergy hooks

This system ensures every Cyberkin is consistent, balanced, and engine‑ready.

⭐ II. Cyberkin Schema (Final Canon Version)
json
{
  "id": "string",
  "name": "string",
  "family": "string",
  "stage": "string",
  "element": "string",
  "role": "string",
  "personality": "string",
  "stats": {
    "hp": "number",
    "attack": "number",
    "defense": "number",
    "magic": "number",
    "speed": "number"
  },
  "growth": {
    "hp": "number",
    "attack": "number",
    "defense": "number",
    "magic": "number",
    "speed": "number"
  },
  "abilities": {
    "baby": ["string"],
    "rookie": ["string"],
    "champion": ["string"],
    "final": ["string"]
  },
  "evolution": {
    "next": "string|null",
    "requirements": {
      "level": "number|null",
      "bond": "number|null",
      "item": "string|null",
      "sector": "string|null",
      "special": "string|null"
    }
  },
  "resistances": {
    "root": "number",
    "firewall": "number",
    "pulse": "number",
    "dream": "number",
    "archive": "number",
    "cloud": "number",
    "echo": "number",
    "void": "number",
    "corrupt": "number"
  },
  "lore": "string",
  "tags": ["string"]
}
This schema is locked and should not change unless the engine evolves.

⭐ III. Cyberkin Stages (Canonical)
1. Baby
Starter form

Low stats

Learns basic abilities

High bonding potential

2. Rookie
First evolution

Gains identity

Learns family‑themed abilities

3. Champion
Mid‑tier evolution

Strong stats

Learns signature family abilities

4. Final
Fully evolved

High stats

Learns signature ultimate ability

Gains full role identity

⭐ IV. Stat System
Cyberkin have five core stats:

HP

Attack

Defense

Magic

Speed

Base Stats
Defined in the stats block.

Growth Stats
Define how much each stat increases per level.

Final Stat Formula
𝐹
𝑖
𝑛
𝑎
𝑙
 
𝑆
𝑡
𝑎
𝑡
=
𝐵
𝑎
𝑠
𝑒
+
(
𝐺
𝑟
𝑜
𝑤
𝑡
ℎ
×
𝐿
𝑒
𝑣
𝑒
𝑙
)
⭐ V. Elemental Alignment
Each Cyberkin belongs to one Sector:

Root • Firewall • Pulse • Dream • Archive • Cloud • Echo • Void • Corrupt

Element determines:

resistances

weaknesses

ability access

synergy

terrain interaction

⭐ VI. Resistances & Weaknesses
Each Cyberkin has a resistance table:

1.5 = strong

1.0 = neutral

0.5 = weak

0.0 = immune

Special rules:

Void ignores illusions

Corrupt may override resistances

⭐ VII. Ability Progression
Abilities are grouped by stage:

json
"abilities": {
  "baby": [...],
  "rookie": [...],
  "champion": [...],
  "final": [...]
}
Rules:

Baby abilities are universal or simple

Rookie abilities introduce family identity

Champion abilities define combat role

Final abilities include signature moves

⭐ VIII. Evolution System
Evolution is defined by:

level

bond

item

sector

special condition

Examples:

Root → bond‑based

Pulse → speed or combo‑based

Dream → emotional resonance

Archive → memory or glyph count

Void → entropy threshold

Corrupt → corruption level

Evolution is not always linear — some families branch.

⭐ IX. Personality System
Personalities modify:

AI behavior

stat growth

bonding

corruption resistance

Canonical personalities:

Brave

Cautious

Chaotic

Neutral

⭐ X. Role System
Roles define combat behavior:

Aggressor

Defender

Support

Disruptor

Specialist

Corrupted

Roles integrate directly with the Tactical AI Bible.

⭐ XI. Tags (Canonical List)
Tags define special behavior:

baby

starter

guardian

corrupted

flying

illusion

glyph

resonance

entropy

viral

tank

healer

multi_hit

combo

Tags are used by:

AI

synergy

battle engine

evolution logic

⭐ XII. Corruption Behavior
Cyberkin have a hidden variable:

𝑐
𝑜
𝑟
𝑟
𝑢
𝑝
𝑡
𝑖
𝑜
𝑛
_
𝑙
𝑒
𝑣
𝑒
𝑙
=
0
–
100
Effects:

0–20: stable

21–50: distorted

51–80: unstable

81–100: broken

Corruption affects:

AI

stats

evolution

abilities

resistances

Some Cyberkin have corruption evolutions.

⭐ XIII. File Structure
Cyberkin files live in:

Code
/data/cyberkin/
    families/
    evolutions/
    base_stats/
    personalities/
    roles/
Each Cyberkin has:

Code
/data/cyberkin/families/<id>.json
⭐ XIV. Validation Rules
IDs must be unique

Stage must be valid

Abilities must exist

Evolution targets must exist

Resistances must be valid multipliers

Tags must be canonical

Personality must be canonical

Role must be canonical

⭐ XV. Future‑Proofing Hooks
The architecture supports:

multi‑form evolutions

corruption evolutions

regional variants

alternate roles

emotional states (Dream expansion)

bond‑based stat boosts

synergy‑based evolutions

🧬 Cyberkin Data Architecture Bible is complete.