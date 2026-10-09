import sys
import json
import re
from pathlib import Path

# Ensure UTF-8 output on Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.resolve()
py_path = HERE / "gh2_gomart.py"
nb_path = HERE / "GH2_TeamName.ipynb"

if not py_path.exists():
    py_path = Path("homework/gh2_gomart/gh2_gomart.py")
if not nb_path.exists():
    nb_path = Path("homework/gh2_gomart/GH2_TeamName.ipynb")

print(f"Reading: {py_path.name}")
with open(py_path, "r", encoding="utf-8") as f:
    py_text = f.read()

print(f"Reading: {nb_path.name}")
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Extract Q2 section
pattern = r"(### Q2 · Is the move to e-wallet real\?[\s\S]*?)(?=### Q3 · Do slow deliveries cost good ratings\?)"
match = re.search(pattern, py_text)
if not match:
    print("[Error] Could not find Q2 section in gh2_gomart.py")
    sys.exit(1)

q2_text = match.group(1).strip()

# Split into cells by '# %%'
# Normalize starting with a marker
chunks = re.split(r"\n# %%\s*", "\n# %% [markdown]\n" + q2_text)
new_cells = []

for chunk in chunks:
    chunk = chunk.strip()
    if not chunk:
        continue
    if chunk.startswith("[markdown]"):
        content = chunk[len("[markdown]"):].strip()
        lines = []
        for line in content.split("\n"):
            if line.startswith("# "):
                lines.append(line[2:] + "\n")
            elif line == "#":
                lines.append("\n")
            else:
                lines.append(line + "\n")
        new_cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": lines
        })
    else:
        lines = [line + "\n" for line in chunk.split("\n")]
        new_cells.append({
            "cell_type": "code",
            "metadata": {},
            "source": lines,
            "execution_count": None,
            "outputs": []
        })

# Locate Q2 in notebook cells
start_idx = None
end_idx = None

for i, cell in enumerate(nb["cells"]):
    text = "".join(cell.get("source", []))
    if "### Q2 · Is the move to e-wallet real?" in text and start_idx is None:
        start_idx = i
    elif "### Q3 · Do slow deliveries cost good ratings?" in text and start_idx is not None:
        end_idx = i
        break

if start_idx is not None and end_idx is not None:
    nb["cells"][start_idx:end_idx] = new_cells
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f"[SUCCESS] Synchronized {len(new_cells)} cells of Q2 from {py_path.name} to {nb_path.name}!")
else:
    print(f"[Error] Start index: {start_idx}, End index: {end_idx}. Could not find Q2 boundary in notebook.")
    sys.exit(1)

