import json
import os

GLYPH_DIR = "src/netgrid/assets/glyphs"

def load_glyphs(sector_file_path):
    with open(sector_file_path, "r") as f:
        sectors = json.load(f)

    glyphs = {}

    for sector, data in sectors.items():
        filename = data.get("glyph")
        if not filename:
            continue

        full_path = os.path.join(GLYPH_DIR, filename)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Missing glyph file: {full_path}")

        glyphs[sector] = full_path

    return glyphs
