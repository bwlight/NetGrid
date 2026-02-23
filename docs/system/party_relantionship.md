# 🤝 Netgrid Party Relationship System — JSON Schema Documentation
Version 1.0 — GitHub‑Ready

This document defines the official JSON schema for the Party Relationship System.
It covers all five modular JSON files:
- friendship_matrix.json
- synergy_rules.json
- relationship_types.json
- party_events.json
- relationship_evolution_modifiers.json

These files work together to define how Cyberkin interact, bond, clash, and influence each other’s evolution.

## 1. friendship_matrix.json
Purpose
Stores pairwise friendship values between Cyberkin in the party.

Schema
```json
{
  "friendship_matrix": {
    "description": "Pairwise friendship values between Cyberkin in the party.",
    "range": {
      "min": 0,
      "max": 100
    },
    "initialization": {
      "default_value": 50,
      "personality_modifier": true,
      "corruption_modifier": true
    },
    "example_structure": {
      "cyberkin_ids": ["A", "B", "C"],
      "matrix": {
        "A": { "B": 50, "C": 50 },
        "B": { "A": 50, "C": 50 },
        "C": { "A": 50, "B": 50 }
      }
    }
  }
}
```
### Notes
- Friendship is directional (A→B may differ from B→A).
- Default value is 50 (neutral).
- Personality and corruption can modify initialization.

## 2. synergy_rules.json
Purpose
Defines synergy tiers and their stat effects.

Schema
```json
{
  "synergy_rules": {
    "calculation": "average_friendship",
    "tiers": [
      {
        "name": "Chaotic",
        "range": [0, 29],
        "effects": {
          "DEF": -0.10,
          "SPD": -0.05
        }
      },
      {
        "name": "Neutral",
        "range": [30, 59],
        "effects": {}
      },
      {
        "name": "Harmonized",
        "range": [60, 79],
        "effects": {
          "ATK": 0.05,
          "DEF": 0.05
        }
      },
      {
        "name": "Synchronized",
        "range": [80, 100],
        "effects": {
          "ATK": 0.10,
          "DEF": 0.10,
          "SPD": 0.05
        }
      }
    ]
  }
}
```
### Notes
Synergy is the average of all friendship values.

Effects apply party‑wide.

## 3. relationship_types.json
Purpose
Defines relationship categories and their mechanical effects.

Schema
```json
{
  "relationship_types": [
    {
      "name": "Bonded",
      "threshold": { "min": 80, "max": 100 },
      "effects": {
        "ATK_together": 0.10,
        "DEF_protect": 0.10,
        "combo_attack_chance": 0.15
      }
    },
    {
      "name": "Friendly",
      "threshold": { "min": 60, "max": 79 },
      "effects": {
        "ATK": 0.05,
        "DEF": 0.05
      }
    },
    {
      "name": "Neutral",
      "threshold": { "min": 40, "max": 59 },
      "effects": {}
    },
    {
      "name": "Rival",
      "threshold": { "min": 20, "max": 39 },
      "effects": {
        "ATK": 0.10,
        "DEF": -0.10,
        "crit_chance": 0.05
      }
    },
    {
      "name": "Hostile",
      "threshold": { "min": 0, "max": 19 },
      "effects": {
        "ATK": -0.10,
        "DEF": -0.10,
        "SPD": -0.10,
        "ignore_command_chance": 0.10,
        "corruption_event_chance": 0.10
      }
    }
  ]
}
```
### Notes
- Relationship type is determined per pair, not party‑wide.
- Effects apply only when paired Cyberkin act together.

## 4. party_events.json
Purpose
Defines events that modify relationships.

Schema
```json
{
  "party_events": [
    {
      "name": "PlayfulInteraction",
      "trigger": "random_positive",
      "effects": { "friendship_gain": 5 }
    },
    {
      "name": "ProtectiveMoment",
      "trigger": "battle_defense",
      "effects": { "friendship_gain": 8, "bond_gain": 2 }
    },
    {
      "name": "SharedVictory",
      "trigger": "battle_win",
      "effects": { "friendship_gain": 4 }
    },
    {
      "name": "Argument",
      "trigger": "random_negative",
      "effects": { "friendship_loss": 6 }
    },
    {
      "name": "Jealousy",
      "trigger": "uneven_attention",
      "effects": { "friendship_loss": 4, "rivalry_chance": 0.10 }
    },
    {
      "name": "CorruptionSurge",
      "trigger": "corruption_spike",
      "effects": { "friendship_loss": 10, "fear_chance": 0.20 }
    }
  ]
}
```
### Notes
- Events can be random or triggered by gameplay.
- Effects can modify friendship, bond, rivalry, or corruption.

### 5. relationship_evolution_modifiers.json
Purpose
Defines how relationships influence evolution.

Schema
```json
{
  "relationship_evolution_modifiers": {
    "bonded": {
      "evolution_score_bonus": 10,
      "discipline_bonus": 5,
      "corruption_reduction": 5
    },
    "rival": {
      "atk_bonus": 10,
      "discipline_penalty": 10,
      "corrupt_evolution_chance": 0.15
    },
    "hostile": {
      "corruption_gain": 10,
      "discipline_penalty": 10,
      "forced_corrupt_threshold": 0.90
    }
  }
}
```
### Notes
- These modifiers plug directly into the Evolution System.
- Hostile relationships can force corruption evolutions.
