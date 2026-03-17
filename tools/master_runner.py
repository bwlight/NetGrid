# tools/master_runner.py

import importlib.util
import traceback
from pathlib import Path

BASE = Path(__file__).resolve().parent
TOOLS = BASE  # tools folder


def load_tool(path: Path):
    """Dynamically load a Python module from a file path."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    print("Running integrity check...\n")

    # 1. Integrity checker
    integrity_path = TOOLS / "data_integrity_checker.py"
    integrity = load_tool(integrity_path)
    integrity.run()

    # 2. TODO generator
    print("Generating TODO list...\n")
    todo_path = TOOLS / "find_todos.py"
    todo = load_tool(todo_path)
    todo.run()

    # 3. Ordered tool execution (AFTER validation)
    tool_paths = [
        TOOLS / "update_allowed_tags.py",
        TOOLS / "reference" / "reference_folder.py",
        TOOLS / "reference" / "reference_autofill.py",
        TOOLS / "cyberkin" / "index_rebuilder.py",
        TOOLS / "cyberkin" / "family_autofill.py",
        TOOLS / "cyberkin" / "cyberkin_page.py",
        TOOLS / "cyberkin" / "family_markdown.py",
        TOOLS / "cyberkin" / "family_index.py"
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
