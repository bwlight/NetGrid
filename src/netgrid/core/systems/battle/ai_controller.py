from __future__ import annotations

from typing import List, Dict, Any, Optional

from netgrid.core.systems.battle import ability_loader
from .battle_entity import BattleEntity
from netgrid.core.ai.ai_config_loader import AIConfigLoader



class AIController:
    """
    Advanced tactical AI for BattleEntity combatants.
    Fully data-driven using ai_config.json.
    Supports:
    - Roles (aggressive, defensive, support, chaotic, smart)
    - Personalities (brave, cautious, chaotic, loyal, vengeful, neutral)
    - Threat system (aggro tables)
    - Ability scoring (damage, healing, control, cooldown, cost)
    - Smart targeting (kill thresholds, threat, biggest threat)
    """

class AIController:
    def __init__(self, config_loader, role_id="neutral", personality_id="neutral"):
        self.config = config_loader
        self.role_id = role_id
        self.personality_id = personality_id

        # Load role config (optional but future-proof)
        self.role = getattr(self.config, "roles", {}).get(self.role_id, {})

        # Load personality config (THIS FIXES THE CRASH)
        if hasattr(self.config, "get_personality"):
            self.personality = self.config.get_personality(self.personality_id)
        else:
            # Fallback if loader exposes personalities as a dict
            personalities = getattr(self.config, "personalities", {})
            self.personality = personalities.get(self.personality_id, {})


    # ---------------------------------------------------------
    # PUBLIC ENTRY POINTS
    # ---------------------------------------------------------

    def choose_target(
        self,
        user: BattleEntity,
        entities: List[BattleEntity],
    ) -> Optional[BattleEntity]:

        enemies = [e for e in entities if e is not user and e.is_alive()]
        if not enemies:
            return None

        # Smart role uses advanced targeting
        if user.role == "smart":
            return self._smart_target(user, enemies)

        # Threat-based targeting
        threat_target = self._choose_by_threat(user, enemies)
        if threat_target:
            return threat_target

        # Role-based targeting from config
        role_cfg = self.config.get_role(user.role)
        targeting = role_cfg.get("targeting", "first")

        if targeting == "highest_hp":
            return self._choose_highest_hp(enemies)
        if targeting == "lowest_hp":
            return self._choose_lowest_hp(enemies)
        if targeting == "biggest_threat":
            return self._choose_biggest_threat(enemies)
        if targeting == "random":
            return enemies[0]  # placeholder for randomness

        # Fallback
        return enemies[0]

    def choose_ability(self, attacker, defender, ability_loader):
        ability_ids = getattr(attacker, "abilities", []) or []
        if not ability_ids:
            return None

        # Filter out abilities that don't exist
        valid_ids = []
        for ability_id in ability_ids:
            try:
                ability_loader.get(ability_id)
                valid_ids.append(ability_id)
            except KeyError:
                continue

        if not valid_ids:
            return None

        best_score = -9999
        best_ability = valid_ids[0]

        # Pull AI config attributes safely
        role_cfg = getattr(self.config, "ability_bias", {})
        randomness_factor = getattr(self.personality, "randomness", 0.1)

        for ability_id in valid_ids:
            ability = ability_loader.get(ability_id)

            # Power-based scoring
            score = getattr(ability, "power", 0)

            # Role bias
            ability_type = getattr(ability, "type", "damage")
            score *= role_cfg.get(ability_type, 1.0)

            # Randomness
            import random
            score += random.uniform(-randomness_factor, randomness_factor)

            if score > best_score:
                best_score = score
                best_ability = ability_id

        return best_ability




    # ---------------------------------------------------------
    # THREAT SYSTEM
    # ---------------------------------------------------------

    def add_threat(self, source: BattleEntity, target: BattleEntity, amount: float) -> None:
        current = target.threat.get(source.id, 0.0)
        target.threat[source.id] = current + amount

    def _choose_by_threat(
        self,
        user: BattleEntity,
        enemies: List[BattleEntity],
    ) -> Optional[BattleEntity]:

        best = None
        best_value = 0.0

        for enemy in enemies:
            value = enemy.threat.get(user.id, 0.0)
            if value > best_value:
                best_value = value
                best = enemy

        return best

    # ---------------------------------------------------------
    # ROLE-BASED TARGETING HELPERS
    # ---------------------------------------------------------

    def _choose_highest_hp(self, enemies: List[BattleEntity]) -> BattleEntity:
        return max(enemies, key=lambda e: e.current_hp)

    def _choose_lowest_hp(self, enemies: List[BattleEntity]) -> BattleEntity:
        return min(enemies, key=lambda e: e.current_hp)

    def _choose_biggest_threat(self, enemies: List[BattleEntity]) -> BattleEntity:
        return max(enemies, key=lambda e: e.stats.get("attack", 1))

    # ---------------------------------------------------------
    # SMART TARGETING
    # ---------------------------------------------------------

    def _smart_target(self, user: BattleEntity, enemies: List[BattleEntity]) -> BattleEntity:
        # 1. Try to finish off low HP enemies
        killable = [
            e for e in enemies
            if e.current_hp < user.stats.get("attack", 1) * 2
        ]
        if killable:
            return min(killable, key=lambda e: e.current_hp)

        # 2. Threat-based targeting
        threat_target = self._choose_by_threat(user, enemies)
        if threat_target:
            return threat_target

        # 3. Target highest damage dealer
        return max(enemies, key=lambda e: e.stats.get("attack", 1))

    # ---------------------------------------------------------
    # ABILITY SCORING
    # ---------------------------------------------------------

    def _score_ability(self, user: BattleEntity, ability: Dict[str, Any]) -> float:
        scoring = self.config.get_ability_scoring()
        score = 0.0

        # Damage
        if "damage" in ability:
            score += ability["damage"] * scoring.get("damage_weight", 2.0)

        # Healing
        if "heal" in ability:
            score += ability["heal"] * scoring.get("heal_weight", 1.5)

        # Status effects
        if "status" in ability:
            status = ability["status"]
            etype = getattr(status, "effect_type", "")

            status_weights = scoring.get("status_weights", {})
            score += status_weights.get(etype, 0.0)

        # Cooldown
        score += ability.get("cooldown", 0) * scoring.get("cooldown_weight", 0.5)

        # Energy cost penalty
        score -= ability.get("energy_cost", 0) * scoring.get("energy_cost_penalty", 0.5)

        # Apply role and personality modifiers
        score = self._apply_role_bias(user, score, ability)
        score = self._apply_personality_bias(user, score, ability)

        return score

    # ---------------------------------------------------------
    # ROLE BIAS
    # ---------------------------------------------------------

    def _apply_role_bias(self, user: BattleEntity, score: float, ability: Dict[str, Any]) -> float:
        role_cfg = self.config.get_role(user.role)
        bias = role_cfg.get("ability_bias", {})

        if "damage" in ability:
            score *= bias.get("damage_multiplier", 1.0)
        if "heal" in ability:
            score *= bias.get("heal_multiplier", 1.0)
        if "status" in ability:
            etype = ability["status"].effect_type
            if etype == "buff":
                score *= bias.get("buff_multiplier", 1.0)
            if etype == "debuff":
                score *= bias.get("debuff_multiplier", 1.0)

        # Smart AI cooldown bonus
        if user.role == "smart":
            score += ability.get("cooldown", 0) * bias.get("cooldown_bonus", 0.0)

        return score

    # ---------------------------------------------------------
    # PERSONALITY BIAS
    # ---------------------------------------------------------

    def _apply_personality_bias(self, user: BattleEntity, score: float, ability: Dict[str, Any]) -> float:
        p_cfg = self.config.get_personality(user.personality)
        bias = p_cfg.get("bias", {})

        if "damage" in ability:
            score *= bias.get("damage_multiplier", 1.0)
        if "heal" in ability:
            score *= bias.get("heal_multiplier", 1.0)
        if "status" in ability:
            etype = ability["status"].effect_type
            if etype == "buff":
                score *= bias.get("buff_multiplier", 1.0)

        return score
