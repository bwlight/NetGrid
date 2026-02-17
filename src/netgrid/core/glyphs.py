class GlyphRegistry:
    def __init__(self, glyph_dict):
        self.glyphs = glyph_dict

    def get(self, sector):
        return self.glyphs.get(sector)

    def list_sectors(self):
        return list(self.glyphs.keys())

    def list_files(self):
        return list(self.glyphs.values())
