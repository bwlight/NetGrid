import json, os

folder = "data/abilities"

print("Scanning ability files...\n")

for f in os.listdir(folder):
    if f.endswith(".json"):
        path = os.path.join(folder, f)
        try:
            with open(path) as fp:
                data = json.load(fp)
        except Exception as e:
            print(f"❌ {f} - JSON error: {e}")
            continue

        if "name" not in data:
            print(f"❌ Missing name: {f}")
        else:
            print(f"✔ OK: {f}")
