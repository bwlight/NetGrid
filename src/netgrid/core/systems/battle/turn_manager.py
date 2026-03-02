class TurnManager:
    def __init__(self):
        self.turn_order = []
        self.index = 0

    def initialize(self, entities):
        # Sort by speed descending
        self.turn_order = sorted(entities, key=lambda e: e.speed, reverse=True)
        self.index = 0

    def next(self):
        if not self.turn_order:
            return None

        entity = self.turn_order[self.index]
        self.index = (self.index + 1) % len(self.turn_order)
        return entity

    def get_turn_order(self):
        return self.turn_order
