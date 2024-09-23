import panel as pn
from ipymolstar.panel import PDBeMolstar

if pn.state.served:
    molstar = PDBeMolstar(molecule_id="1qyn", theme="light")
    parameters = pn.Param(
        molstar,
        parameters=[
            "molecule_id",
            "spin",
            "hide_controls",
            "visual_style",
            "hide_water",
        ],
    )
    settings = pn.Column(parameters)
    view = pn.Column(molstar, width=500)
    pn.Row(settings, view).servable()
