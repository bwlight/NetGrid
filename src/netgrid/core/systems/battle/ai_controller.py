#version 4.0 - 3/2/26
class AIController:
    def __init__(self):
        # Threat memory persists across turns
        self.threat_table = {}  # { entity_id: { target_id: threat_value } }

    # ---------------------------------------------------------
    # MAIN ENTRY POINT
    # ---------------------------------------------------------
    def choose_action(self, entity, battle):
        cyberkin = entity.cyberkin
        turn = getattr(battle, "turn_number", None)

        # Ensure threat table exists for this entity
        if entity.id not in self.threat_table:
            self.threat_table[entity.id] = {}

        # Track previous phase
        previous_phase = cyberkin.active_ai_phase

        # 1. Evaluate phase
        phase = self.evaluate_phase(entity)
        new_phase = phase["name"] if phase else None

        # 2. Developer-only phase transition logging
        if new_phase != previous_phase:
            if previous_phase is None and new_phase is not None:
                msg = f"Turn {turn}: Entered phase '{new_phase}'."
            elif previous_phase is not None and new_phase is None:
                msg = f"Turn {turn}: Exited phase '{previous_phase}'."
            else:
                msg = f"Turn {turn}: Transitioned {previous_phase} → {new_phase}."

            print(f"[AI][Phase] {cyberkin.id} {msg}")
            cyberkin.ai_warnings.append(msg)

        cyberkin.active_ai_phase = new_phase

        # 3. Determine effective role/personality/modifiers
        role = phase["role"] if phase and phase.get("role") else cyberkin.ai_role
        personality = (
            phase["personality"]
            if phase and phase.get("personality")
            else cyberkin.ai_personality
        )

        # Merge base + phase modifiers
        modifiers = dict(cyberkin.ai_modifiers)
        if phase:
            for k, v in phase["behavior_modifiers"].items():
                modifiers[k] = v

        # 4. Score abilities (cooldown-aware + tag-aware)
        ability_scores = self.score_abilities(entity, battle, role, personality, modifiers)

        if not ability_scores:
            return None, None

        chosen_ability = max(ability_scores, key=lambda a: ability_scores[a])

        # 5. Pick target (based on ability.target + threat + kill logic)
        target = self.choose_target(entity, battle, chosen_ability, role, personality, modifiers)

        # 6. Update threat memory
        if target:
            self.add_threat(entity, target, amount=5)

        return chosen_ability, target

    # ---------------------------------------------------------
    # PHASE EVALUATION
    # ---------------------------------------------------------
    def evaluate_phase(self, entity):
        cyberkin = entity.cyberkin
        hp_ratio = entity.current_hp / entity.max_hp

        for phase in cyberkin.ai_phases:
            trigger = phase.get("trigger", {})

            if "hp_below" in trigger:
                if hp_ratio <= trigger["hp_below"]:
                    return phase

        return None

    # ---------------------------------------------------------
    # ABILITY SCORING (role, personality, modifiers, cooldowns, tags)
    # ---------------------------------------------------------
    def score_abilities(self, entity, battle, role, personality, modifiers):
        scores = {}

        for ability in entity.abilities:
            # Skip abilities on cooldown
            if entity.cooldowns.is_on_cooldown(ability.id):
                continue

            base = 1.0

            # -------------------------
            # Role scoring
            # -------------------------
            if role == "aggressive":
                base *= modifiers.get("damage_mult", 1.0)
            if role == "control":
                base *= modifiers.get("control_focus_mult", 1.0)
            if role == "purifier":
                base *= modifiers.get("dot_focus_mult", 1.0)
            if role == "tank":
                base *= modifiers.get("tank_focus_mult", 1.0)

            # -------------------------
            # Personality scoring
            # -------------------------
            if personality == "brave":
                base *= 1.15
            elif personality == "cautious":
                base *= 0.85
            elif personality == "chaotic":
                base *= 1.25

            # -------------------------
            # Tag-based scoring
            # -------------------------
            tags = ability.tags

            if "buff" in tags:
                base *= 1.2
            if "heal" in tags:
                base *= 1.3
            if "debuff" in tags:
                base *= 1.15
            if "status" in tags:
                base *= 1.25
            if "control" in tags and role == "control":
                base *= 1.4
            if "multi_hit" in tags:
                base *= 1.1
            if "high_damage" in tags:
                base *= 1.2
            if "finisher" in tags:
                base *= 1.5

            # -------------------------
            # Power scaling
            # -------------------------
            base *= (1 + ability.power / 100)

            scores[ability] = base

        return scores

    # ---------------------------------------------------------
    # TARGET SELECTION (ability.target + threat + kill logic + role logic)
    # ---------------------------------------------------------
def choose_target(self, entity, battle, ability, role, personality, modifiers):
    # Self-targeting
    if ability.target == "self":
        return entity

    # Multi-target abilities return a LIST of targets
    if ability.target == "multi_enemy":
        return battle.get_opposing_team(entity)

    if ability.target == "multi_ally":
        return battle.get_team(entity)

    if ability.target == "multi_all":
        return battle.all_entities()

    # Ally targeting
    if ability.target == "ally":
        allies = battle.get_team(entity)
        return min(allies, key=lambda a: a.current_hp / a.max_hp)

    # Enemy targeting (single)
    enemies = battle.get_opposing_team(entity)
    if not enemies:
        return None

    # Kill threshold logic
    kill_targets = [e for e in enemies if e.current_hp <= e.max_hp * 0.25]
    if kill_targets:
        return min(kill_targets, key=lambda e: e.current_hp)

    # Threat-based targeting
    threat_table = self.threat_table[entity.id]
    if threat_table:
        highest_threat = max(threat_table, key=lambda tid: threat_table[tid])
        for e in enemies:
            if e.id == highest_threat:
                return e

    # Role-based targeting
    if role == "aggressive":
        return min(enemies, key=lambda e: e.current_hp)
    if role == "defensive":
        return max(enemies, key=lambda e: e.current_hp)
    if role == "control":
        return max(enemies, key=lambda e: e.speed)

    return enemies[0]


    # ---------------------------------------------------------
    # THREAT SYSTEM
    # ---------------------------------------------------------
    def add_threat(self, entity, target, amount):
        table = self.threat_table[entity.id]
        table[target.id] = table.get(target.id, 0) + amount
