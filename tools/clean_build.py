import time
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Base paths
BASE = Path(__file__).resolve().parents[1]
TOOLS = BASE / "tools"

# Thread pool for parallel execution
POOL = ThreadPoolExecutor(max_workers=6)

# Log directory
LOG_DIR = BASE / "logs"
LOG_FILE = LOG_DIR / "clean_build.log"
DIFF_LOG = LOG_DIR / "clean_build_diff.log"


class BuildSummary:
    # ANSI colors
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    DIM = "\033[90m"
    RESET = "\033[0m"

    def __init__(self):
        self.start = time.time()
        self.generated = []
        self.errors = []
        self.todo_count = 0
        self.integrity_issues = 0
        self.diff_output = ""

    def add_generated(self, label):
        self.generated.append(label)

    def add_error(self, label):
        self.errors.append(label)

    def set_todo_count(self, count):
        self.todo_count = count

    def set_integrity_issues(self, count):
        self.integrity_issues = count

    def collect_diff(self):
        """Capture the diff after all tools have run."""
        try:
            result = subprocess.run(
                ["git", "diff", "--color=always"],
                capture_output=True,
                text=True
            )
            # Always assign a string
            self.diff_output = result.stdout if result.stdout is not None else ""
        except Exception as e:
            # Always assign a string
            self.diff_output = f"Error collecting diff: {e}"


    def _write_log(self, duration):
        LOG_DIR.mkdir(exist_ok=True)

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n=== CLEAN BUILD @ {time.ctime()} ===\n")
            f.write(f"Duration: {duration:.2f} seconds\n")
            f.write(f"Generated: {', '.join(self.generated)}\n")
            f.write(f"Integrity issues: {self.integrity_issues}\n")
            f.write(f"TODO items: {self.todo_count}\n")

            if self.errors:
                f.write(f"Errors: {', '.join(self.errors)}\n")
                f.write("STATUS: FAILED\n")
            else:
                f.write("STATUS: PASSED\n")

        # Write diff log
        with open(DIFF_LOG, "a", encoding="utf-8") as f:
            f.write(f"\n=== DIFF @ {time.ctime()} ===\n")
            f.write(self.diff_output)
            f.write("\n")

    def print(self):
        duration = time.time() - self.start

        print(f"\n{self.CYAN}================ CLEAN BUILD SUMMARY ================{self.RESET}")
        print(f"{self.DIM}Duration: {duration:.2f} seconds{self.RESET}")

        print(f"\n{self.CYAN}Generated:{self.RESET}")
        for g in self.generated:
            print(f"  {self.GREEN}• {g}{self.RESET}")

        print(f"\n{self.CYAN}Integrity issues:{self.RESET} {self.YELLOW}{self.integrity_issues}{self.RESET}")
        print(f"{self.CYAN}TODO items:{self.RESET} {self.YELLOW}{self.todo_count}{self.RESET}")

        print(f"\n{self.CYAN}Changed files:{self.RESET}")
        if not (self.diff_output or "").strip():
            print(f"  {self.GREEN}No changes detected{self.RESET}")
        else:
            import re
            files = set(re.findall(r'diff --git a/(.*?) b/', self.diff_output))
            for f in files:
                print(f"  {self.YELLOW}• {f}{self.RESET}")

        if self.errors:
            print(f"\n{self.RED}❌ CLEAN BUILD FAILED{self.RESET}")
        else:
            print(f"\n{self.GREEN}✔ CLEAN BUILD PASSED{self.RESET}")

        print(f"{self.CYAN}====================================================={self.RESET}\n")

        self._write_log(duration)


def run(path: Path, summary: BuildSummary, label: str):
    try:
        rel = path.relative_to(BASE).with_suffix("")
        module = ".".join(rel.parts)

        result = subprocess.run(
            ["python", "-m", module],
            capture_output=True,
            text=True,
            check=True
        )

        # Capture TODO count if this is the TODO tool
        if label == "TODO List":
            import re
            match = re.search(r"(\d+)", result.stdout)
            if match:
                summary.set_todo_count(int(match.group(1)))

        summary.add_generated(label)

    except subprocess.CalledProcessError:
        summary.add_error(label)



def main():
    summary = BuildSummary()

    print("Running full clean build...")

    futures = []

    # Validation tools
    futures.append(POOL.submit(run, TOOLS / "data_integrity_checker.py", summary, "Integrity Check"))
    futures.append(POOL.submit(run, TOOLS / "find_todos.py", summary, "TODO List"))
    futures.append(POOL.submit(run, TOOLS / "update_allowed_tags.py", summary, "Allowed Tags"))

    # Cyberkin tools
    futures.append(POOL.submit(run, TOOLS / "cyberkin" / "family_autofill.py", summary, "Family Autofill"))
    futures.append(POOL.submit(run, TOOLS / "cyberkin" / "cyberkin_page.py", summary, "Cyberkin Markdown"))
    futures.append(POOL.submit(run, TOOLS / "cyberkin" / "family_markdown.py", summary, "Family Markdown"))
    futures.append(POOL.submit(run, TOOLS / "cyberkin" / "index_rebuilder.py", summary, "Cyberkin Index"))
    futures.append(POOL.submit(run, TOOLS / "cyberkin" / "family_index.py", summary, "Family Index"))

    # Reference tools
    futures.append(POOL.submit(run, TOOLS / "reference" / "reference_folder.py", summary, "Reference Folder"))
    futures.append(POOL.submit(run, TOOLS / "reference" / "reference_autofill.py", summary, "Reference Autofill"))

    # Wait for all tasks
    for f in futures:
        f.result()

    # Capture diff after all tools complete
    summary.collect_diff()

    # Print summary + write logs
    summary.print()

    if summary.errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
