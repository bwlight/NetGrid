# 🧮 A. Stat Formulas — Core System
These formulas define how Cyberkin stats grow through leveling, training, care, and evolution.

All formulas are written in a way that can be implemented in Unity, Godot, Unreal, Python, or any engine.

## 1. Base Stat Formula (Per Level Growth)
Every Cyberkin has a Base Stat for each primary stat (HP, ATK, DATK, DEF, DDEF, SPD).

The formula:

FinalStat = BaseStat + (Level × GrowthRate) + TrainingBonus

Where:
BaseStat = species default
GrowthRate = species growth bias (low/medium/high)
TrainingBonus = earned through training mini‑games

Example Growth Rates:
-Low = 1
-Medium = 2
-High = 3

Example:
A Rookie with:
Base ATK = 14
GrowthRate = 2
Level = 10
TrainingBonus = 4

14 + (10 × 2) + 4 = 38

## 2. Training Bonus Formula
Training mini‑games award Training Points (TP).

Each TP increases a stat:

TrainingBonus = TP×TrainingValue

Where TrainingValue is usually 1–3 depending on difficulty.

## 3. Care Influence Formula (Mood, Hunger, Cleanliness)
Care stats affect performance and growth.

**Mood Modifier**

MoodMultiplier = 1 + (Mood−50 \div 200)

-Mood 100 → +25% performance
-Mood 0 → −25% performance

**Energy Modifier**

EnergyMultiplier = Energy \div 100

-Energy 100 → full power
-Energy 50 → half power

**Cleanliness Modifier**
Affects sickness and corruption gain:

CorruptionGain = BaseGain × (1+(100−Clean \div 100))

## 4. Corruption Formula
Corruption rises from:
-battles
-neglect
-dirty environments
-corrupted scans
-Void/Corrupt Sectors

Corruption + = SourceValue × StabilityFactor

Where:

StabilityFactor = (100 − StabilityThreshold) \div 100

High StabilityThreshold = less corruption gain.

## 5. Bond Formula
Bond increases from:
-feeding
-cleaning
-playing
-winning battles
-walking together
-scanning together

BondGain = ActionValue × TemperamentModifier 

TemperamentModifier examples:

-Brave: 1.0
-Shy: 0.8
-Affectionate: 1.2
-Stoic: 0.6

## 6. Evolution Threshold Formula
Evolution checks use a weighted system:

EvolutionScore = (Stats)+(Bond×2)+(Discipline)−(Corruption×15)+(TrainingPoints)

Each evolution form has a required score range.

Example:
-Champion A: 120–160
-Champion B: 160–200
-Corrupt Evolution: Corruption > 70 AND Score < 100

## 7. Speed → Turn Order Formula

TurnPriority = SPD + Random (0,5)

This keeps battles dynamic.

## 8. Encounter Chance Formula (Mobile Exploration)

EncounterChance = RiftInstinct + SectorBonus + WeatherBonus

## 9. Scan Rarity Formula (Skannerz System)

ScanRarity = ScanSense + ObjectComplexity + Random (1,100)

Higher = rarer Cyberkin or loot.

## 10. Party Synergy Formula
SynergyBonus = ∑FriendshipMatrix \div PartySize

High synergy = passive buffs.

# 📈 B. Scaling Rules — Evolution Stage Multipliers & Growth Curves
These rules define how Cyberkin stats scale across their four evolutionary stages.
This system is designed to be:

-simple to implement
-easy to tune
-compatible with all 10 Sectors
-balanced for both mobile and PC
-faithful to Digimon‑style growth

## 1. Evolution Stage Multipliers
Each evolution stage applies a multiplier to Base Stats and Growth Rates.

Stage | Base Stat Multiplier | Growth Rate Multiplier | Notes
|:----:|:---:|:---:|
Baby | ×0.6 | ×0.5 | Weak, grows slowly, care‑focused
Rookie | ×1.0 | ×1.0 | Baseline stage
Champion | ×1.6 | ×1.4 | Stronger stats, faster growth
Final | ×2.4 | ×1.8 | Peak stats, fastest growth

Why this works:
-Babies feel fragile
-Rookies feel stable
-Champions feel powerful
-Finals feel like true endgame partners

This mirrors Digimon World 1’s stat jumps but keeps it clean and programmable.

## 2. Growth Curve Types
Each Cyberkin family uses one of three growth curves:

A) Linear Growth (Balanced Families)
Used by: Core, Root, Archive

StatGain = Level × GrowthRate

B) Accelerated Growth (Aggressive Families)
Used by: Pulse, Firewall, Corrupt

StatGain = Level^1 .2 × GrowthRate

C) Stability Growth (Defensive/Support Families)
Used by: Cloud, Echo, Dream, Void

StatGain = (Level×GrowthRate)+(Stability×0.2)

This gives each family a unique “feel” without complicating the math.

## 3. Evolution Bonus Stats
When a Cyberkin evolves, it receives a flat bonus on top of its multipliers.

Stage | Bonus HP | Bonus ATK | Bonus DATK | Bonus DEF | Bonus DDEF | Bonus SPD
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
Baby → Rookie | +10 | +4 | +4 | +4 | +4 | +3
Rookie → Champion | +20 | +8 | +8 | +8 | +8 |+6
Champion → Final | +35 | +12 | +12 | +12 | +12 | +10

These bonuses make evolution feel rewarding and noticeable.

## 4. Care‑Based Scaling (Digimon‑Style Influence)
Your care affects stat growth.

### Good Care Bonus
If:
-Hunger > 70
-Cleanliness > 70
-Mood > 70
-Energy > 50

Then: StatGain × 1.1

### Neglect Penalty
If:
-Hunger < 30
-Cleanliness < 30
-Mood < 30

Then: StatGain × 0.85

This makes raising Cyberkin meaningful.

## 5. Corruption Scaling
Corruption affects stats dynamically.

**Low Corruption (0–20)**
    No penalty
**Medium Corruption (21–60)**
    AllStats × 0.95
**High Corruption (61–90)**
    AllStats × 0.85
**Critical Corruption (91–100)**
-Random stat drops
-Random behavior
-Chance of Corrupt evolution

This ties the Corrupt Sector into the core gameplay loop.

## 6. Personality Scaling
Temperament affects growth.

Temperament | Effect 1 | Effect 2
Brave | +5% ATK | −5% DDEF
Calm | +5% DDEF | −5% SPD
Curious | +10% Scan Sense | 0
Aggressive | +10% ATK | −10% Discipline
Shy | +10% Bond gain | −5% ATK
Stoic | +10% Discipline | −5% Mood gain

This makes Cyberkin feel alive and unique.

## 7. Party Synergy Scaling
Party relationships affect stats.

**High Synergy (Friendship > 70)**
    AllStats × 1.05

**Low Synergy (Friendship < 30)**
    AllStats × 0.95

Rivalry Pair
- +10% ATK
- −10% DEF

This creates emergent party behavior.

## 8. Sector Alignment Scaling
Cyberkin gain bonuses in their aligned Sector.

**Aligned Sector**
    AllStats × 1.10
**Opposing Sector**
    AllStats × 0.90

This ties exploration and combat together.