import glob, json

for path in glob.glob("notebooks/*.ipynb"):
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            new_source = []
            for line in cell.get("source", []):
                if ".plot(" in line:
                    new_source.append("# " + line + "\n# (Plotting disabled because matplotlib is not installed)")
                else:
                    new_source.append(line)
            cell["source"] = new_source
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)

print("Disabled all pandas .plot() calls successfully!")
