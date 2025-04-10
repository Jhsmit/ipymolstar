from ipymolstar import PDBeMolstar
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import reactive_read, render_widget

ui.input_text("molecule_id", "Molecule id", "1qyn")


@render_widget
def molstar():
    view = PDBeMolstar(molecule_id="1qyn")
    return view


@reactive.effect
def _():
    molecule_id = input.molecule_id()
    # check for valid pdb id
    if len(molecule_id) == 4:
        molstar.widget.molecule_id = input.molecule_id()


@render.text
def center():
    event = reactive_read(molstar.widget, "mouseover_event")
    return f"Mouseover event: {event}"
