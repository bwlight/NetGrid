# 🧮 A. Stat Formulas — Core System
These formulas define how Cyberkin stats grow through leveling, training, care, and evolution.

All formulas are written in a way that can be implemented in Unity, Godot, Unreal, Python, or any engine.

## 1. Base Stat Formula (Per Level Growth)
Every Cyberkin has a Base Stat for each primary stat (HP, ATK, DATK, DEF, DDEF, SPD).

The formula:
[ \text{FinalStat} = \text{BaseStat} + (\text{Level} \times \text{GrowthRate}) + \text{TrainingBonus} ]

Where:
- BaseStat = species default
- GrowthRate = species growth bias (low/medium/high)
- TrainingBonus = earned through training mini‑games

Example Growth Rates:
- Low = 1
- Medium = 2
- High = 3

Example:
A Rookie with:
- Base ATK = 14
- GrowthRate = 2
- Level = 10
- TrainingBonus = 4

14 + (10 × 2) + 4 = 38

## 2. Training Bonus Formula
Training mini‑games award Training Points (TP).

Each TP increases a stat:

[ \text{TrainingBonus} = \text{TP} \times \text{TrainingValue} ]

Where TrainingValue is usually 1–3 depending on difficulty.

## 3. Care Influence Formula (Mood, Hunger, Cleanliness)
Care stats affect performance and growth.

**Mood Modifier**

[ \text{MoodMultiplier} = 1 + \left(\frac{\text{Mood} - 50}{200}\right) ]

- Mood 100 → +25% performance
- Mood 0 → −25% performance

**Energy Modifier**

[ \text{EnergyMultiplier} = \frac{\text{Energy}}{100} ]

- Energy 100 → full power
- Energy 50 → half power

**Cleanliness Modifier**
Affects sickness and corruption gain:

[ \text{CorruptionGain} = \text{BaseGain} \times \left(1 + \frac{100 - \text{Clean}}{100}\right) ]

## 4. Corruption Formula
Corruption rises from:
- battles
- neglect
- dirty environments
- corrupted scans
- Void/Corrupt Sectors

[ \text{Corruption} += \text{SourceValue} \times \text{StabilityFactor} ]

Where:

[ \text{StabilityFactor} = \frac{100 - \text{StabilityThreshold}}{100} ]

High StabilityThreshold = less corruption gain.

## 5. Bond Formula
Bond increases from:
-feeding
-cleaning
-playing
-winning battles
-walking together
-scanning together

[ \text{BondGain} = \text{ActionValue} \times \text{TemperamentModifier} ]

TemperamentModifier examples:

-Brave: 1.0
-Shy: 0.8
-Affectionate: 1.2
-Stoic: 0.6

## 6. Evolution Threshold Formula
Evolution checks use a weighted system:

[ \text{EvolutionScore} = (\text{Stats}) + (\text{Bond} \times 2) + (\text{Discipline}) - (\text{Corruption} \times 1.5) + (\text{TrainingPoints}) ]

Each evolution form has a required score range.

Example:
-Champion A: 120–160
-Champion B: 160–200
-Corrupt Evolution: Corruption > 70 AND Score < 100

## 7. Speed → Turn Order Formula

[ \text{TurnPriority} = \text{SPD} + \text{Random}(0,5) ]

This keeps battles dynamic.

## 8. Encounter Chance Formula (Mobile Exploration)

[ \text{EncounterChance} = \text{RiftInstinct} + \text{SectorBonus} + \text{WeatherBonus} ]

## 9. Scan Rarity Formula (Skannerz System)

[ \text{ScanRarity} = \text{ScanSense} + \text{ObjectComplexity} + \text{Random}(1,100) ]

Higher = rarer Cyberkin or loot.

## 10. Party Synergy Formula

[ \text{SynergyBonus} = \frac{\sum \text{FriendshipMatrix}}{\text{PartySize}} ]

High synergy = passive buffs.
