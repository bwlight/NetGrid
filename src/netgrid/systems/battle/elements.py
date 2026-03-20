# src/netgrid/core/systems/battle/elements.py

ELEMENT_CHART = {
    "core": {},

    "root":     {"pulse": 1.5, "cloud": 1.5, "corrupt": 0.5, "void": 0.5},
    "pulse":    {"cloud": 1.5, "dream": 1.5, "root": 0.5, "firewall": 0.5},
    "archive":  {"corrupt": 1.5, "void": 1.5, "pulse": 0.5, "dream": 0.5},
    "cloud":    {"archive": 1.5, "firewall": 1.5, "pulse": 0.5, "root": 0.5},
    "firewall": {"pulse": 1.5, "corrupt": 1.5, "cloud": 0.5, "dream": 0.5},
    "dream":    {"firewall": 1.5, "archive": 1.5, "pulse": 0.5, "echo": 0.5},
    "echo":     {"dream": 1.5, "pulse": 1.5, "void": 0.5, "corrupt": 0.5},
    "void":     {"root": 1.5, "echo": 1.5, "archive": 0.5, "core": 0.5},
    "corrupt":  {"root": 1.5, "echo": 1.5, "archive": 0.5, "firewall": 0.5},
}
