#🌱 Netgrid Care System — Full System Blueprint
This is the official care loop for Cyberkin.
It’s built around needs, decay, player actions, care mistakes, and evolution influence.

Let’s break it down cleanly.

## 1. Care Stats (The Heart of the System)
These are the stats the Care System manipulates:

|Stat |	Range | Meaning |
|:---:|:---:|:---:|
Hunger | 0–100 | How full the Cyberkin is
Energy | 0–100 | Stamina for activities
Mood | 0–100 | Emotional state
Cleanliness | 0–100 | Hygiene level
Corruption | 0–100 | Instability level
Bond | 0–100 | Relationship strength
Discipline | 0–100 | Obedience & stability

These are the “living creature” stats that make Cyberkin feel real.

## 2. Natural Decay System
Every Cyberkin has a passive decay loop that runs over time.

### Hunger Decay
- Drops every 20–40 minutes (species‑dependent)
- Faster for energetic/aggressive Cyberkin
- Slower for calm/heavy Cyberkin

### Energy Decay
Drops from:
- battles
- training
- walking
- exploration
- Recovers through rest/sleep

### Mood Decay
Mood decreases when:
- Hunger < 40
- Cleanliness < 40
- Corruption rises
- They’re ignored
- They lose battles

### Cleanliness Decay
- Drops slowly over time
- Drops faster after battles or exploration
- Drops sharply after corruption events

### Corruption Gain
Corruption increases from:
- neglect
- dirty environments
- corrupted scans
- Void/Corrupt sectors
- care mistakes

## 3. Player Actions (The Care Menu)
These are the actions the player can take to care for their Cyberkin.

### Feeding
Effects:
- Hunger +20 to +40
- Bond +1
- Weight +1
- Overfeeding → Weight +3, Discipline −2

### Cleaning
Effects:
- Cleanliness +40
- Corruption −2
- Discipline +2

### Playing
Effects:
- Mood +20
- Bond +3
- Energy −5

### Training
Effects:
- TP +1
- Discipline +3
- Energy −10
- Mood −5

### Resting / Sleeping
Effects:
- Energy +30
- Mood +5
- Cleanliness −5

### Walking / Exploration
Effects:
- Bond +2
- Mood +5
- Scan Sense +1
- Energy −5

## 4. Care Mistakes (Digimon‑Style Penalties)
A care mistake happens when:
- Hunger hits 0
- Energy hits 0
- Cleanliness hits 0
- Mood hits 0
- Corruption exceeds 60
- A Cyberkin calls for attention and is ignored

Each mistake applies:
- Corruption +5
- Bond −3
- Discipline −4
- Mood −10

These matter a lot for evolution.

## 5. Attention Calls (The “Ping” System)
Cyberkin will call the player when they need something.

Triggers:
- Hunger < 30
- Cleanliness < 30
- Mood < 40
- Wants to play
- Wants to explore
- Wants to interact with another party member
- Ignoring a call = **care mistake**

Responding quickly:
- Bond +2
- Discipline +1

## 6. Care → Evolution Influence
Care directly shapes evolution outcomes.

### Good Care Evolution Requirements
- Bond > 60
- Discipline > 50
- Corruption < 20
- < 3 care mistakes

### Neutral Evolution Requirements
- Mixed stats
- Moderate corruption
- Moderate discipline

### Corrupt Evolution Requirements
- Corruption > 60
- Discipline < 30
- Mood < 30
- 5 care mistakes

This gives you the branching evolution system you want.

## 7. Care Formulas (GitHub‑Safe Math)
### Hunger Decay
Hunger − = DecayRate × SpeciesModifier

### Energy Recovery
Energy + = RestValue × TemperamentModifier

### Mood Change
Mood + = ActionValue − PenaltyValue

### Corruption Gain
Corruption + = SourceValue × (1+100−Clean \div 100)

### Bond Gain
Bond + = ActionValue × TemperamentModifier