import json
from pathlib import Path
from typing import Dict, Any, Set, List


class EvolutionDebugger:
    """
    Debug tool for validating evolution data across all families.
    Checks for:
    - Missing links
    - Circular evolutions
    - Unreachable forms
    - Reverse mapping correctness
    - Pretty-printed evolution chains
    """

    def __init__(self, evolution_data: Dict[str, Any]):
        self.data = evolution_data

    # ---------------------------------------------------------
    # 1. Detect Missing Links
    # ---------------------------------------------------------
    def find_missing_links(self) -> List[str]:
        missing = []
        for species, evo in self.data.items():
            if "into" in evo:
                target = evo["into"]
                if target not in self.data:
                    missing.append(f"{species} → {target} (missing)")
            if "branches" in evo:
                for branch in evo["branches"]:
                    target = branch["into"]
                    if target not in self.data:
                        missing.append(f"{species} → {target} (missing)")
        return missing

    # ---------------------------------------------------------
    # 2. Detect Circular Evolutions
    # ---------------------------------------------------------
    def detect_cycles(self) -> List[List[str]]:
        visited = set()
        stack = []
        cycles = []

        def dfs(node: str):
            if node in stack:
                cycle_start = stack.index(node)
                cycles.append(stack[cycle_start:] + [node])
                return

            if node in visited:
                return

            visited.add(node)
            stack.append(node)

            evo = self.data.get(node, {})
            targets = []

            if "into" in evo:
                targets.append(evo["into"])
            if "branches" in evo:
                for b in evo["branches"]:
                    targets.append(b["into"])

            for t in targets:
                if t in self.data:
                    dfs(t)

            stack.pop()

        for species in self.data.keys():
            dfs(species)

        return cycles

    # ---------------------------------------------------------
    # 3. Detect Unreachable Forms
    # ---------------------------------------------------------
    def find_unreachable(self) -> Set[str]:
        reachable = set()

        def mark_reachable(node: str):
            if node in reachable:
                return
            reachable.add(node)

            evo = self.data.get(node, {})
            if "into" in evo:
                mark_reachable(evo["into"])
            if "branches" in evo:
                for b in evo["branches"]:
                    mark_reachable(b["into"])

        # Start from all baby forms
        for species in self.data:
            if species.endswith("_baby"):
                mark_reachable(species)

        unreachable = set(self.data.keys()) - reachable
        return unreachable

    # ---------------------------------------------------------
    # 4. Pretty Print Evolution Chains
    # ---------------------------------------------------------
    def print_chains(self):
        def print_chain(species: str, indent: int = 0):
            print("  " * indent + f"- {species}")
            evo = self.data.get(species, {})

            if "into" in evo:
                print_chain(evo["into"], indent + 1)

            if "branches" in evo:
                for b in evo["branches"]:
                    print_chain(b["into"], indent + 1)

        for species in sorted(self.data.keys()):
            if species.endswith("_baby"):
                print(f"\n=== Evolution Chain for {species} ===")
                print_chain(species)

    # ---------------------------------------------------------
    # 5. Validate Reverse Map
    # ---------------------------------------------------------
    def validate_reverse_map(self, reverse_map: Dict[str, List[str]]) -> List[str]:
        errors = []

        for final_form, chain in reverse_map.items():
            if final_form not in self.data:
                errors.append(f"{final_form} not found in evolution data")
                continue

            for ancestor in chain:
                if ancestor not in self.data:
                    errors.append(f"{final_form} → {ancestor} (missing ancestor)")

        return errors


# ---------------------------------------------------------
# Load evolution data from /families folder
# ---------------------------------------------------------
def load_evolution_folder(base_folder: str) -> Dict[str, Any]:
    base = Path(base_folder)
    families_folder = base / "families"

    if not families_folder.exists():
        raise FileNotFoundError(f"Missing folder: {families_folder}")

    merged = {}

    for file in families_folder.glob("evolution_*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for k, v in data.items():
                if k in merged:
                    raise ValueError(f"Duplicate species ID: {k}")
                merged[k] = v

    return merged


# ---------------------------------------------------------
# Example usage
# ---------------------------------------------------------
if __name__ == "__main__":
    evo_data = load_evolution_folder("src/netgrid/core/systems/evolution")
    debugger = EvolutionDebugger(evo_data)

    print("\n=== Missing Links ===")
    print(debugger.find_missing_links())

    print("\n=== Cycles ===")
    print(debugger.detect_cycles())

    print("\n=== Unreachable Forms ===")
    print(debugger.find_unreachable())

    print("\n=== Evolution Chains ===")
    debugger.print_chains()

    # ---------------------------------------------------------
    # Reverse Map Validation
    # ---------------------------------------------------------
    reverse_map_path = (
        "src/netgrid/core/systems/evolution/maps/reverse_evolution_map.json"
    )

    if Path(reverse_map_path).exists():
        with open(reverse_map_path, "r", encoding="utf-8") as f:
            reverse_map = json.load(f)

        print("\n=== Reverse Map Validation ===")
        print(debugger.validate_reverse_map(reverse_map))
    else:
        print("\nReverse map not found. Skipping validation.")
