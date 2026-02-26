import os

HEADER = "# Auto-generated exports. Do not edit manually.\n"

def is_python_module(filename: str) -> bool:
    return filename.endswith(".py") and filename != "__init__.py"


def generate_exports_for_folder(folder: str):
    """
    Generates clean exports for all Python modules in a folder.
    """
    modules = [
        f[:-3] for f in os.listdir(folder)
        if is_python_module(f)
    ]

    # Skip folders with no Python modules
    if not modules:
        return None

    init_path = os.path.join(folder, "__init__.py")

    lines = [HEADER]

    for module in modules:
        class_name = "".join(part.capitalize() for part in module.split("_"))
        lines.append(f"from .{module} import {class_name}")

    with open(init_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return init_path


def ensure_init_files(root_path: str):
    created = []
    updated = []

    for folder, subfolders, files in os.walk(root_path):
        # Skip __pycache__ and data/schema folders
        if "__pycache__" in folder:
            continue
        if folder.endswith("data") or folder.endswith("schemas"):
            continue

        init_path = os.path.join(folder, "__init__.py")

        # Create missing __init__.py
        if not os.path.exists(init_path):
            with open(init_path, "w", encoding="utf-8") as f:
                f.write(HEADER)
            created.append(init_path)

        # Generate exports for this folder
        updated_path = generate_exports_for_folder(folder)
        if updated_path:
            updated.append(updated_path)

    return created, updated


if __name__ == "__main__":
    root = "src/netgrid"
    created, updated = ensure_init_files(root)

    print("\n=== __init__.py Auto-Generation Report ===")
    for f in created:
        print(f"Created: {f}")
    for f in updated:
        print(f"Updated exports: {f}")

    if not created and not updated:
        print("All __init__.py files already exist and are up to date.")

    print("==========================================\n")
    print("Export generation complete.")    