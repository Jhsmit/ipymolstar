import solara
from ipymolstar import PDBeMolstar


@solara.component
def Page():
    expanded = solara.use_reactive(True)

    with solara.Sidebar():
        solara.Checkbox(label="Expanded", value=expanded)

    with solara.Card(style={"width": "500px"}):
        PDBeMolstar.element(
            hide_controls_icon=True,
            hide_expand_icon=True,
            hide_settings_icon=True,
            hide_selection_icon=True,
            molecule_id="1qyn",
            expanded=expanded.value,
        )
