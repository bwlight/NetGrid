import os
import json
import sys

CYBERKIN_ROOT = os.path.join("data", "cyberkin")
ABILITIES_ROOT = os.path.join("data", "abilities")

IGNORE_ABILITY_FOLDERS = {".LEGACY"}
IGNORE_CYBERKIN_FOLDERS = {".LEGACY"}

STAGE_RULES = {
    "baby": {"basic"},
    "rookie": {"basic", "advanced", "disruptor", "support"},
    "champion": {"basic", "advanced", "disruptor", "support", "signature"},
    "final": {"basic", "advanced", "disruptor", "support", "signature", "ultimate", "mythic", "primacore"},
}


def load_all_abilities():
    ability_map = {}

    for folder in os.listdir(ABILITIES_ROOT):
        if folder in IGNORE_ABILITY_FOLDERS:
            continue

        folder_path = os.path.join(ABILITIES_ROOT, folder)
        if not os.path.isdir(folder_path):
            continue

        for file in os.listdir(folder_path):
            if not file.endswith(".json"):
                continue

            full_path = os.path.join(folder_path, file)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                continue

            ability = data.get("ability")
            if not ability:
                continue

            name = ability.get("name")
            ability_id = ability.get("id")

            if name and ability_id:
                ability_map[name] = {
                    "folder": folder,
                    "id": ability_id,
                    "path": full_path,
                }

    return ability_map


def extract_id_parts(ability_id):
    """Extract element, tier, name from ID: element.tier.name"""
    parts = ability_id.split(".")
    if len(parts) < 3:
        return None, None, None
    return parts[0], parts[1], ".".join(parts[2:])


def validate_cyberkin_file(path, stage, ability_map):
    errors = []
    missing = []

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    ck = data.get("cyberkin", {})
    name = ck.get("name", os.path.basename(path))
    element = ck.get("element", "core")

    abilities = ck.get("abilities", {})
    basic = abilities.get("basic", []) or []
    advanced = abilities.get("advanced", []) or []
    signature = abilities.get("signature")
    ultimate = abilities.get("ultimate")

    tier_groups = {
        "basic": basic,
        "advanced": advanced,
        "signature": [signature] if signature else [],
        "ultimate": [ultimate] if ultimate else []
    }

    # Missing ability detection
    for tier, ability_list in tier_groups.items():
        for ability_name in ability_list:
            if ability_name not in ability_map:
                errors.append(f"[ERROR] {name}: ability '{ability_name}' does not exist.")
                missing.append((ability_name, tier, element))

    # Stage eligibility + ID validation
    allowed = STAGE_RULES[stage]

    for tier, ability_list in tier_groups.items():
        for ability_name in ability_list:
            if ability_name not in ability_map:
                continue

            ability_id = ability_map[ability_name]["id"]
            id_element, id_tier, _ = extract_id_parts(ability_id)

            # Element mismatch
            if id_element != element:
                errors.append(
                    f"[ERROR] {name}: '{ability_name}' element mismatch. "
                    f"Cyberkin is '{element}', ability ID is '{id_element}'."
                )

            # Tier mismatch
            if id_tier != tier:
                errors.append(
                    f"[ERROR] {name}: '{ability_name}' tier mismatch. "
                    f"Cyberkin tier '{tier}', ability ID tier '{id_tier}'."
                )

            # Stage rule mismatch
            if id_tier not in allowed:
                errors.append(
                    f"[ERROR] {name}: '{ability_name}' is a {id_tier} ability but stage '{stage}' cannot use it."
                )

    # Signature/Ultimate rules
    if stage == "champion":
        if not signature:
            errors.append(f"[ERROR] {name}: Champion-stage Cyberkin must have exactly one signature ability.")
        if ultimate:
            errors.append(f"[ERROR] {name}: Champion-stage Cyberkin cannot have an ultimate ability.")

    if stage == "final":
        sig_count = 1 if signature else 0
        ult_count = 1 if ultimate else 0
        if sig_count + ult_count != 1:
            errors.append(
                f"[ERROR] {name}: Final-stage Cyberkin must have exactly one of: signature OR ultimate."
            )

    if stage in {"baby", "rookie"}:
        if signature:
            errors.append(f"[ERROR] {name}: {stage.capitalize()}-stage Cyberkin cannot have a signature ability.")
        if ultimate:
            errors.append(f"[ERROR] {name}: {stage.capitalize()}-stage Cyberkin cannot have an ultimate ability.")

    # Minimum move count
    valid_count = 0
    for tier, ability_list in tier_groups.items():
        for ability_name in ability_list:
            if ability_name in ability_map:
                valid_count += 1

    if valid_count < 2:
        errors.append(f"[ERROR] {name}: Cyberkin must have at least two valid abilities.")

    return name, errors, missing


def main():
    ability_map = load_all_abilities()

    folder_results = {}
    all_errors = []

    missing_abilities = set()
    missing_map = {}
    missing_tiers = {}
    missing_elements = {}

    for stage_folder in os.listdir(CYBERKIN_ROOT):
        if stage_folder in IGNORE_CYBERKIN_FOLDERS:
            continue

        stage_path = os.path.join(CYBERKIN_ROOT, stage_folder)
        if not os.path.isdir(stage_path):
            continue

        stage = stage_folder.lower()
        if stage not in STAGE_RULES:
            continue

        folder_results[stage] = {"failed": 0, "errors": 0}

        for file in os.listdir(stage_path):
            if not file.endswith(".json"):
                continue

            full_path = os.path.join(stage_path, file)
            name, errors, missing_list = validate_cyberkin_file(full_path, stage, ability_map)

            for ability_name, tier, element in missing_list:
                missing_abilities.add(ability_name)
                missing_map.setdefault(ability_name, set()).add(name)
                missing_tiers[ability_name] = tier
                missing_elements[ability_name] = element

            if errors:
                folder_results[stage]["failed"] += 1
                folder_results[stage]["errors"] += len(errors)
                all_errors.extend(errors)
            else:
                print(f"[OK] {name}")

    print("\n=== SUMMARY ===")
    for stage in ["baby", "rookie", "champion", "final"]:
        if stage in folder_results:
            failed = folder_results[stage]["failed"]
            err = folder_results[stage]["errors"]
            status = "PASS" if failed == 0 else "FAIL"
            print(f"{stage.capitalize()}: {status} ({failed} failed, {err} errors)")

    if all_errors:
        print("\n=== ERRORS ===")
        for e in all_errors:
            print(e)

    if missing_abilities:
        print("\n=== MISSING ABILITIES ===")
        for ability_name in sorted(missing_abilities):
            tier = missing_tiers[ability_name]
            element = missing_elements[ability_name]
            users = ", ".join(sorted(missing_map[ability_name]))
            print(f"{ability_name} — {tier} — {element} — used by: {users}")

        print("\n=== NAMES ONLY ===")
        for ability_name in sorted(missing_abilities):
            print(ability_name)

    sys.exit(1 if all_errors else 0)


if __name__ == "__main__":
    main()
