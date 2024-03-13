import solara
from ipymolstar import PDBeMolstar
from dataclasses import dataclass, asdict
from solara.alias import rw, rv


@dataclass
class PDBeData:
    molecule_id: str = "1qyn"
    spin: bool = False
    hide_polymer: bool = False
    hide_water: bool = False
    hide_heteroatoms: bool = False
    hide_carbs: bool = False
    hide_non_standard: bool = False
    hide_coarse: bool = False


data = solara.Reactive(PDBeData())
molecule_id_options = ["1qyn", "2pe4"]

visibility_cbs = ["polymer", "water", "heteroatoms", "carbs", "non_standard", "coarse"]


@solara.component
def ProteinView(dark_effective: bool):
    with solara.Card("Protein view"):
        theme = "dark" if dark_effective else "light"
        PDBeMolstar.element(**asdict(data.value), theme=theme)


@solara.component
def Page():
    counter, set_counter = solara.use_state(0)
    dark_effective = solara.lab.use_dark_effective()

    with solara.AppBar():
        solara.lab.ThemeToggle()

    with solara.Columns([4, 8]):
        with solara.Card("Controls"):
            solara.Button(
                "reset", on_click=lambda: set_counter(counter + 1), block=True
            )

            values = [{"text": s.upper(), "value": s} for s in molecule_id_options]
            solara.Select(
                label="molecule id",
                value=data.value.molecule_id,
                values=values,
                on_value=lambda x: data.update(molecule_id=x),
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
                rv.ColorPicker(v_model="#ff00ff")  # todo connect to model

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
