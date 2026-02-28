# Netgrid loaders package - this package contains the core functionality for loading various game assets and data in the NetGrid engine. The loaders are responsible for parsing and loading data from various sources, such as files or databases, and converting it into usable objects and structures within the game. This package includes loaders for glyphs, panels, sectors, status effects, and travel mechanics, among others. The loaders are designed to be modular and extensible, allowing for easy addition of new loaders as the game evolves. They serve as an essential component of the NetGrid experience, ensuring that game data is efficiently loaded and managed for a seamless gameplay experience.

# src/netgrid/core/loaders/__init__.py

from .glyph_loader import GlyphLoader
from .panel_loader import PanelLoader
from .sector_loader import SectorLoader
from .status_loader import StatusLoader
from .travel_loader import TravelLoader
