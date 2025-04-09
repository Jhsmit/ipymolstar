from pathlib import Path

import solara
import solara.lab
from Bio.PDB import PDBParser, Structure
from ipymolstar import PDBeMolstar
from matplotlib import colormaps
from matplotlib.colors import Normalize

AMINO_ACIDS = [
    "ALA",
    "ARG",
    "ASN",
    "ASP",
    "CYS",
    "GLN",
    "GLU",
    "GLY",
    "HIS",
    "ILE",
    "LEU",
    "LYS",
    "MET",
    "PHE",
    "PRO",
    "PYL",
    "SEC",
    "SER",
    "THR",
    "TRP",
    "TYR",
    "VAL",
]

# %%

root = Path(__file__).parent.parent
pdb_path = root / "assets" / "1qyn.pdb"

parser = PDBParser(QUIET=True)
structure = parser.get_structure("1qyn", pdb_path)
MAX_R = max(r.id[1] for r in structure.get_residues())

# %%

custom_data = {"data": pdb_path.read_bytes(), "format": "pdb", "binary": False}


# %%
def color_residues(
    structure: Structure.Structure, auth: bool = False, phase: int = 0
) -> dict:
    _, resn, _ = zip(
        *[r.id for r in structure.get_residues() if r.get_resname() in AMINO_ACIDS]
    )

    rmin, rmax = min(resn), max(resn)
    # todo check for off by one errors
    norm = Normalize(vmin=rmin, vmax=rmax)
    auth_str = "_auth" if auth else ""

    cmap = colormaps["hsv"]
    data = []
    for i in range(rmin, rmax + 1):
        range_size = rmax + 1 - rmin
        j = rmin + ((i - rmin + phase) % range_size)
        r, g, b, a = cmap(norm(i), bytes=True)
        color = {"r": int(r), "g": int(g), "b": int(b)}
        elem = {
            f"start{auth_str}_residue_number": j,
            f"end{auth_str}_residue_number": j,
            "color": color,
            "focus": False,
        }
        data.append(elem)

    color_data = {"data": data, "nonSelectedColor": None}
    return color_data


@solara.component
def Page():
    phase = solara.use_reactive(0.0)
    color_data = color_residues(structure, auth=True, phase=phase.value)
    with solara.Card():
        PDBeMolstar.element(
            custom_data=custom_data, hide_water=True, color_data=color_data
        )
        solara.FloatSlider(label="Phase", min=0, max=MAX_R, value=phase, step=1)


Page()
