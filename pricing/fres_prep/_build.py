"""Percent-format .py -> executed .ipynb converter for the FRES prep notebooks.

Usage:  python _build.py src/N4_uncertainty_to_decision.py [--no-exec]

Markdown cells start with `# %% [markdown]` (lines prefixed `# ` are stripped);
code cells start with `# %%`. The executed notebook lands next to this script.
"""
from __future__ import annotations

import sys
from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient

HERE = Path(__file__).parent


def parse_percent(text: str):
    cells, kind, buf = [], None, []

    def flush():
        if kind is None:
            return
        src = "\n".join(buf).strip("\n")
        if not src:
            return
        if kind == "markdown":
            src = "\n".join(
                l[2:] if l.startswith("# ") else ("" if l.strip() == "#" else l)
                for l in src.split("\n")
            )
            cells.append(nbf.v4.new_markdown_cell(src))
        else:
            cells.append(nbf.v4.new_code_cell(src))

    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("# %%"):
            flush()
            kind = "markdown" if "[markdown]" in s else "code"
            buf = []
        elif kind is not None:
            buf.append(line)
    flush()
    return cells


def build(src: Path, execute: bool = True) -> Path:
    nb = nbf.v4.new_notebook()
    nb.cells = parse_percent(src.read_text(encoding="utf-8"))
    nb.metadata["kernelspec"] = {
        "name": "python3", "display_name": "Python 3", "language": "python",
    }
    out = HERE / (src.stem + ".ipynb")
    if execute:
        client = NotebookClient(nb, timeout=180, kernel_name="python3",
                                resources={"metadata": {"path": str(HERE)}})
        client.execute()
    nbf.write(nb, out)
    print(f"wrote {out.name}  ({len(nb.cells)} cells, executed={execute})")
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    execute = "--no-exec" not in sys.argv
    for a in args:
        build(Path(a) if Path(a).is_absolute() else HERE / a, execute)
