🗂️ LOADER & FILE STRUCTURE BIBLE
“The complete ruleset governing how Netgrid stores, loads, validates, and organizes all game data.”
⭐ I. Purpose of the Loader System
The Loader System ensures that every piece of data in Netgrid:

loads cleanly

validates against schemas

remains modular

avoids the “God Loader” anti‑pattern

supports hot‑swapping and future expansion

keeps legacy files archived but accessible

This is the system that keeps your entire project organized, scalable, and error‑proof.

⭐ II. Core Principles of the Loader Architecture
Your loader system is built on six non‑negotiable principles:

1. Modularity
Each subsystem loads its own data independently.

2. Schema Validation
Every file must pass validation before entering the engine.

3. Canonical Folder Structure
All files live in predictable, clean, sector‑aligned directories.

4. No God Loader
No single file loads everything.
Each system loads only what it needs.

5. Legacy Archiving
Old files are archived, not deleted.

6. Debug Transparency
Load logs clearly show what succeeded, failed, or was skipped.

⭐ III. Canonical Folder Structure
Your project uses a studio‑grade directory layout:

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
Everything is clean, predictable, and future‑proof.

⭐ IV. Loader Modules (Canonical Set)
Each subsystem has its own loader:

1. Ability Loader
Loads all abilities by category and validates them.

2. Status Loader
Loads all statuses and ensures they match the Status Schema.

3. Cyberkin Loader
Loads Cyberkin, evolutions, stats, personalities, and roles.

4. Battle Loader
Loads terrain, synergy rules, and corruption rules.

5. Schema Loader
Loads schemas and exposes them to all other loaders.

Each loader is independent and can be upgraded without breaking others.

⭐ V. Loader Flow (Canonical Sequence)
Loaders run in this order:

Schema Loader

Ability Loader

Status Loader

Cyberkin Loader

Battle Loader

This ensures dependencies are always available.

⭐ VI. Validation Pipeline
Every file must pass:

1. Schema Validation
Matches the JSON schema exactly.

2. Type Validation
Ensures numbers, strings, arrays, and nulls are correct.

3. Cross‑Reference Validation
Examples:

Ability references a valid status

Cyberkin references valid abilities

Evolution references valid Cyberkin

Status references valid tags

4. Canonical Naming Validation
IDs must be:

lowercase

snake_case

unique

5. Sector Alignment Validation
Files must live in the correct folder for their element.

⭐ VII. Error Handling Rules
If a file fails validation:

It is skipped

A warning is logged

The engine continues running

The file is not loaded into memory

This prevents crashes and preserves stability.

⭐ VIII. Logging & Debugging
Loaders produce logs in four modes:

silent

minimal

verbose

debug

Debug mode includes:

file paths

validation errors

schema mismatches

cross‑reference failures

load times

This makes debugging painless.

⭐ IX. Legacy File Archiving Rules
When a file is replaced:

Move it to /data/legacy/<category>/

Add a timestamp

Add a version note

Example:

Code
burn_v1_2026-03-12.json
Legacy files are never deleted — they’re preserved for reference.

⭐ X. Loader File Structure
Loader code lives in:

Code
/core/loaders/
    ability_loader.py
    status_loader.py
    cyberkin_loader.py
    battle_loader.py
    schema_loader.py
Each loader:

loads only its own data

validates using schemas

returns a clean dictionary to the engine

⭐ XI. Hot‑Swap Support
Loaders support:

reloading abilities mid‑session

reloading statuses

reloading Cyberkin

reloading battle rules

This is perfect for:

debugging

balancing

live patching

modding

⭐ XII. Future‑Proofing Hooks
The loader system supports:

DLC folders

mod folders

alternate schema versions

multi‑language localization

encrypted data files

cloud‑based data loading

Your architecture is built to scale for years.

🗂️ Loader & File Structure Bible is complete.