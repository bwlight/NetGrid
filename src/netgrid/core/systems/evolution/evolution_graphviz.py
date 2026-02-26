import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List


# ---------------------------------------------------------
# Family Color Themes
# ---------------------------------------------------------
FAMILY_COLORS = {
    "core": "#4fc3f7",
    "root": "#81c784",
    "archive": "#ce93d8",
    "firewall": "#ff8a65",
    "cloud": "#90caf9",
    "echo": "#ba68c8",
    "pulse": "#f06292",
    "dream": "#9575cd",
    "void": "#b0bec5",
    "corrupt": "#ef5350"
}


# ---------------------------------------------------------
# Load evolution data
# ---------------------------------------------------------
def load_evolution_folder(base_folder: Path) -> Dict[str, Any]:
    families_folder = base_folder / "families"

    if not families_folder.exists():
        raise FileNotFoundError(f"Missing folder: {families_folder}")

    merged = {}

    for file in families_folder.glob("evolution_*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for k, v in data.items():
                if k in merged:
                    raise ValueError(f"Duplicate species ID: {k}")
                merged[k] = v

    return merged


# ---------------------------------------------------------
# Color logic
# ---------------------------------------------------------
def themed_color(species: str) -> str:
    family = species.split("_")[0]
    return FAMILY_COLORS.get(family, "#e0e0e0")


# ---------------------------------------------------------
# Render DOT → PNG/SVG (High DPI)
# ---------------------------------------------------------
def render_graphviz(dot_path: Path):
    png_path = dot_path.with_suffix(".png")
    svg_path = dot_path.with_suffix(".svg")

    # High DPI PNG (300 DPI)
    subprocess.run([
        "dot", "-Tpng",
        "-Gdpi=300",
        str(dot_path),
        "-o", str(png_path)
    ], check=False)

    # SVG (infinite resolution)
    subprocess.run([
        "dot", "-Tsvg",
        str(dot_path),
        "-o", str(svg_path)
    ], check=False)

    print(f"Rendered PNG: {png_path}")
    print(f"Rendered SVG: {svg_path}")


# ---------------------------------------------------------
# Generate a DOT graph
# ---------------------------------------------------------
def generate_graph(evo_data: Dict[str, Any], species_list: List[str], output_path: Path, dark_mode=False):
    lines = []

    if dark_mode:
        lines.append('digraph EvolutionTree {')
        lines.append('  rankdir=LR;')
        lines.append('  bgcolor="#1e1e1e";')
        lines.append('  node [shape=box, style="rounded,filled", fontcolor="white"];')
    else:
        lines.append('digraph EvolutionTree {')
        lines.append('  rankdir=LR;')
        lines.append('  node [shape=box, style="rounded,filled"];')

    for species in species_list:
        evo = evo_data[species]
        color = themed_color(species)

        if dark_mode:
            lines.append(f'  "{species}" [fillcolor="{color}", fontcolor="black"];')
        else:
            lines.append(f'  "{species}" [fillcolor="{color}"];')

        # Single evolution
        if "into" in evo:
            lines.append(f'  "{species}" -> "{evo["into"]}";')

        # Branches
        if "branches" in evo:
            for branch in evo["branches"]:
                lines.append(f'  "{species}" -> "{branch["into"]}" [color="#7e57c2"];')

    lines.append("}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Generated DOT: {output_path}")


# ---------------------------------------------------------
# Cluster Graph
# ---------------------------------------------------------
def generate_cluster_graph(evo_data: Dict[str, Any], output_path: Path):
    lines = []
    lines.append("digraph EvolutionTree {")
    lines.append("  rankdir=LR;")
    lines.append('  node [shape=box, style="rounded,filled"];')

    # Group species by family
    families = {}
    for species in evo_data:
        family = species.split("_")[0]
        families.setdefault(family, []).append(species)

    # Create clusters
    for family, species_list in families.items():
        lines.append(f'  subgraph cluster_{family} {{')
        lines.append(f'    label="{family.upper()}";')
        lines.append('    style="rounded,filled"; fillcolor="#f5f5f5";')

        for species in species_list:
            color = themed_color(species)
            lines.append(f'    "{species}" [fillcolor="{color}"];')

        lines.append("  }")

    # Add edges
    for species, evo in evo_data.items():
        if "into" in evo:
            lines.append(f'  "{species}" -> "{evo["into"]}";')
        if "branches" in evo:
            for branch in evo["branches"]:
                lines.append(f'  "{species}" -> "{branch["into"]}" [color="#7e57c2"];')

    lines.append("}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Generated DOT: {output_path}")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
if __name__ == "__main__":
    base_folder = Path(__file__).parent
    evo_data = load_evolution_folder(base_folder)

    # Output folder structure
    graphs_folder = base_folder / "graphs"
    full_folder = graphs_folder / "full"
    dark_folder = graphs_folder / "dark"
    cluster_folder = graphs_folder / "clusters"
    families_folder = graphs_folder / "families"

    # Create folders
    for folder in [full_folder, dark_folder, cluster_folder, families_folder]:
        folder.mkdir(parents=True, exist_ok=True)

    # Full graph
    dot_file = full_folder / "evolution_graph.dot"
    generate_graph(evo_data, list(evo_data.keys()), dot_file)
    render_graphviz(dot_file)

    # Dark mode
    dot_file = dark_folder / "evolution_graph_dark.dot"
    generate_graph(evo_data, list(evo_data.keys()), dot_file, dark_mode=True)
    render_graphviz(dot_file)

    # Family graphs
    families = {}
    for species in evo_data:
        family = species.split("_")[0]
        families.setdefault(family, []).append(species)

    for family, species_list in families.items():
        family_dir = families_folder / family
        family_dir.mkdir(exist_ok=True)

        dot_file = family_dir / f"{family}.dot"
        generate_graph(evo_data, species_list, dot_file)
        render_graphviz(dot_file)

    # Cluster graph
    dot_file = cluster_folder / "evolution_clusters.dot"
    generate_cluster_graph(evo_data, dot_file)
    render_graphviz(dot_file)
