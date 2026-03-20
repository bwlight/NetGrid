# Expose subsystems as namespaces for easier access and organization. Systems include battle management, party management, and other core game mechanics. Each system is designed to be modular and extensible, allowing for easy addition of new features and mechanics as the game evolves. This structure helps maintain a clean and organized codebase while providing a clear separation of concerns between different aspects of the game.

# src/netgrid/core/systems/__init__.py

from .battle import (
    BattleManager,
    BattleEntity,
    AbilityManager,
    AbilityLoader,
    AIController,
    AIConfigLoader,
    StatusEngine,
    StatusEffect,
    CooldownManager,
    TurnManager,
)

from .party import PartyManager
