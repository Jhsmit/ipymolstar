import panel as pn
from ipymolstar.panel import PDBeMolstar

theme = "light" if pn.config.theme == "default" else "dark"
molstar = PDBeMolstar(molecule_id="1qyn", theme=theme, width="1150px")
parameters = pn.Param(
    molstar,
    parameters=[
        "molecule_id",
        "spin",
        "visual_style",
        "hide_water",
    ],
)
settings = pn.Column(parameters)
view = pn.Column(molstar, sizing_mode="stretch_width")

template = pn.template.FastListTemplate(
    title="MaterialTemplate",
    sidebar=[settings],
    main_max_width="1200px",
)

template.main.append(view)

if pn.state.served:
    template.servable()
