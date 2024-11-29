"""
This example shows to how use click interactions
"""

from string import Template

import solara
from ipymolstar import PDBeMolstar

url_template = Template(
    "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/$cid/record/SDF?record_type=3d&response_type=save&response_basename=Conformer3D_COMPOUND_CID_$cid"
)


AA_LUT = {
    "ARG": 6322,
    "HIS": 6274,
    "LYS": 5962,
    "ASP": 5960,
    "GLU": 33032,
    "SER": 5951,
    "THR": 6288,
    "ASN": 6267,
    "GLN": 5961,
    "CYS": 5862,
    "SEC": 6326983,
    "GLY": 750,
    "PRO": 145742,
    "ALA": 5950,
    "VAL": 6287,
    "ILE": 6306,
    "LEU": 6106,
    "MET": 6137,
    "PHE": 6140,
    "TYR": 6057,
    "TRP": 6305,
}

custom_data_initial = dict(
    url=url_template.substitute(cid=AA_LUT["TRP"]),
    format="sdf",
    binary=False,
)


molecule_id = "1QYN"

# %%
s = """empty
  -ISIS-  

  0  0  0  0  0  0  0  0  0  0999 V2000
M  END
$$$$
"""

b = s.encode()
empty_data = {
    "data": b,
    "format": "sdf",
    "binary": True,
}

# %%


@solara.component
def Page():
    solara.Title("ipymolstar - Click Events")
    click_event = solara.use_reactive(None)
    custom_data = solara.use_reactive(empty_data)
    molecule_id = solara.use_reactive("1QYN")
    amino_acid = solara.use_reactive("")

    def on_click(event):
        click_event.set(event)
        aa_tla = event["comp_id"]

        if aa_tla in AA_LUT:
            amino_acid.set(aa_tla)
            custom_data.set(
                dict(
                    url=url_template.substitute(cid=AA_LUT[aa_tla]),
                    format="sdf",
                    binary=False,
                )
            )
        else:
            amino_acid.set("")
            custom_data.set(empty_data)

    with solara.Sidebar():
        solara.InputText(
            label="Molecule ID", value=molecule_id, on_value=molecule_id.set
        )

    with solara.Columns():
        with solara.Card(f"Protein: {molecule_id.value}", style={"width": "500px"}):
            PDBeMolstar.element(
                molecule_id=molecule_id.value.lower(),
                hide_controls_icon=True,
                hide_expand_icon=True,
                hide_settings_icon=True,
                hide_selection_icon=False,
                select_interaction=False,  # dont show local interactions on click
                click_focus=False,  # dont zoom on click
                on_click_event=on_click,
            )

        with solara.Card(f"Amino Acid: {amino_acid.value}", style={"width": "500px"}):
            PDBeMolstar.element(
                molecule_id="",
                custom_data=custom_data.value,
                hide_controls_icon=True,
                hide_expand_icon=True,
                hide_settings_icon=True,
                hide_selection_icon=False,
                click_focus=False,
            )
