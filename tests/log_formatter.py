# tests/log_formatter.py

import sys

class LogFormatter:
    COLORS = {
        "RESET": "\033[0m",
        "PHASE": "\033[95m",      # magenta
        "ACTION": "\033[94m",     # blue
        "DAMAGE": "\033[91m",     # red
        "HEAL": "\033[92m",       # green
        "STATUS": "\033[93m",     # yellow
        "KO": "\033[41m\033[97m", # white on red
    }

    def __init__(self, stream=sys.stdout):
        self.stream = stream

    def __call__(self, msg: str):
        formatted = self.format_message(msg)
        self.stream.write(formatted + "\n")

    def format_message(self, msg: str) -> str:
        text = msg

        if "PHASE" in msg or "TURN" in msg:
            text = f"{self.COLORS['PHASE']}{msg}{self.COLORS['RESET']}"
        elif "uses" in msg or "chooses" in msg:
            text = f"{self.COLORS['ACTION']}{msg}{self.COLORS['RESET']}"
        elif "takes" in msg and "damage" in msg:
            text = f"{self.COLORS['DAMAGE']}{msg}{self.COLORS['RESET']}"
        elif "heals" in msg:
            text = f"{self.COLORS['HEAL']}{msg}{self.COLORS['RESET']}"
        elif "status" in msg or "DOT" in msg:
            text = f"{self.COLORS['STATUS']}{msg}{self.COLORS['RESET']}"
        elif "is defeated" in msg or "KO" in msg:
            text = f"{self.COLORS['KO']}{msg}{self.COLORS['RESET']}"

        return text
