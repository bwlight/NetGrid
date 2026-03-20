## Netgrid

A digital‑mythic creature RPG built on a modular, schema‑validated engine. Netgrid blends tactical combat, emotional creature‑raising, and a data‑driven world into a unified experience set inside the Grid — a vast, living network shaped by elemental families, ancient systems, and evolving digital life.

---

## 🌐 What Is Netgrid?

Netgrid is a creature‑raising RPG where players bond with Cyberkin, explore the fractured sectors of the Grid, and uncover the mysteries of Primacore — the mythic origin system that once unified all digital life. The game blends:

- Tactical, turn‑based combat  
- Emotional bonding and evolution  
- Exploration across diverse sectors  
- A deep elemental identity system  
- A fully data‑driven world powered by JSON and schemas  

This repository serves as the public mirror for the project’s data, engine, and documentation.

---

## 🔮 Elemental Families

Every Cyberkin belongs to one of ten elemental families, each with its own identity, combat role, and visual theme:

- **Root** — growth, nature, regeneration  
- **Pulse** — energy, motion, voltage  
- **Cloud** — mist, illusion, wind  
- **Dream** — mind, memory, psychic data  
- **Void** — shadow, null, anti‑signal  
- **Firewall** — heat, defense, overload  
- **Corrupt** — virus, decay, glitch  
- **Archive** — knowledge, order, data integrity  
- **Core** — metal, structure, stability  
- **Primacore** — origin, apex, mythic system  

These families shape combat, evolution, lore, and the world itself.

---

## 📘 Explore the Game Bible

The full world lore, sector pages, species index, and system documentation are available on the Netgrid website:

**https://<your-pages-site-url>**

---

## Developer Documentation

This section provides a technical overview of the repository, engine, data architecture, and development workflow.

---

## 📁 Repository Structure

data/       → All game content (Cyberkin, abilities, statuses, AI, world data)
schemas/    → JSON schemas for validation
src/netgrid → Python engine (battle, AI, runtime models, loaders)
tools/      → Generators, validators, index builders, debugging utilities
docs/       → Game Bible (lore, design, systems)
tests/      → Pytest suite and runtime tests


---

## ⚙️ Engine Features

- Schema‑validated data loading  
- Ability system (all categories)  
- Status effect system  
- Cyberkin runtime models  
- AI behavior and scoring logic  
- Battle engine foundations  
- World and sector data structures  
- Automated index generation  
- Validation and debugging pipelines  

---

## 🚀 Installation & Setup

Clone the repository:

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

Install dependencies:

```bash
pip install -r requirements.txt
```
Run validation:
```bash
python tools/validate_all.py
```
Run tests:
```bash
pytest
```

## 🛠 Development Workflow
Add new Cyberkin → create a species JSON file → validate → rebuild indexes

Add new abilities → place in correct category folder → validate

Update schemas → run full validation suite

Modify engine → run tests to ensure compatibility

Use tools/ for automated generation and debugging

## 🗺 Roadmap
Short‑term

Finalize Cyberkin families

Complete ability and status libraries

Expand battle engine

Add world traversal logic

Mid‑term

Implement UI layer

Add save/load system

Build playable prototype

Long‑term

Full campaign

Creature bonding system

Sector‑based exploration loop

## 📄 License
All rights reserved. Netgrid is a proprietary creative project.

