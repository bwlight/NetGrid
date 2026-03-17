# tools/master_runner.py

import importlib.util
import traceback
from pathlib import Path

BASE = Path(__file__).resolve().parent


def load_tool(path: Path):
    """Dynamically load a Python module from a file path."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    print("Running integrity check...\n")

    integrity_path = BASE / "data_integrity_checker.py"
    integrity = load_tool(integrity_path)
    errors = integrity.run_integrity_check()

    # Stop on critical errors
    if errors["critical"]:
        print("CRITICAL ERRORS — generation aborted.\n")
        for err in errors["critical"]:
            print(f"❌ {err}")
        print("\nFix the above critical errors and re-run the generator.")
        return

    # Print warnings but continue
    if errors["warnings"]:
        for group, items in errors["grouped"].items():
            if items:
                print(f"--- {group} ---")
                for item in items:
                    print(f"• {item}")
                print()

        print("Warnings:")
        for w in errors["warnings"]:
            print(f"- {w}")
        print()

    # Ordered tool execution
    tool_paths = [
        BASE / "reference" / "reference_folder.py",
        BASE / "reference" / "reference_autofill.py",
        BASE / "cyberkin" / "index_rebuilder.py",
        BASE / "cyberkin" / "family_autofill.py",
        BASE / "cyberkin" / "cyberkin_page.py",
        BASE / "cyberkin" / "family_markdown.py",
        BASE / "cyberkin" / "family_index.py",
    ]

    for path in tool_paths:
        print(f"Running {path.as_posix()}...")
        try:
            tool = load_tool(path)
            tool.run()
        except Exception as e:
            print(f"Error running {path.name}: {e}")
            traceback.print_exc()
            print("Continuing to next tool...\n")

    print("\nPipeline complete. All reference, family, and index files updated.")


if __name__ == "__main__":
    main()
