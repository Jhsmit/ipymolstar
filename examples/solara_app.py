import statistics
from dataclasses import asdict, dataclass
from io import StringIO
from pathlib import Path

import requests
import solara
import solara.lab
from Bio.PDB import PDBParser, Residue, Structure
from ipymolstar import THEMES, PDBeMolstar
from matplotlib import colormaps
from matplotlib.colors import Normalize
from solara.alias import rv

parser = PDBParser(QUIET=True)
CHAIN_COLORS = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
]
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
# use auth residue numbers or not
AUTH_RESIDUE_NUMBERS = {
    "1QYN": False,
    "2PE4": True,
}

pdb_ids = ["1QYN", "2PE4"]


def fetch_pdb(pdb_id) -> StringIO:
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url)
    if response.status_code == 200:
        sio = StringIO(response.text)
        sio.seek(0)
        return sio
    else:
        raise requests.HTTPError(f"Failed to download PDB file {pdb_id}")


structures = {p_id: parser.get_structure(p_id, fetch_pdb(p_id)) for p_id in pdb_ids}


@dataclass
class PDBeData:
    molecule_id: str = "1qyn"
    custom_data: dict | None = None
    color_data: dict | None = None
    bg_color: str = "#F7F7F7"
    spin: bool = False
    hide_polymer: bool = False
    hide_water: bool = False
    hide_heteroatoms: bool = False
    hide_carbs: bool = False
    hide_non_standard: bool = False
    hide_coarse: bool = False

    height: str = "700px"


visibility_cbs = ["polymer", "water", "heteroatoms", "carbs"]


def color_chains(structure: Structure.Structure) -> dict:
    data = [
        {
            "struct_asym_id": chain.id,
            "color": hex_color,
        }
        for hex_color, chain in zip(CHAIN_COLORS, structure.get_chains())
    ]

    color_data = {"data": data, "nonSelectedColor": None}
    return color_data


def color_residues(structure: Structure.Structure, auth: bool = False) -> dict:
    _, resn, _ = zip(
        *[r.id for r in structure.get_residues() if r.get_resname() in AMINO_ACIDS]
    )

    rmin, rmax = min(resn), max(resn)
    norm = Normalize(vmin=rmin, vmax=rmax)
    auth_str = "auth_" if auth else ""

    cmap = colormaps["rainbow"]
    data = []
    for i in range(rmin, rmax):
        r, g, b, a = cmap(norm(i), bytes=True)
        color = {"r": int(r), "g": int(g), "b": int(b)}
        elem = {
            f"{auth_str}residue_number": i,
            "color": color,
            "focus": False,
        }
        data.append(elem)

    color_data = {"data": data, "nonSelectedColor": None}
    return color_data


def get_bfactor(residue: Residue.Residue):
    """returns the residue-average b-factor"""
    return statistics.mean([atom.get_bfactor() for atom in residue])


def color_bfactor(structure: Structure.Structure, auth: bool = False) -> dict:
    auth_str = "auth_" if auth else ""
    value_data = []
    for chain in structure.get_chains():
        for r in chain.get_residues():
            if r.get_resname() in AMINO_ACIDS:
                bfactor = get_bfactor(r)
                elem = {
                    f"{auth_str}residue_number": r.id[1],
                    "struct_asym_id": chain.id,
                    "value": bfactor,
                }
                value_data.append(elem)

    all_values = [d["value"] for d in value_data]
    vmin, vmax = min(all_values), max(all_values)

    norm = Normalize(vmin=vmin, vmax=vmax)
    cmap = colormaps["inferno"]
    data = []
    for v_elem in value_data:
        elem = v_elem.copy()
        r, g, b, a = cmap(norm(elem.pop("value")), bytes=True)
        elem["color"] = {"r": int(r), "g": int(g), "b": int(b)}
        data.append(elem)

    color_data = {"data": data, "nonSelectedColor": None}
    return color_data


def apply_coloring(pdb_id: str, color_mode: str):
    structure = structures[pdb_id]
    auth = AUTH_RESIDUE_NUMBERS[pdb_id]
    if color_mode == "Chain":
        return color_chains(structure)
    elif color_mode == "Residue":
        return color_residues(structure, auth)
    elif color_mode == "β-factor":
        return color_bfactor(structure, auth)
    else:
        raise ValueError(f"Invalid color mode: {color_mode}")


color_options = ["Chain", "Residue", "β-factor"]
color_data = apply_coloring(pdb_ids[0], color_options[0])
data = solara.Reactive(PDBeData(color_data=color_data))

molecule_store = {
    "Glucose": dict(
        url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/conformers/000016A100000001/SDF?response_type=save&response_basename=Conformer3D_COMPOUND_CID_5793",
        format="sdf",
        binary=False,
    ),
    "ATP": dict(
        url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/5957/record/SDF?record_type=3d&response_type=save&response_basename=Conformer3D_COMPOUND_CID_5957",
        format="sdf",
        binary=False,
    ),
    "Caffeine": dict(
        url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/2519/record/SDF?record_type=3d&response_type=save&response_basename=Conformer3D_COMPOUND_CID_2519",
        format="sdf",
        binary=False,
    ),
    "Strychnine": dict(
        url=" https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/441071/record/SDF?record_type=3d&response_type=save&response_basename=Conformer3D_COMPOUND_CID_441071 ",
        format="sdf",
        binary=False,
    ),
}


def download_pdb(pdb_id, fpath: Path):
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url)
    if response.status_code == 200:
        fpath.write_bytes(response.content)
        return f"{pdb_id}.pdb"
    else:
        print("Failed to download PDB file")
        return None


@solara.component
def ProteinView(dark_effective: bool):
    with solara.Card("PDBeMol*"):
        theme = "dark" if dark_effective else "light"
        PDBeMolstar.element(**asdict(data.value), theme=theme)


@solara.component
def Page():
    solara.Title("ipymolstar - Solara")
    counter, set_counter = solara.use_state(0)
    dark_effective = solara.lab.use_dark_effective()
    dark_effective_previous = solara.use_previous(dark_effective)

    structure_type = solara.use_reactive("Protein")
    color_mode = solara.use_reactive(color_options[0])
    protein_id = solara.use_reactive(pdb_ids[0])
    molecule_key = solara.use_reactive(next(iter(molecule_store.keys())))

    if dark_effective != dark_effective_previous:
        if dark_effective:
            data.update(bg_color=THEMES["dark"]["bg_color"])
        else:
            data.update(bg_color=THEMES["light"]["bg_color"])

    def update_protein_id(value: str):
        protein_id.set(value)
        color_data = apply_coloring(protein_id.value, color_mode.value)
        data.update(color_data=color_data, molecule_id=protein_id.value.lower())

    def update_molecule_key(value: str):
        molecule_key.set(value)
        data.update(custom_data=molecule_store[molecule_key.value])

    def update_structure_type(value: str):
        structure_type.set(value)
        if structure_type.value == "Protein":
            color_data = apply_coloring(protein_id.value, color_mode.value)
            data.update(
                color_data=color_data,
                custom_data=None,
                molecule_id=protein_id.value.lower(),
            )
        else:
            color_data = {"data": [], "nonSelectedColor": None}
            data.update(
                molecule_id="",
                custom_data=molecule_store[molecule_key.value],
                color_data=color_data,  # used to reset colors
            )

    def update_color_mode(value: str):
        color_data = apply_coloring(protein_id.value, value)
        color_mode.set(value)
        data.update(color_data=color_data)

    with solara.AppBar():
        solara.lab.ThemeToggle()

    with solara.ColumnsResponsive([4, 8]):
        with solara.Card("Controls"):
            with solara.ToggleButtonsSingle(
                value=structure_type.value,
                on_value=update_structure_type,
                classes=["d-flex", "flex-row"],
            ):
                solara.Button(label="Protein", classes=["flex-grow-1"])
                solara.Button(label="Molecule", classes=["flex-grow-1"])

            solara.Div(style="height: 20px")

            if structure_type.value == "Protein":
                solara.Select(
                    label="PDB id",
                    value=protein_id.value,
                    values=pdb_ids,
                    on_value=update_protein_id,
                )

                solara.Select(
                    label="Color mode",
                    value=color_mode.value,
                    on_value=update_color_mode,
                    values=color_options,
                )
            else:
                solara.Select(
                    label="Molecule",
                    value=molecule_key.value,
                    values=list(molecule_store.keys()),
                    on_value=update_molecule_key,
                )

            solara.Checkbox(
                label="spin",
                value=data.value.spin,
                on_value=lambda x: data.update(spin=x),
            )

            for struc_elem in visibility_cbs:
                attr = f"hide_{struc_elem}"

                def on_value(x, attr=attr):
                    data.update(**{attr: x})

                solara.Checkbox(
                    label=f"hide {struc_elem}",
                    value=getattr(data.value, attr),
                    on_value=on_value,
                )

            btn = solara.Button("background color", block=True)
            with solara.lab.Menu(activator=btn, close_on_content_click=False):
                rv.ColorPicker(
                    v_model=data.value.bg_color,
                    on_v_model=lambda x: data.update(bg_color=x),
                )

            solara.Div(style="height: 20px")
            solara.Button(
                "redraw", on_click=lambda: set_counter(counter + 1), block=True
            )

        key = f"{counter}_{dark_effective}"
        ProteinView(dark_effective).key(key)


@solara.component
def Layout(children):
    dark_effective = solara.lab.use_dark_effective()
    return solara.AppLayout(children=children, toolbar_dark=dark_effective, color=None)
