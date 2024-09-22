import pathlib

try:
    import panel as pn
except ImportError:
    msg = "To use ipypmolstar as panel AnyWidgetComponent, the panel package needs to be installed"
    raise ImportError(msg)
import param
from panel.custom import AnyWidgetComponent


class PDBeMolstarPane(AnyWidgetComponent):
    _esm = pathlib.Path(__file__).parent / "widget.js"
    _stylesheets = [str(pathlib.Path(__file__).parent / "pdbe-light.css")]
    molecule_id = param.String(default="1qyn")


if pn.state.served:
    molstar = PDBeMolstarPane()
    parameters = pn.Param(molstar, parameters=["molecule_id"])
    settings = pn.Column(parameters)
    pn.FlexBox(settings, molstar).servable()
