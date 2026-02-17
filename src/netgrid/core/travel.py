import json
from collections import defaultdict, deque
import datetime
from tracemalloc import start
import random

class TravelSystem:
    def __init__(self, travel_map_path):
        with open(travel_map_path, "r") as f:
            data = json.load(f)

        # Load all sections
        self.routes = data.get("routes", [])
        self.connections = data.get("connections", {})
        self.path_types = data.get("path_types", {})
        self.travel_rules = data.get("travel_rules", {})
        self.events = data.get("events", {})
        self.ui_data = data.get("ui_data", {})


        # Load restrictions
        self.restrictions = data.get("restrictions", {})
        self.requires_item = self.restrictions.get("requires_item", {})
        self.min_corruption = self.restrictions.get("min_corruption_level", {})
        self.blocked_paths = set(self.restrictions.get("blocked_paths", []))
        self.requires_flag = self.restrictions.get("requires_flag", {})
        self.time_constraints = self.restrictions.get("time_constraints", {})
        self.cost_modifiers = data.get("cost_modifiers", {})


        # Build a unified graph with cost + stability
        self.graph = defaultdict(list)

        # 1. Load explicit routes
        for r in self.routes:
            self.graph[r["from"]].append({
                "to": r["to"],
                "cost": r.get("cost", self.default_cost(r["type"])),
                "stable": r.get("stable", self.default_stability(r["type"]))
            })

        # 2. Load simple connections (fallback)
        for node, neighbors in self.connections.items():
            for n in neighbors:
                key = f"{node}->{n}"
                path_type = self.path_types.get(key, "stable")

                # Add forward edge
                self.graph[node].append({
                    "to": n,
                    "cost": self.default_cost(path_type),
                    "stable": (path_type == "stable")
                })

        # If it's a GATE route, add reverse edge
                if node.startswith("GATE_") and n.startswith("GATE_"):
                    reverse_key = f"{n}->{node}"
                    reverse_type = self.path_types.get(reverse_key, path_type)

                    self.graph[n].append({
                        "to": node,
                        "cost": self.default_cost(reverse_type),
                        "stable": (reverse_type == "stable")
                    })

    def default_cost(self, route_type):
        if route_type == "gate":
            return self.travel_rules.get("gate_cost", 1)
        if route_type == "stream":
            return self.travel_rules.get("stream_cost", 2)
        return 1

    def default_stability(self, route_type):
        if route_type == "gate":
            return self.travel_rules.get("gate_stability", True)
        if route_type == "stream":
            return self.travel_rules.get("stream_stability", False)
        return True

    def _time_in_range(self, start, end, current):
        """Handles ranges that cross midnight."""
        if start <= end:
            return start <= current <= end
        else:
            return current >= start or current <= end
        
    def check_events(self, start, end):
        key = f"{start}->{end}"
        if key not in self.events:
            return []

        triggered = []
        for event in self.events[key]:
            if random.randint(1, 100) <= event.get("chance", 0):
                triggered.append(event)
        return triggered


    def can_travel(self, start, end, inventory=None, corruption_level=0, flags=None, current_time=None):
        key = f"{start}->{end}"

        # 1. Blocked paths
        if key in self.blocked_paths:
            return False

        # 2. Item requirement
        if key in self.requires_item:
            required = self.requires_item[key]
            if not inventory or required not in inventory:
                return False

        # 3. Corruption requirement
        if key in self.min_corruption:
            if corruption_level < self.min_corruption[key]:
                return False

        # 4. Flag requirement
        if key in self.requires_flag:
            required_flag = self.requires_flag[key]
            if not flags or not flags.get(required_flag, False):
                return False

        # 5. Time constraints
        if key in self.time_constraints:
            tc = self.time_constraints[key]

            start_t = datetime.datetime.strptime(tc["start_time"], "%H:%M").time()
            end_t = datetime.datetime.strptime(tc["end_time"], "%H:%M").time()

            if current_time is None:
                return False  # must provide time

            if not self._time_in_range(start_t, end_t, current_time):
                return False

        # 6. Normal travel rules
        return any(edge["to"] == end for edge in self.graph[start])

    def get_ui_data(self, start, end):
        return self.ui_data.get(f"{start}->{end}", {})


    def travel_cost(self, start, end, corruption_level=0, time_of_day=None, weather=None):
        base_cost = None
        for edge in self.graph[start]:
            if edge["to"] == end:
                base_cost = edge["cost"]
                break

        if base_cost is None:
            return None

        cost = base_cost

        # Corruption modifiers
        if "corruption_level" in self.cost_modifiers:
            for rule in self.cost_modifiers["corruption_level"]["thresholds"]:
                if corruption_level >= rule["min"]:
                    cost *= rule["cost_multiplier"]

        # Time of day
        if time_of_day and "time_of_day" in self.cost_modifiers:
            if time_of_day in self.cost_modifiers["time_of_day"]:
                cost *= self.cost_modifiers["time_of_day"][time_of_day]

        # Weather
        if weather and "weather" in self.cost_modifiers:
            if weather in self.cost_modifiers["weather"]:
                cost *= self.cost_modifiers["weather"][weather]

        return round(cost, 2)


    def find_path(self, start, end):
        queue = deque([[start]])
        visited = set()

        while queue:
            path = queue.popleft()
            node = path[-1]

            if node == end:
                return path

            if node in visited:
                continue

            visited.add(node)

            for edge in self.graph[node]:
                new_path = path + [edge["to"]]
                queue.append(new_path)

        return None
    
    def preview_route(self, start, end, inventory=None, corruption_level=0, flags=None, time_of_day=None, weather=None, current_time=None):
        key = f"{start}->{end}"

        preview = {
            "start": start,
            "end": end,
            "can_travel": self.can_travel(start, end, inventory, corruption_level, flags, current_time),
            "cost": self.travel_cost(start, end, corruption_level, time_of_day, weather),
            "ui": self.get_ui_data(start, end),
            "events": self.events.get(key, []),
            "requirements": {
                "item": self.requires_item.get(key),
                "corruption": self.min_corruption.get(key),
                "flag": self.requires_flag.get(key),
                "time_window": self.time_constraints.get(key)
            }
        }

        return preview
