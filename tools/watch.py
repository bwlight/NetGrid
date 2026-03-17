# tools/watch.py

import time
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# -------------------------------
# PATH SETUP
# -------------------------------

BASE = Path(__file__).resolve().parents[1]
TOOLS = BASE / "tools"

CYBERKIN_DIR = BASE / "data" / "cyberkin"
FAMILIES_DIR = BASE / "data" / "families"
SCHEMAS_DIR = BASE / "schemas"
ALLOWED_TAGS = SCHEMAS_DIR / "allowed_tags.json"

# -------------------------------
# IMPORT INCREMENTAL TOOLS
# -------------------------------

import tools.data_integrity_checker as integrity
import tools.find_todos as todos
import tools.update_allowed_tags as update_tags

import tools.cyberkin.cyberkin_page as cyberkin_page
import tools.cyberkin.family_autofill as family_autofill
import tools.cyberkin.family_markdown as family_markdown
import tools.cyberkin.index_rebuilder as index_rebuilder
import tools.cyberkin.family_index as family_index

from tools.dependency_graph import load_graph


# -------------------------------
# PARALLEL EXECUTOR
# -------------------------------
# We use a thread pool to run independent rebuild tasks at the same time.
# 4 workers is safe for your workload and avoids I/O contention.

POOL = ThreadPoolExecutor(max_workers=4)


# -------------------------------
# CYBERKIN PIPELINE (PARALLEL)
# -------------------------------

def run_cyberkin_pipeline(path: Path):
    """
    Rebuild everything affected by a single Cyberkin change.
    This version uses parallel threads for independent tasks.
    """

    print(f"→ Cyberkin changed: {path.name}")

    # 1. Validation must run BEFORE parallel work.
    integrity.run()
    todos.run()

    # Load Cyberkin JSON to determine family
    ck = json.load(open(path, "r", encoding="utf-8"))
    cid = ck["id"]
    family_id = ck.get("family")

    # 2. Submit parallel tasks
    futures = []

    # Rebuild Cyberkin markdown
    futures.append(POOL.submit(cyberkin_page.run_single, path))

    # Update family membership + family JSON
    futures.append(POOL.submit(family_autofill.run_for_cyberkin, path))

    # Update Cyberkin index entry
    futures.append(POOL.submit(index_rebuilder.run_single, path))

    # If Cyberkin has a family, rebuild that family’s markdown + index
    if family_id:
        family_path = FAMILIES_DIR / f"{family_id}.json"
        futures.append(POOL.submit(family_markdown.run_for_family, family_path))
        futures.append(POOL.submit(family_index.run_for_family, family_path))

    # 3. Wait for all tasks to finish
    for f in futures:
        f.result()


# -------------------------------
# FAMILY PIPELINE (PARALLEL)
# -------------------------------

def run_family_pipeline(path: Path):
    """
    Rebuild everything affected by a single family change.
    Uses dependency graph to find all Cyberkin in this family.
    """

    print(f"→ Family changed: {path.name}")

    integrity.run()
    todos.run()

    family = json.load(open(path, "r", encoding="utf-8"))
    fid = family["id"]
    members = family.get("members", [])

    futures = []

    # Rebuild family markdown + index
    futures.append(POOL.submit(family_markdown.run_for_family, path))
    futures.append(POOL.submit(family_index.run_for_family, path))

    # Rebuild markdown for all Cyberkin in this family
    for cid in members:
        ck_path = None

        # Find the Cyberkin file by searching the directory
        for stage_dir in CYBERKIN_DIR.iterdir():
            candidate = stage_dir / f"{cid}.json"
            if candidate.exists():
                ck_path = candidate
                break

        if ck_path:
            futures.append(POOL.submit(cyberkin_page.run_single, ck_path))
            futures.append(POOL.submit(index_rebuilder.run_single, ck_path))

    for f in futures:
        f.result()


# -------------------------------
# SCHEMA PIPELINE
# -------------------------------

def run_schema_pipeline():
    print("→ Schema changed")
    integrity.run()
    todos.run()


# -------------------------------
# TAG PIPELINE
# -------------------------------

def run_allowed_tags_pipeline():
    print("→ allowed_tags.json changed")
    update_tags.run()
    integrity.run()
    todos.run()


# -------------------------------
# WATCHER EVENT HANDLER
# -------------------------------

class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_run = 0

    def on_any_event(self, event):
        if event.is_directory:
            return

        # Debounce rapid saves
        now = time.time()
        if now - self.last_run < 0.8:
            return
        self.last_run = now

        path = Path(event.src_path)
        print(f"\nDetected change: {path}")

        # CYBERKIN JSON
        if CYBERKIN_DIR in path.parents and path.suffix == ".json":
            run_cyberkin_pipeline(path)
            return

        # FAMILY JSON
        if FAMILIES_DIR in path.parents and path.suffix == ".json":
            run_family_pipeline(path)
            return

        # SCHEMAS
        if SCHEMAS_DIR in path.parents and path.suffix == ".json":
            if path == ALLOWED_TAGS:
                run_allowed_tags_pipeline()
            else:
                run_schema_pipeline()
            return

        # TOOL CHANGES
        if TOOLS in path.parents and path.suffix == ".py":
            print("Tool changed — will reload on next run.")
            return

        print("Change ignored.")


# -------------------------------
# WATCHER STARTUP
# -------------------------------

def run():
    print("Watching for changes...\n")

    observer = Observer()
    handler = ChangeHandler()

    observer.schedule(handler, str(CYBERKIN_DIR), recursive=True)
    observer.schedule(handler, str(FAMILIES_DIR), recursive=True)
    observer.schedule(handler, str(SCHEMAS_DIR), recursive=True)
    observer.schedule(handler, str(TOOLS), recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    run()
