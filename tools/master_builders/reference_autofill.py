#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parent.parent.parent

CYBERKIN_INDEX = BASE / "data" / "indexes" / "cyberkin_index.json"
CYBERKIN_DIR = BASE / "data" / "cyberkin"
REFERENCE_DIR = BASE / "docs" / "reference"
FAMILY_DATA_DIR = BASE / "docs" / "lore" / "family_data"


def load_json(path):
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_cyberkin_file(ck_name, stage):
    ck_path = CYBERKIN_DIR / stage.lower() / f"{ck_name}.json"
    if not ck_path.exists():
        return None
    return load_json(ck_path)["cyberkin"]


# ---------- PARSER FOR FAMILY_DATA/<family>.md ----------

def load_family_data_block(path):
    if not path.exists():
        return {}

    lines = path.read_text(encoding="utf-8").splitlines()
    data = {
        "habitat": None,
        "evolution_requirements": [],
        "quest_hooks": []
    }

    current_key = None

    for line in lines:
        stripped = line.strip()

        # Habitat: "value"
        if stripped.lower().startswith("habitat:"):
            value = stripped.split(":", 1)[1].strip().strip('"')
            data["habitat"] = value
            current_key = None
            continue

        # Evolution_requirements:
        if stripped.lower().startswith("evolution_requirements"):
            current_key = "evolution_requirements"
            continue

        # Quest_hooks:
        if stripped.lower().startswith("quest_hooks"):
            current_key = "quest_hooks"
            continue

        # List items: "value",
        if current_key and stripped.startswith('"'):
            value = stripped.strip().strip('",')
            data[current_key].append(value)

    return data


# ---------- AUTO-FILL INFERENCE LOGIC ----------

def infer_sector_from_cyberkin(cyberkin_list):
    sectors = [ck.get("sector") for ck in cyberkin_list if ck.get("sector")]
    if not sectors:
        return "Unknown — to be defined"
    return Counter(sectors).most_common(1)[0][0]


def infer_type(elements):
    if len(elements) == 1:
        return list(elements)[0].capitalize()
    if len(elements) > 1:
        return "Hybrid"
    return "Unknown — to be defined"


def infer_habitat(tags):
    if any(t in tags for t in ["forest", "nature", "wild"]):
        return "Forest biomes"
    if any(t in tags for t in ["urban", "tech", "industrial"]):
        return "Urban/industrial zones"
    if any(t in tags for t in ["cave", "rock", "earth"]):
        return "Subterranean caverns"
    if any(t in tags for t in ["water", "aqua", "tide"]):
        return "Aquatic regions"
    if any(t in tags for t in ["sky", "wind", "storm"]):
        return "High-altitude zones"
    if any(t in tags for t in ["desert", "sand"]):
        return "Arid regions"
    return "Varied habitats across the sector"


def infer_themes(roles, personalities):
    themes = set()
    if "support" in roles:
        themes.update(["Team synergy", "Healing", "Buffing"])
    if "disruptor" in roles:
        themes.update(["Interference", "Control", "Debuffs"])
    if "offense" in roles:
        themes.update(["Aggression", "Power"])
    if "defense" in roles:
        themes.update(["Protection", "Endurance"])
    if "loyal" in personalities:
        themes.add("Loyalty")
    if "curious" in personalities:
        themes.add("Discovery")
    if "aggressive" in personalities:
        themes.add("Predation")
    return list(themes)


def combine_family_abilities(abilities_list):
    combined = set()

    for ck in abilities_list:
        for category, ability_names in ck.items():
            if isinstance(ability_names, list):
                for ability in ability_names:
                    combined.add(ability)

    return sorted(combined)


def build_autofill_lore(family_id, cyberkin_list):
    elements = Counter()
    tags = Counter()
    roles = Counter()
    personalities = Counter()
    abilities = []
    evolutions = []

    for ck in cyberkin_list:
        elements[ck["element"].lower()] += 1
        for t in ck["tags"]:
            tags[t.lower()] += 1
        for r in ck["role"]:
            roles[r.lower()] += 1
        for p in ck["personality"]:
            personalities[p.lower()] += 1
        abilities.append(ck["abilities"])
        evolutions.append(ck["evolution"])

    element_set = set(elements.keys())
    tag_set = set(tags.keys())
    role_set = set(roles.keys())
    personality_set = set(personalities.keys())

    return {
        "sector": infer_sector_from_cyberkin(cyberkin_list),
        "type": infer_type(element_set),
        "habitat": infer_habitat(tag_set),
        "themes": infer_themes(role_set, personality_set),
        "evolution_requirements": [],
        "quest_hooks": [],
        "example_abilities": combine_family_abilities(abilities)
    }


# ---------- MAIN SCRIPT ----------

def main():
    print("Auto-fill reference builder starting...\n")

    cyberkin_index = load_json(CYBERKIN_INDEX)
    families = {}

    for ck_name, ck_info in cyberkin_index["cyberkin"].items():
        family = ck_info.get("family", "none").lower()
        if not family or family == "none":
            family = "none"
        families.setdefault(family, []).append(ck_name)

    print("Choose how to handle existing reference files:")
    print("1) Update (overwrite)")
    print("2) Fill Fields Only")
    print("3) Ask me per family")
    mode = input("Enter 1, 2, or 3: ").strip()

    REFERENCE_DIR.mkdir(parents=True, exist_ok=True)

    for family_id, member_ids in families.items():
        json_path = REFERENCE_DIR / f"{family_id}.json"
        md_path = REFERENCE_DIR / f"{family_id}.md"

        cyberkin_list = []
        for ck_name in member_ids:
            stage = cyberkin_index["cyberkin"][ck_name]["stage"]
            ck_data = load_cyberkin_file(ck_name, stage)
            if ck_data:
                cyberkin_list.append(ck_data)

        autofill = build_autofill_lore(family_id, cyberkin_list)

        # Load custom family_data overrides
        family_data_path = FAMILY_DATA_DIR / f"{family_id}.md"
        family_data = load_family_data_block(family_data_path)

        if family_data.get("habitat"):
            autofill["habitat"] = family_data["habitat"]

        if family_data.get("evolution_requirements"):
            autofill["evolution_requirements"] = family_data["evolution_requirements"]

        if family_data.get("quest_hooks"):
            autofill["quest_hooks"] = family_data["quest_hooks"]

        # Determine overwrite behavior
        if json_path.exists() and mode == "3":
            print(f"\nFamily '{family_id}' already has a reference file.")
            print("1) Update (overwrite)")
            print("2) Fill Fields Only")
            choice = input("Enter 1 or 2: ").strip()
        else:
            choice = mode

        # JSON writing
        if choice == "1":
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(autofill, f, indent=2)
        else:
            existing = load_json(json_path)
            for key, value in autofill.items():

                # Sector should always update unless manually written
                if key == "sector":
                    if existing.get("sector") in [None, "", "Unknown — to be defined"]:
                        existing["sector"] = value
                    continue

                # Normal fill-only behavior
                if key not in existing or not existing[key]:
                    existing[key] = value

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(existing, f, indent=2)

        # Markdown summary block
        summary = (
            f"# {family_id.capitalize()} Family Lore\n\n"
            f"## Summary\n"
            f"- **Sector:** {autofill['sector']}\n"
            f"- **Type:** {autofill['type']}\n"
            f"- **Habitat:** {autofill['habitat']}\n"
            f"- **Themes:** {', '.join(autofill['themes']) if autofill['themes'] else 'None'}\n"
            f"- **Evolution Requirements:** {', '.join(autofill['evolution_requirements']) if autofill['evolution_requirements'] else 'None'}\n"
            f"- **Quest Hooks:** {', '.join(autofill['quest_hooks']) if autofill['quest_hooks'] else 'None'}\n"
            f"- **Example Abilities:** {', '.join(autofill['example_abilities']) if autofill['example_abilities'] else 'None'}\n\n"
            f"Auto-generated baseline lore.\n"
        )

        if not md_path.exists() or choice == "1":
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(summary)

    print("\nReference auto-fill complete.")


if __name__ == "__main__":
    main()
