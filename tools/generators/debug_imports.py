print("Trying to import netgrid...")
import netgrid
print("Imported netgrid OK")

print("Trying battle system...")
from netgrid.core.systems.battle import BattleManager
print("Battle system OK")

print("Trying cyberkin...")
from netgrid.core.models.cyberkin import Cyberkin, CyberkinLoader
print("Cyberkin OK")

print("Trying ability loader...")
from netgrid.core.systems.battle import AbilityLoader
print("AbilityLoader OK")

