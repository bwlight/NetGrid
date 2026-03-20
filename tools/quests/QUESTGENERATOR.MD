## Quest Code
QUESTGENERATOR

## Quest Type
Unknown

## Quest Title

## Sector

## Quest Summary

## Steps

## Objectives

## Rewards

## Notes

## Follow-Up Quests Unlocked
All lists under Objectives, Rewards, and Follow-Up Quests must use - bullet points.

Example:

Code

## Objectives
- Enter the corrupted chamber.
- Stabilize the resonance breach.
- Defeat the Core Entity.
Reward Conversion
Human‑readable reward text is automatically converted into symbolic tokens.

Examples
Markdown Text	JSON Token
Resonance Level 4	resonance_level:4
Unlock Sector Two	unlock_sector_2
Sector Map unlocked	unlock_sector_map
Guardian’s Blessing	guardian_blessing
Fragment: Sector Core Memory	lore_fragment_fragment_sector_core_memory
First real-world ability upgrade	ability_upgrade:first_real_world_ability_upgrade
Unknown reward text is converted to snake_case.

Follow-Up Quest Conversion
Markdown:

Code
- CORE.05 — Into Sector Two
JSON:

Code
"unlock_quest:CORE.05"
Step Generation
Each objective becomes a step with an auto‑generated ID:

Code
CORE.04.01
CORE.04.02
CORE.04.03
...
Only the final step receives rewards.

Overwrite Behavior
When the script runs, if any JSON files already exist under data/quests/, the tool prompts:

Code
Existing quest JSON files detected. Overwrite all? (y/n):
y → regenerate all JSON files

n → only generate JSON for quests that do not already exist

The tool never deletes JSON files.

Running the Generator
From the project root:

Code
python tools/generate_quests_from_docs.py
The script will:

Crawl all .md files under docs/quests/

Parse quest metadata

Convert rewards and follow‑ups

Generate JSON files under data/quests/

Validate structure against the schema (implicit via generation rules)

JSON Schema (quest.schema.json)
json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Quest",
  "type": "object",
  "required": ["id", "name", "type", "steps"],
  "properties": {
    "id": { "type": "string" },
    "name": { "type": "string" },
    "type": {
      "type": "string",
      "enum": ["main", "side", "bond", "sector", "event"]
    },
    "sector": { "type": ["string", "null"] },
    "description": { "type": ["string", "null"] },
    "steps": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "description"],
        "properties": {
          "id": { "type": "string" },
          "description": { "type": "string" },
          "conditions": { "type": "array", "items": { "type": "string" } },
          "rewards": { "type": "array", "items": { "type": "string" } }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
Extending the System
Adding new reward types
Modify the convert_reward() function in the generator script.

Adding new quest fields
Add new headers to the HEADERS dictionary and update the JSON output structure.

Adding schema validation
You can integrate jsonschema to validate each generated file automatically.

