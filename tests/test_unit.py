from ipymolstar import PDBeMolstar, MolViewSpec
from molviewspec import create_builder


def test_pdbemolstar():
    """Test the PDBeMolstar component"""
    # Create a PDBeMolstar instance
    pdbe_molstar = PDBeMolstar(
        molecule_id="1qyn",
        hide_controls_icon=True,
        hide_expand_icon=True,
        hide_settings_icon=True,
        hide_selection_icon=True,
    )
    # Check if the instance is created successfully
    assert isinstance(pdbe_molstar, PDBeMolstar), (
        "Failed to create PDBeMolstar instance"
    )


def test_molviewspec():
    """Test the MolViewSpec component"""
    # Create a MolViewSpec instance
    builder = create_builder()
    (
        builder.download(url=f"https://files.rcsb.org/download/1qyn.pdb")
        .parse(format="pdb")
        .model_structure()
        .component()
        .representation()
        .color(color="blue")
    )

    molview_spec = MolViewSpec(
        msvj_data=builder.get_state().dumps(),
    )
    # Check if the instance is created successfully
    assert isinstance(molview_spec, MolViewSpec), (
        "Failed to create MolViewSpec instance"
    )
