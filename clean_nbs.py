import glob, json

for path in glob.glob("notebooks/*.ipynb"):
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            new_source = []
            for line in cell.get("source", []):
                if any(k in line for k in ["matplotlib", "seaborn", "plt.", "sns.", "fig,"]):
                    new_source.append("# " + line)
                else:
                    new_source.append(line)
            cell["source"] = new_source
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)

print("Done cleaning notebooks!")
