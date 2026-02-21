# 🧬 Cyberkin Core Stats — Master Reference
Netgrid Canon System Document
Version 1.0 — Editable

This document defines the official Core Stats used by all Cyberkin across mobile and PC/console versions of Netgrid.
These stats power:
-care system
-evolution system
-combat system
-scanning system
-GPS exploration
-party dynamics
-corruption mechanics

This page is designed to be editable so we can refine formulas and scaling as the system evolves.

## 1. Primary Combat Stats
These stats define a Cyberkin’s battle performance.

Stat | Key | Description
Health Points | HP | Determines survivability.
Attack | ATK | Physical/melee damage output.
Digital Attack | DATK | Energy/sector‑type damage output.
Defense | DEF | Reduces physical damage taken.
Digital Defense | DDEF | Reduces digital/sector damage taken.
Speed | SPD | Determines turn order, dodge chance, and encounter initiative.

## 2. Care & Condition Stats
These stats drive the Tamagotchi/Digimon‑style care loop.

Stat | Key | Description
Hunger | HUNGER | How urgently the Cyberkin needs food.
Energy | ENERGY | Stamina for training, battles, and exploration.
Mood | MOOD | Emotional state; affects performance and behavior.
Cleanliness | CLEAN | Hygiene level; affects sickness and corruption.
Corruption | CORRUPTION | Instability level; affects evolution and behavior.

## 3. Bonding & Behavior Stats

These stats define emotional connection and obedience.

Stat | Key | Description
Bond | BOND | Relationship strength with the player.
Discipline | DISCIPLINE | Obedience and stability; affects evolution.
Friendship Matrix | FRIENDSHIP[x][y] | How Cyberkin feel about each other.
Synergy| SYNERGY | Party‑wide compatibility bonus.

## 4. Growth Stats
These stats track long‑term progression.

Stat | Key | Description
Level | LVL | Overall growth tier.
Experience | XP | Points earned from battles, training, exploration.
Training Points | TP | Earned from training mini‑games.
Age | AGE | Time since creation/hatching.
Weight | WEIGHT | Optional Digimon‑style stat.

## 5. Sector Affinity Stats
These stats tie Cyberkin to the 10 Sectors.

Stat | Key | Description
Sector Alignment | ALIGNMENT | Core/Root/Archive/etc.
Sector Resistance | SECTOR_RESIST | Bonus defense in aligned sectors.
Sector Weakness | SECTOR_WEAK | Penalty in opposing sectors.

## 6. Exploration & Scan Stats
These stats power the Pokémon GO + Skannerz hybrid loop.

Stat | Key | Description
Scan Sense | SCAN_SENSE | Chance to detect rare scans.
Rift Instinct | RIFT_INSTINCT | Chance to trigger encounters.
Terrain Adaptation | TERRAIN_ADAPT | Bonus in certain GPS biomes.
Curiosity | CURIOSITY | Frequency of idle events/requests.

## 7. Hidden Stats
These stats are invisible to the player but drive behavior and evolution.

Stat | Key | Description
Temperament | TEMPERAMENT | Calm, aggressive, shy, curious, etc.
Growth Bias | GROWTH_BIAS | Which stats grow faster.
Mutation Potential |MUTATION_POTENTIAL | Chance of Corrupt evolutions.
Stability Threshold | STABILITY_THRESHOLD | How easily corruption rises.

## 8. JSON Structure Example
Here’s how a Cyberkin’s core stats would look in JSON:
'''json
{
  "id": "core_001",
  "name": "Bytecub",
  "stage": "rookie",
  "sector": "Core",

  "stats": {
    "HP": 34,
    "ATK": 18,
    "DATK": 20,
    "DEF": 22,
    "DDEF": 20,
    "SPD": 16
  },

  "care": {
    "HUNGER": 40,
    "ENERGY": 70,
    "MOOD": 80,
    "CLEAN": 60,
    "CORRUPTION": 5
  },

  "bonding": {
    "BOND": 25,
    "DISCIPLINE": 40
  },

  "growth": {
    "LVL": 5,
    "XP": 120,
    "TP": 3,
    "AGE": 2,
    "WEIGHT": 8
  },

  "sector_affinity": {
    "ALIGNMENT": "Core",
    "SECTOR_RESIST": ["Root", "Archive"],
    "SECTOR_WEAK": ["Void", "Corrupt"]
  },

  "exploration": {
    "SCAN_SENSE": 12,
    "RIFT_INSTINCT": 8,
    "TERRAIN_ADAPT": ["Urban"],
    "CURIOSITY": 15
  },

  "hidden": {
    "TEMPERAMENT": "Brave",
    "GROWTH_BIAS": "Balanced",
    "MUTATION_POTENTIAL": 2,
    "STABILITY_THRESHOLD": 85
  }
}
'''
