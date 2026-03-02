class BattleManager:
    def __init__(self, team_a, team_b):
        self.team_a = team_a
        self.team_b = team_b

        # Turn counter for AI logging
        self.turn_number = 1

        # AI controller
        self.ai = AIController()

        # Battle log (developer only for now)
        self.log = []

    # ---------------------------------------------------------
    # TEAM HELPERS
    # ---------------------------------------------------------
    def get_team(self, entity):
        if entity in self.team_a:
            return self.team_a
        return self.team_b

    def get_opposing_team(self, entity):
        if entity in self.team_a:
            return [e for e in self.team_b if e.is_alive()]
        return [e for e in self.team_a if e.is_alive()]

    def all_entities(self):
        return self.team_a + self.team_b

    # ---------------------------------------------------------
    # MAIN BATTLE LOOP
    # ---------------------------------------------------------
    def start_battle(self):
        print("\n=== Battle Start ===")

        while True:
            # 1. Determine turn order (simple speed-based)
            turn_order = sorted(
                [e for e in self.all_entities() if e.is_alive()],
                key=lambda e: e.speed,
                reverse=True
            )

            print(f"\n--- Turn {self.turn_number} ---")

            # 2. Each entity takes a turn
            for entity in turn_order:
                if not entity.is_alive():
                    continue

                self.take_turn(entity)

                # Check for battle end
                if self.check_battle_end():
                    print("\n=== Battle End ===")
                    return self.get_winner()

            # 3. Tick cooldowns
            for entity in self.all_entities():
                entity.cooldowns.tick()

            # 4. Advance turn counter
            self.turn_number += 1

    # ---------------------------------------------------------
    # SINGLE TURN EXECUTION
    # ---------------------------------------------------------
    def take_turn(self, entity):
        # AI chooses ability + target
        ability, target = self.ai.choose_action(entity, self)

        if ability is None or target is None:
            print(f"[Turn] {entity.name} has no valid actions.")
            return

        print(f"[Turn] {entity.name} uses {ability.name} on {target.name}.")

        # Apply ability effects
        self.execute_ability(entity, target, ability)

        # Apply cooldown
        entity.cooldowns.apply_cooldown(ability)

    # ---------------------------------------------------------
    # ABILITY EXECUTION
    # ---------------------------------------------------------
    def execute_ability(self, user, target, ability):
        # Damage abilities
        if ability.is_attack:
            damage = ability.power
            target.apply_damage(damage)
            print(f"[Damage] {target.name} takes {damage} damage ({target.current_hp}/{target.max_hp}).")

        # Support abilities
        if ability.is_support:
            if "stat_modifiers" in ability.effects:
                for stat, value in ability.effects["stat_modifiers"].items():
                    target.apply_stat_modifier(stat, 1 + (value / 100))
                    print(f"[Buff] {target.name}'s {stat} modified by {value}%.")

            if "heal_percent" in ability.effects:
                heal_amount = target.max_hp * ability.effects["heal_percent"]
                target.heal(heal_amount)
                print(f"[Heal] {target.name} heals {heal_amount} HP.")

        # Status effects (future expansion)
        # if ability.status_effects:
        #     ...

        # KO check
        if not target.is_alive():
            print(f"[KO] {target.name} has been defeated!")

    # ---------------------------------------------------------
    # BATTLE END CHECK
    # ---------------------------------------------------------
    def check_battle_end(self):
        alive_a = any(e.is_alive() for e in self.team_a)
        alive_b = any(e.is_alive() for e in self.team_b)
        return not (alive_a and alive_b)

    def get_winner(self):
        alive_a = any(e.is_alive() for e in self.team_a)
        alive_b = any(e.is_alive() for e in self.team_b)

        if alive_a and not alive_b:
            return "Team A wins"
        if alive_b and not alive_a:
            return "Team B wins"
        return "Draw"
