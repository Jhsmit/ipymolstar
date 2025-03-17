# %%

from ipymolstar.molviewspec import MolViewSpec
from molviewspec import create_builder

# %%

# Example with custom schema
builder = create_builder()

com = [17.83685904, 20.84872876, 27.42270239]
structure = (
    builder.camera(target=com, position=[0, 250, 0], up=[0, 1, 0])
    .download(url="https://www.ebi.ac.uk/pdbe/entry-files/download/1cbs_updated.cif")
    .parse(format="mmcif")
    .model_structure()
    .component()
    .representation()
    .color(color="blue")
)

schema = builder.get_state()
molview = MolViewSpec(schema=schema, height="500px", width="500px")
molview


# %%
from ipymolstar import PDBeMolstar

view = PDBeMolstar(
    molecule_id="1qyn",
    theme="light",
    hide_water=True,
    visual_style="cartoon",
    spin=False,
    lighting="glossy",
)

view.tooltips = {
    "data": [
        {"struct_asym_id": "A", "tooltip": "Custom tooltip for chain A"},
        {"struct_asym_id": "B", "tooltip": "Custom tooltip for chain B"},
        {"struct_asym_id": "C", "tooltip": "Custom tooltip for chain C"},
        {"struct_asym_id": "D", "tooltip": "Custom tooltip for chain D"},
    ]
}

view

# %%
