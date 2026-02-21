# 🧮 A. Stat Formulas — Core System
These formulas define how Cyberkin stats grow through leveling, training, care, and evolution.

All formulas are written in a way that can be implemented in Unity, Godot, Unreal, Python, or any engine.

## 1. Base Stat Formula (Per Level Growth)
Every Cyberkin has a Base Stat for each primary stat (HP, ATK, DATK, DEF, DDEF, SPD).

The formula:

	FinalStat = BaseStat + (Level × GrowthRate) + TrainingBonus

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

	TrainingBonus = TP×TrainingValue

Where TrainingValue is usually 1–3 depending on difficulty.

## 3. Care Influence Formula (Mood, Hunger, Cleanliness)
Care stats affect performance and growth.

**Mood Modifier**

	MoodMultiplier = 1 + (Mood−50 \div 200)

- Mood 100 → +25% performance
- Mood 0 → −25% performance

**Energy Modifier**

	EnergyMultiplier = Energy \div 100

- Energy 100 → full power
- Energy 50 → half power

**Cleanliness Modifier**
Affects sickness and corruption gain:

	CorruptionGain = BaseGain × (1+(100−Clean \div 100))

## 4. Corruption Formula
Corruption rises from:
- battles
- neglect
- dirty environments
- corrupted scans
- Void/Corrupt Sectors

	```Corruption + = SourceValue × StabilityFactor```

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
	```math
	SynergyBonus = \frac {∑FriendshipMatrix} {PartySize}
	```
	
High synergy = passive buffs.