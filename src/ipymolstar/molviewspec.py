import anywidget
import pathlib
import traitlets


class MolViewSpec(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "molviewspec_widget.js"
    _css = pathlib.Path(__file__).parent / "molstar.css"

    width = traitlets.Unicode("100%").tag(sync=True)
    height = traitlets.Unicode("500px").tag(sync=True)
    schema = traitlets.Unicode("").tag(sync=True)
    test123 = traitlets.Unicode("").tag(sync=True)
