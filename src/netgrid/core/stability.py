from __future__ import annotations


class StabilitySystem:
    """
    Tracks Cyberkin stability (corruption, overclocking, glitches).
    Stability affects:
    - crit chance
    - damage output
    - status susceptibility
    - evolution paths
    """

    def __init__(self, max_stability: int = 100):
        self.max_stability = max_stability

    def apply_stress(self, cyberkin, amount: int):
        cyberkin.stability = min(self.max_stability, cyberkin.stability + amount)

    def reduce_stress(self, cyberkin, amount: int):
        cyberkin.stability = max(0, cyberkin.stability - amount)

    def get_state(self, cyberkin) -> str:
        s = cyberkin.stability

        if s < 20:
            return "stable"
        if s < 50:
            return "strained"
        if s < 80:
            return "unstable"
        return "critical"
