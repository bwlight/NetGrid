from netgrid.core.loaders.panel_loader import load_panels
from netgrid.core.loaders.glyph_loader import load_glyphs
from netgrid.core.panels import PanelRegistry
from netgrid.core.glyphs import GlyphRegistry

class AssetManager:
    def __init__(self, panel_map_path, sector_file_path):
        # Load panels
        panel_dict = load_panels(panel_map_path)
        self.panels = PanelRegistry(panel_dict)

        # Load glyphs
        glyph_dict = load_glyphs(sector_file_path)
        self.glyphs = GlyphRegistry(glyph_dict)

    def get_panel(self, sector):
        return self.panels.get(sector)

    def get_glyph(self, sector):
        return self.glyphs.get(sector)
    
    def list_glyph_sectors(self):
        return self.glyphs.list_sectors()

    def list_panel_sectors(self):    
        return self.panels.list_sectors()  