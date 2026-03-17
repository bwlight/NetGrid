<div id="sidebar">
  <div class="sidebar-title">NETGRID</div>

  <nav class="sidebar-nav">
    <a href="/">🏠 Home</a>
    <a href="https://github.com/<your-username>/<your-repo>/tree/main/data">📁 Data</a>
    <a href="https://github.com/<your-username>/<your-repo>/tree/main/docs">📚 Game Bible</a>
    <a href="https://github.com/<your-username>/<your-repo>/tree/main/schemas">🧩 Schemas</a>
    <a href="https://github.com/<your-username>/<your-repo>/tree/main/src/netgrid">⚙️ Engine</a>
    <a href="https://github.com/<your-username>/<your-repo>/tree/main/tools">🛠 Tools</a>
    <a href="https://github.com/<your-username>/<your-repo>/tree/main/tests">🧪 Tests</a>
  </nav>

  <button id="sidebar-toggle">☰</button>
</div>

<script>
  const sidebar = document.getElementById("sidebar");
  const toggle = document.getElementById("sidebar-toggle");

  toggle.onclick = () => {
    sidebar.classList.toggle("open");
  };
</script>


<link rel="stylesheet" href="assets/css/colors.css">
<div style="font-size:1.15rem; color:#9cd3ff; margin-top:-0.5rem; text-shadow:0 0 8px rgba(100,180,255,0.4);">
A Digital‑Mythic Creature RPG
</div>

<div style="border-bottom:1px solid rgba(80,150,255,0.25); margin:1.2rem 0;"></div>

<div style="font-size:0.95rem; color:#7f8694;">
Schema‑Driven • Modular Engine • Data‑Powered Worldbuilding
</div>

Netgrid Project Repository

Netgrid is a digital‑mythic creature RPG built on a fully modular, schema‑validated architecture.
This site provides a clean, navigable entry point into the project’s structure, letting you explore the data, engine, documentation, and tooling that power the world of the Grid.

📁 Data Layer
The canonical source of truth for all game content. Every Cyberkin, ability, status effect, AI behavior, and world definition lives here in structured JSON.

Abilities — Elemental, disruptive, mythic, passive, signature, support, and ultimate abilities

Cyberkin — Rookie, Champion, Final, and legacy species

Statuses — DOTs, debuffs, buffs, battlefield effects

AI — Behavior configs, scoring profiles, and indexes

World Data — Nodes, sectors, panels, travel maps

Indexes — Master indexes for abilities, species, families, and elements

Explore:
https://github.com/bwlight/netgrid/tree/main/data

📚 Game Bible (Documentation)
Narrative, design, and system documentation for the Netgrid universe.
This is the studio‑grade Game Bible that defines the world, its lore, its creatures, and its mechanics.

Bestiary — Family pages, species lore, evolution lines

Design — Battle system, stability, evolution, UI/UX, gameplay loops

Lore — Sectors, mythology, factions, world origin

Quests — Main story, bond quests, sector quests, side quests

Reference — Glossaries, naming conventions, style guides

System Docs — Engine architecture, data flow, schemas

Explore:
https://github.com/bwlight/netgrid/tree/main/docs

🧩 Schemas
The validation backbone of Netgrid.
Every data file in the project is validated against these schemas to ensure consistency, safety, and engine compatibility.

Ability schema

Cyberkin schema

Status schema

AI behavior schema

Map and travel schemas

Master index schema

Netgrid root schema

Explore:
https://github.com/bwlight/netgrid/tree/main/schemas

⚙️ Engine (src/netgrid)
The full Python engine that loads, validates, and runs the game.

Core Systems — Battle, evolution, party, stability, status, travel

AI — Loaders, managers, behavior logic

Models — Cyberkin runtime classes

Assets — Glyphs, icons, UI panels, portraits

Engine Modules — Quest engine, world engine, runtime state

Explore:
https://github.com/bwlight/netgrid/tree/main/src/netgrid

🛠 Developer Tools
A complete DevOps/DataOps suite for generating, validating, indexing, and debugging Netgrid content.

Generators

Master builders

Validators

Pipelines

Debugging utilities

TODO scanning and reporting

Explore:
https://github.com/bwlight/netgrid/tree/main/tools

🧪 Tests
Runtime tests, pytest configuration, and logging utilities that ensure the engine loads and runs cleanly.

Explore:
https://github.com/bwlight/netgrid/tree/main/tests

📄 Project Files
General project metadata and documentation.

README

Roadmap

Feature checklist

Devlog template

Code of Conduct

Git attributes and ignore rules

Explore:
https://github.com/bwlight/netgrid

About Netgrid
Netgrid blends digital mysticism, tactical combat, and emotional creature‑raising into a unified RPG experience.
This repository serves as the public mirror for the project’s data, engine, and documentation.

<button id="theme-toggle" style="
  background: var(--code-bg);
  color: var(--accent);
  border: 1px solid var(--accent-soft);
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 1rem;
">
  Change Theme
</button>

<script>
  const themes = ["","theme-root","theme-pulse","theme-cloud","theme-dream","theme-void","theme-firewall","theme-corrupt","theme-archive","theme-core","theme-primacore"];
  let index = 0;

  const saved = localStorage.getItem("netgrid-theme");
  if (saved) {
    document.body.className = saved;
    index = themes.indexOf(saved);
  }

  document.getElementById("theme-toggle").onclick = () => {
    index = (index + 1) % themes.length;
    const theme = themes[index];
    document.body.className = theme;
    localStorage.setItem("netgrid-theme", theme);
  };
</script>


<footer style="
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(80,150,255,0.25);
  color: #7f8694;
  font-size: 0.9rem;
  text-align: center;
">

  <div style="font-size:1rem; color:#9cd3ff; margin-bottom:0.4rem;">
    Netgrid Project Repository
  </div>

  <div style="margin-bottom:0.6rem;">
    A digital‑mythic creature RPG built on a modular, schema‑validated engine.
  </div>

  <div style="opacity:0.8;">
    © <span id="year"></span> Netgrid Development — All rights reserved.
  </div>

  <script>
    document.getElementById("year").textContent = new Date().getFullYear();
  </script>

</footer>