# /// script
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///


import solara
from ipymolstar import PDBeMolstar, MolViewSpec
from molviewspec import create_builder


@solara.component
def Page():
    solara.Title("Solara + PDBeMolstar + MolViewSpec")
    molecule_id = solara.use_reactive("1qyn")

    builder = create_builder()
    (
        builder.download(url=f"https://files.rcsb.org/download/{molecule_id.value}.pdb")
        .parse(format="pdb")
        .model_structure()
        .component()
        .representation()
        .color(color="blue")
    )

    with solara.Sidebar():
        solara.InputText(label="Molecule ID", value=molecule_id)

    with solara.Columns():
        with solara.Card("PDBeMolstar"):
            PDBeMolstar.element(
                hide_controls_icon=True,
                hide_expand_icon=True,
                hide_settings_icon=True,
                hide_selection_icon=True,
                molecule_id=molecule_id.value,
            )
        with solara.Card("MolViewSpec"):
            MolViewSpec.element(msvj_data=builder.get_state())
