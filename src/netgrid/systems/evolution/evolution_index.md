# Netgrid Evolution Index  
Master directory for all evolution data files in the Netgrid creature system.

This index lists each Cyberkin family, its evolution file, and a short description of its branching evolution identity.

---

## 📁 Evolution Files (Inside `families/`)

| Family   | File Path                        | Description |
|----------|----------------------------------|-------------|
| **Core** | `families/evolution_core.json`    | Balanced, foundational branching evolutions. |
| **Root** | `families/evolution_root.json`    | Growth, nature-logic, defensive and adaptive branches. |
| **Archive** | `families/evolution_archive.json` | Memory, logic, corruption-risk branches. |
| **Firewall** | `families/evolution_firewall.json` | Defense, shielding, counter-based branches. |
| **Cloud** | `families/evolution_cloud.json` | Mobility, support, weather-based branches. |
| **Echo** | `families/evolution_echo.json` | Resonance, recursion, distortion branches. |
| **Pulse** | `families/evolution_pulse.json` | Energy, speed, rhythm-based branches. |
| **Dream** | `families/evolution_dream.json` | Emotion, surreal, duality branches. |
| **Void** | `families/evolution_void.json` | Entropy, instability, rare cross-family evolutions into Corrupt. |
| **Corrupt** | `families/evolution_corrupt.json` | Glitch, instability, terminal corruption paths. |

---

## 🔧 How the Evolution Loader Uses This Index

The Evolution Loader scans the `families/` folder for all `evolution_*.json` files and merges them into a single evolution dictionary.

This index is used for:

- Documentation  
- Build validation  
- Debugging  
- Tooling (schema validators, editors, visualizers)

---

## 📚 Related Systems

- [Evolution Loader](copilot-action://composer-send?text=Show%20me%20the%20Evolution%20Loader%20again)  
- [Branching Evolutions](copilot-action://composer-send?text=How%20do%20branching%20evolutions%20work)  
- [Evolution Schema](copilot-action://composer-send?text=Explain%20JSON%20Schema%20in%20simple%20terms)  
- [Reverse Evolution Map](copilot-action://composer-send?text=How%20do%20I%20build%20a%20reverse%20evolution%20map)


## 🧩 Notes

- Families remain modular and isolated.  
- Void and Corrupt include rare cross-family evolution paths.  
- All files are schema-validated and safe for engine loading.  
