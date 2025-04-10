import statistics
from io import StringIO

import panel as pn
import param
import requests
from Bio.PDB import PDBParser, Residue, Structure
from ipymolstar.panel import PDBeMolstar
from matplotlib import colormaps
from matplotlib.colors import Normalize

theme = "light" if pn.config.theme == "default" else "dark"

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


protein_store = ["1QYN", "2PE4"]
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


class Controller(param.Parameterized):
    structure_type = param.Selector(
        default="Protein",
        allow_None=False,
        objects=["Protein", "Molecule"],
        doc="Choose to display protein or a small molecule",
    )

    protein_id = param.Selector(
        default=protein_store[0],
        objects=protein_store,
        doc="Protein to display",
    )

    molecule_id = param.Selector(
        default="Glucose",
        objects=list(molecule_store.keys()),
        doc="Molecule to display",
    )

    color_mode = param.Selector(
        default="Chain",
        objects=["Chain", "Residue", "β-factor"],
        doc="Coloring mode",
    )

    def __init__(self, molstar_view: PDBeMolstar, **params):
        self.molstar_view = molstar_view
        super().__init__(**params)

    @param.depends("structure_type")
    def secondary_selector(self):
        if self.structure_type == "Protein":
            return pn.widgets.Select.from_param(self.param.protein_id, name="Protein")
        elif self.structure_type == "Molecule":
            return pn.widgets.Select.from_param(self.param.molecule_id, name="Molecule")
        else:
            return pn.pane.Str("Please make a selection")

    @param.depends("structure_type")
    def color_selector(self):
        if self.structure_type == "Protein":
            return pn.widgets.Select.from_param(
                self.param.color_mode, name="Color mode"
            )
        return None

    @param.depends(
        "structure_type", "protein_id", "molecule_id", "color_mode", watch=True
    )
    def update_molecule_data(self):
        if self.structure_type == "Protein":
            molecule_id = self.protein_id.lower()
            custom_data = None
            color_data = apply_coloring(self.protein_id, self.color_mode)
        else:
            molecule_id = ""
            custom_data = molecule_store[self.molecule_id]
            color_data = {"data": [], "nonSelectedColor": None}

        self.molstar_view.param.update(
            molecule_id=molecule_id, custom_data=custom_data, color_data=color_data
        )


color_data = apply_coloring(pdb_ids[0], "Chain")  # initial value
molstar = PDBeMolstar(
    molecule_id="1qyn", theme=theme, sizing_mode="stretch_width", color_data=color_data
)  # , width="1150px")


parameters = pn.Param(
    molstar,
    parameters=[
        "spin",
        "visual_style",
        "hide_water",
        "hide_polymer",
        "hide_heteroatoms",
        "hide_carbs",
        "hide_non_standard",
        "hide_coarse",
        "bg_color",
    ],
    widgets={
        "bg_color": {"type": pn.widgets.ColorPicker, "sizing_mode": "stretch_width"}
    },
    show_name=False,
)

ctrl = Controller(molstar)


settings = pn.Column(
    pn.pane.Markdown("## Controls"),
    pn.widgets.Select.from_param(ctrl.param.structure_type, name="Structure type"),
    ctrl.secondary_selector,
    ctrl.color_selector,
    *parameters,
)
view = pn.Column(molstar, sizing_mode="stretch_width")

template = pn.template.FastListTemplate(
    title="ipymolstar - Panel",
    sidebar=[settings],
    main_max_width="1200px",
)

template.main.append(view)

if pn.state.served:
    template.servable()
