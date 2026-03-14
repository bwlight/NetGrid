🧭 MASTER INDEX — CODING EDITION
“The unified directory of every system, schema, file, and rule that powers Netgrid.”
This is the single source of truth for the entire code architecture.
Every subsystem links back to this page.
Every schema, every loader, every rule is indexed here.

⭐ I. Core Coding Bibles (Primary Systems)
These are the five foundational systems that define Netgrid’s engine:

1. Ability System Bible
Defines:

ability schema

categories

damage formula

targeting rules

cooldowns & costs

synergy

corruption anomalies

ability tags

universal & sector abilities

2. Status System Bible
Defines:

status schema

buffs, debuffs, DOT, HOT

control effects

terrain

stacking rules

cleansing rules

corruption statuses

resolution order

3. Cyberkin Data Architecture Bible
Defines:

Cyberkin schema

stats & growth

evolution rules

roles & personalities

resistances

corruption behavior

ability progression

4. Battle Engine Bible
Defines:

turn order

action flow

damage calculation

accuracy & evasion

status resolution

terrain system

synergy system

corruption anomalies

AI hooks

5. Tactical AI Bible
Defines:

AI decision formula

roles

personalities

threat evaluation

memory system

corruption influence

multi‑enemy coordination

boss AI

6. Loader & File Structure Bible
Defines:

folder structure

loader modules

validation pipeline

error handling

legacy archiving

hot‑swap support

⭐ II. Canonical Schemas (Authoritative Definitions)
All schemas live in:

Code
/data/schemas/
1. ability_schema.json
Defines the structure of every ability.

2. status_schema.json
Defines the structure of every status effect.

3. cyberkin_schema.json
Defines the structure of every Cyberkin.

4. evolution_schema.json
Defines evolution requirements and branching.

These schemas are locked and referenced by all loaders.

⭐ III. Canonical Folder Structure (Global)
This is the official directory layout for all Netgrid data:

Code
/data/
    /abilities/
        universal/
        cross_family/
        root/
        firewall/
        pulse/
        dream/
        archive/
        cloud/
        echo/
        void/
        corrupt/

    /statuses/
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

    /cyberkin/
        families/
        evolutions/
        base_stats/
        personalities/
        roles/

    /battle/
        terrain/
        synergy/
        corruption/

    /schemas/
        ability_schema.json
        status_schema.json
        cyberkin_schema.json
        evolution_schema.json

    /legacy/
        abilities/
        statuses/
        cyberkin/
This structure is canonical and should not be altered.

⭐ IV. Engine Modules (Core Python Systems)
These files live in:

Code
/core/systems/
1. battle/
battle_manager.py

turn_manager.py

ability_resolver.py

status_engine.py

cooldown_manager.py

ai_controller.py

2. loaders/
ability_loader.py

status_loader.py

cyberkin_loader.py

battle_loader.py

schema_loader.py

3. utils/
logger.py

validator.py

math_tools.py

randomizer.py

⭐ V. Cross‑System Dependencies
This section defines how systems interact.

Abilities depend on:
Status System (for effects)

Cyberkin (for scaling stats)

Battle Engine (for execution)

Loader System (for validation)

Statuses depend on:
Ability System (for application)

Battle Engine (for resolution)

Loader System (for validation)

Cyberkin depend on:
Ability System (for movesets)

Status System (for resistances)

AI System (for behavior)

Loader System (for validation)

Battle Engine depends on:
Abilities

Statuses

Cyberkin

AI

Terrain rules

AI depends on:
Cyberkin roles

Cyberkin personalities

Ability tags

Status effects

Battle Engine hooks

Loader System depends on:
Schemas

File structure

Validation rules

Everything is modular and interconnected.

⭐ VI. Canonical Tags (Global Tag List)
Tags used across all systems:

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

baby

starter

guardian

corrupted

flying

tank

healer

Tags are used by:

abilities

statuses

Cyberkin

AI

synergy

evolution logic

⭐ VII. Canonical Variables (Global Engine Variables)
These variables are used across multiple systems:

corruption_level
0–100 scale for corruption behavior.

terrain_state
Current active terrain.

bond_level
Used for evolution and synergy.

threat_score
Used by AI.

action_queue
Used by Battle Engine.

cooldown_tracker
Used by Ability Resolver.

⭐ VIII. Master Validation Rules
All data must:

match schema

use canonical tags

use canonical elements

use canonical roles

use canonical personalities

use lowercase snake_case IDs

reference existing files

live in the correct folder

If any rule fails → file is skipped, engine continues.

⭐ IX. Master Debugging Modes
Global debug modes:

silent

minimal

verbose

debug

Debug mode logs:

load failures

schema mismatches

cross‑reference errors

battle events

AI decisions

corruption anomalies

⭐ X. Future‑Proofing Hooks
The architecture supports:

DLC folders

mod folders

alternate schema versions

multi‑Cyberkin parties

emotional states (Dream expansion)

corruption evolutions

synergy expansions

boss‑tier scripting

cloud‑based data loading

Your engine is built for long‑term growth.

🧭 Master Index (Coding Edition) is complete.