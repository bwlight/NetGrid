import json
from netgrid.core.models.cyberkin.cyberkin import Cyberkin
from src.netgrid.core.loaders.ai_behavior_loader import AIBehaviorLoader

# Load the JSON
with open("data/cyberkin/EMBERBIT.json", "r") as f:
    data = json.load(f)

# Create Cyberkin object
c = Cyberkin(id=data["id"])

# Create loader
loader = AIBehaviorLoader("schemas/ai_behavior.schema.json")

# Apply AI behavior
loader.apply(data, c)

# Print results
print("\n=== Final AI Behavior ===")
print(c.ai)

print("\n=== Direct Attributes ===")
print("Role:", c.ai_role)
print("Personality:", c.ai_personality)
print("Tags:", c.role_tags)
print("Modifiers:", c.ai_modifiers)
print("Phases:", c.ai_phases)
print("Active Phase:", c.active_ai_phase)

print("\n=== Warnings ===")
for w in c.ai_warnings:
    print("-", w)
