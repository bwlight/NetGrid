🧩 STATUS SYSTEM BIBLE
“The complete ruleset governing every status effect in Netgrid.”
⭐ I. Purpose of the Status System
Statuses define ongoing effects that persist across turns.
They shape combat flow, create strategy, and allow abilities to interact in complex ways.

Statuses govern:

buffs

debuffs

DOTs (damage over time)

HOTs (healing over time)

corruption anomalies

terrain effects

illusions

resonance loops

entropy decay

Statuses are the long‑term consequences of actions in battle.

⭐ II. Status Schema (Final Canon Version)
Every status file must follow this schema:

Code
{
  "id": "string",                     // short, unique ID (e.g., 'burn', 'dream_fog')
  "name": "string",                   // display name
  "type": "string",                   // Buff, Debuff, DOT, HOT, Control, Terrain, Special
  "element": "string|null",           // Sector element (or null for universal)
  "duration": "number|null",          // number of turns (null = indefinite)
  "potency": "number|null",           // strength of effect
  "max_stacks": "number",             // stacking limit
  "stack_behavior": "string",         // refresh, extend, amplify, ignore
  "tick_timing": "string",            // start_of_turn, end_of_turn, on_action
  "effects": {                        // mechanical effects
    "attack_mod": "number|null",
    "defense_mod": "number|null",
    "speed_mod": "number|null",
    "magic_mod": "number|null",
    "accuracy_mod": "number|null",
    "evasion_mod": "number|null",
    "dot": "number|null",
    "hot": "number|null",
    "special": "string|null"          // custom logic hook
  },
  "cleansable": "boolean",            // can it be removed?
  "tags": ["string"],                 // dream, corruption, echo, glyph, etc.
  "description": "string"             // in-game text
}
This schema is locked and should not change unless the engine evolves.

⭐ III. Status Categories (Canonical)
Statuses fall into these categories:

1. Buffs
Increase stats or grant positive effects.

2. Debuffs
Reduce stats or impose penalties.

3. DOT (Damage Over Time)
Burn, bleed, corruption decay, entropy drain.

4. HOT (Healing Over Time)
Regeneration, dream mending, root growth.

5. Control
Stun, sleep, charm, confusion, silence.

6. Terrain
Sector‑themed battlefield effects.

7. Special
Illusions, glyph marks, resonance loops, corruption anomalies.

⭐ IV. Duration Rules
Duration decreases at the end of the affected Cyberkin’s turn.

Duration cannot drop below 1 unless cleansed or overwritten.

Indefinite statuses require a special hook to remove.

⭐ V. Stacking Rules
Statuses can stack in four ways:

1. Refresh
Resets duration to max.

2. Extend
Adds duration (up to a cap).

3. Amplify
Increases potency.

4. Ignore
Additional stacks do nothing.

Each status defines its own behavior.

⭐ VI. Tick Timing Rules
Statuses activate at one of three times:

start_of_turn

end_of_turn

on_action (rare, used for corruption or resonance)

DOTs and HOTs typically tick at end_of_turn.

⭐ VII. Cleansing Rules
A status can be cleansed if:

cleansable = true

the ability used has the cleanse tag

the Cyberkin has a passive that removes statuses

terrain effects override it

Corruption statuses often have cleansable = false.

⭐ VIII. Status Interaction Rules
Statuses interact with each other based on tags:

Dream + Echo
Illusions become clones.

Root + Cloud
Regeneration spreads to allies.

Pulse + Echo
Resonance loops trigger multi‑hit effects.

Void + Corrupt
Entropy ruptures cause instant decay.

Firewall + Corrupt
Purification burns corruption stacks.

These interactions are defined in the Battle Engine Bible, but referenced here.

⭐ IX. Canonical Status List (Core Set)
These are the universal statuses every Sector can use:

Buffs
Attack Up

Defense Up

Speed Up

Magic Up

Accuracy Up

Evasion Up

Debuffs
Attack Down

Defense Down

Speed Down

Magic Down

Accuracy Down

Evasion Down

DOT
Burn (Firewall)

Poison (Root)

Static Shock (Pulse)

Entropy Decay (Void)

Corruption Rot (Corrupt)

HOT
Regeneration (Root)

Dream Mend (Dream)

Cloud Drift Heal (Cloud)

Control
Stun

Sleep

Charm

Confusion

Silence

Fear (Void)

Special
Glyph Mark (Archive)

Echo Clone (Echo)

Illusion Veil (Dream)

Corrupt Mutation (Corrupt)

⭐ X. Status File Structure
Statuses are stored in:

Code
/data/statuses/
    universal/
    root/
    firewall/
    pulse/
    dream/
    archive/
    cloud/
    echo/
    void/
    corrupt/
Each file is named:

Code
<id>.json
⭐ XI. Validation Rules
IDs must be unique

Duration must be ≥ 1 or null

Potency must be ≥ 0

Tags must be from the canonical list

Element must match a Sector or be null

Status effects must match the schema

⭐ XII. Corruption Status Rules
Corruption statuses are special:

cannot be cleansed (usually)

mutate at random

may spread to allies or enemies

may override other statuses

may cause recursion loops

may trigger corruption anomalies in abilities

Corruption is the only status type that can rewrite itself.

⭐ XIII. Terrain Status Rules
Terrain statuses affect the entire battlefield:

Rootfield (healing vines)

Firewall Dome (purification flame)

Pulse Circuit (speed boost)

Dream Fog (illusion chance)

Archive Crystal Field (glyph amplification)

Cloud Drift (evasion boost)

Echo Chamber (resonance loops)

Void Silence (no healing)

Corrupt Zone (mutation chance)

Only one terrain can be active at a time.

⭐ XIV. Status Resolution Order
Statuses resolve in this order:

Start‑of‑turn statuses

Action

On‑action statuses

End‑of‑turn statuses

Duration reduction

Expiration checks

This order is canon and must not change.

⭐ XV. Special Hooks
Statuses can define special logic:

on_apply

on_expire

on_tick

on_hit

on_damage_taken

on_ally_action

on_enemy_action

These hooks are implemented in the Battle Engine.

🧩 Status System Bible is complete.