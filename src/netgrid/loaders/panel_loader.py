import json
import os

ASSET_DIR = "src/netgrid/assets/panels"

def load_panels(panel_map_path):
    with open(panel_map_path, "r") as f:
        mapping = json.load(f)

    panels = {}

    for sector, filename in mapping.items():
        full_path = os.path.join(ASSET_DIR, filename)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Panel image missing: {full_path}")

        panels[sector] = full_path

    return panels
