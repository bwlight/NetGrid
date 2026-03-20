# ai_controller.py

from typing import List, Tuple, Optional
import random
from .battle_entity import BattleEntity

class AIController:
    """
    Tactical AI for Cyberkin.
    Evaluates abilities using:
    - role (attacker, tank, support, disruptor)
    - personality (brave, cautious, chaotic, vengeful, loyal, neutral)
    - threat tables
    - cooldowns
    - statuses
    - stat modifiers
    - multi-hit potential
    """

    def __init__(self, rng: Optional[random.Random] = None, dev_log=None):
        self.rng = rng or random.Random()
        self.dev_log = dev_log or (lambda msg: None)

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def choose_action(self, actor, entities, battle_manager) -> Tuple[Optional[dict], List["BattleEntity"]]:
        """
        Returns (ability, targets).
        """
        if not actor.is_alive():
            return None, []

        abilities = actor.abilities
        if not abilities:
            return None, []

        scored = []

        for ability in abilities:
            if not actor.is_ability_available(ability["id"]):
                continue

            targets = self._get_valid_targets(actor, entities, ability)
            if not targets:
                continue

            score = self._score_ability(actor, ability, targets, battle_manager)
            scored.append((score, ability, targets))

        if not scored:
            return None, []

        scored.sort(key=lambda x: x[0], reverse=True)
        best_score, best_ability, best_targets = scored[0]

        self.dev_log(f"AI: {actor.debug_name} selects {best_ability['name']} (score {best_score:.2f})")
        return best_ability, best_targets

    # -------------------------------------------------------------------------
    # Target Selection
    # -------------------------------------------------------------------------

    def _get_valid_targets(self, actor, entities, ability) -> List["BattleEntity"]:
        target_type = ability.get("target", "enemy")

        if target_type == "self":
            return [actor]

        actor_team = getattr(actor.cyberkin, "team", "A")

        if target_type == "enemy":
            return [e for e in entities if e.is_alive() and getattr(e.cyberkin, "team", "A") != actor_team]

        if target_type == "ally":
            return [e for e in entities if e.is_alive() and getattr(e.cyberkin, "team", "A") == actor_team]

        if target_type == "area":
            return [e for e in entities if e.is_alive()]

        return []

    # -------------------------------------------------------------------------
    # Ability Scoring
    # -------------------------------------------------------------------------

    def _score_ability(self, actor, ability, targets, battle_manager) -> float:
        """
        Produces a numeric score representing how desirable the ability is.
        Factors:
        - role
        - personality
        - damage potential
        - multi-hit potential
        - status application
        - stat modifiers
        - threat
        - target HP
        """
        score = 0.0
        role = actor.role
        personality = actor.personality

        # Damage scoring
        if ability["type"] == "attack" and ability["power"]:
            for t in targets:
                dmg = battle_manager.calculate_damage(actor, t, ability)
                score += dmg * 0.5

                # Multi-hit bonus
                if ability.get("multi_hit"):
                    min_h = ability["multi_hit"]["min"]
                    max_h = ability["multi_hit"]["max"]
                    avg_hits = (min_h + max_h) / 2
                    score += dmg * (avg_hits - 1) * 0.3

                # Low HP kill bonus
                if t.current_hp <= dmg:
                    score += 25

                # Threat bonus
                threat = actor.get_threat(t.entity_id)
                score += threat * 0.2

        # Support scoring
        if ability["type"] == "support":
            mods = ability.get("stat_modifiers") or {}
            for stat, val in mods.items():
                if stat in ("atk", "spd", "crt"):
                    score += val * 100
                if stat in ("def", "res"):
                    score += val * 80
                if stat == "int":
                    score += val * 60

        # Status scoring
        status_id = ability.get("status_inflict")
        if status_id:
            score += 15
            if ability.get("status_chance", 0) < 1.0:
                score *= ability["status_chance"]

        # Role adjustments
        if role == "attacker":
            score *= 1.2
        elif role == "tank":
            if ability["type"] == "support":
                score *= 1.3
        elif role == "support":
            if ability["type"] == "support":
                score *= 1.5
        elif role == "disruptor":
            if status_id:
                score *= 1.4

        # Personality adjustments
        if personality == "brave":
            score *= 1.15
        elif personality == "cautious":
            if ability["type"] == "support":
                score *= 1.25
        elif personality == "chaotic":
            score *= self.rng.uniform(0.8, 1.2)
        elif personality == "vengeful":
            # Bonus for targeting high-threat enemies
            for t in targets:
                score += actor.get_threat(t.entity_id) * 0.5
        elif personality == "loyal":
            if ability["target"] == "ally":
                score *= 1.3

        return score
