import solara
from ipymolstar import PDBeMolstar, THEMES
from dataclasses import dataclass, asdict
from solara.alias import rw, rv
import solara.lab


@dataclass
class PDBeData:
    molecule_id: str = "1qyn"
    custom_data: dict | None = None
    bg_color: str = "#F7F7F7"
    spin: bool = False
    hide_polymer: bool = False
    hide_water: bool = False
    hide_heteroatoms: bool = False
    hide_carbs: bool = False
    hide_non_standard: bool = False
    hide_coarse: bool = False


data = solara.Reactive(PDBeData())
visibility_cbs = ["polymer", "water", "heteroatoms", "carbs", "non_standard", "coarse"]

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


@solara.component
def ProteinView(dark_effective: bool):
    with solara.Card("Protein view"):
        theme = "dark" if dark_effective else "light"
        PDBeMolstar.element(**asdict(data.value), theme=theme)


@solara.component
def Page():
    counter, set_counter = solara.use_state(0)
    dark_effective = solara.lab.use_dark_effective()
    dark_effective_previous = solara.use_previous(dark_effective)

    structure_type = solara.use_reactive("Protein")
    protein_id = solara.use_reactive(protein_store[0])
    molecule_key = solara.use_reactive(next(iter(molecule_store.keys())))

    if dark_effective != dark_effective_previous:
        if dark_effective:
            data.update(bg_color=THEMES["dark"]["bg_color"])
        else:
            data.update(bg_color=THEMES["light"]["bg_color"])

    def update_molecule_data(value: str, name: str):
        if name == "protein_id":
            protein_id.set(value)
        elif name == "molecule_key":
            molecule_key.set(value)
        elif name == "structure_type":
            structure_type.set(value)

        if structure_type.value == "Protein":
            # note: molecule_id is used to set the protein
            # seems confusing here because we use custom_data to show molecules
            data.update(molecule_id=protein_id.value.lower(), custom_data=None)
        else:
            data.update(molecule_id="", custom_data=molecule_store[molecule_key.value])

    with solara.AppBar():
        solara.lab.ThemeToggle()

    with solara.Columns([4, 8]):
        with solara.Card("Controls"):

            def on_value(x, name="structure_type"):
                update_molecule_data(x, name)

            with solara.ToggleButtonsSingle(
                value=structure_type.value,
                on_value=on_value,
                classes=["d-flex", "flex-row"],
            ):
                solara.Button(label="Protein", classes=["flex-grow-1"])
                solara.Button(label="Molecule", classes=["flex-grow-1"])

            solara.Div(style="height: 20px")

            if structure_type.value == "Protein":

                def on_value(x, name="protein_id"):
                    update_molecule_data(x, name)

                solara.Select(
                    label="PDB id",
                    value=protein_id.value,
                    values=protein_store,
                    on_value=on_value,
                )
            else:

                def on_value(x, name="molecule_key"):
                    update_molecule_data(x, name)

                solara.Select(
                    label="Molecule",
                    value=molecule_key.value,
                    values=list(molecule_store.keys()),
                    on_value=on_value,
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

            solara.Button(
                "redraw", on_click=lambda: set_counter(counter + 1), block=True
            )

        # with solara.Card("Protein view"):
        #     PDBeMolstar.element(**asdict(data.value)).key(f"molstar-{counter}")
        key = f"{counter}_{dark_effective}"
        ProteinView(dark_effective).key(key)

        # solara.Text(str(counter) + str(dark_effective))


@solara.component
def Layout(children):
    route, routes = solara.use_route()
    dark_effective = solara.lab.use_dark_effective()
    return solara.AppLayout(
        children=children, toolbar_dark=dark_effective, color=None
    )  # if dark_effective else "primary")
