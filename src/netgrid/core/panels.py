class PanelRegistry:
    def __init__(self, panel_dict):
        self.panels = panel_dict

    def get(self, sector):
        return self.panels.get(sector)

    def list_sectors(self):
        return list(self.panels.keys())

    def list_files(self):
        return list(self.panels.values())
