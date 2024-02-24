import pathlib

import anywidget
import traitlets


class PDBeMolstar(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "widget.js"
    _css = pathlib.Path(__file__).parent / "widget.css"
    value = traitlets.Int(0).tag(sync=True)

    molecule_id = traitlets.Unicode().tag(sync=True)
    custom_data = traitlets.Dict(default_value=None, allow_none=True).tag(sync=True)

    bg_color = traitlets.Unicode("#F7F7F7").tag(sync=True)

    spin = traitlets.Bool(False).tag(sync=True)

    hide_polymer = traitlets.Bool(False).tag(sync=True)
    hide_water = traitlets.Bool(False).tag(sync=True)
    hide_heteroatoms = traitlets.Bool(False).tag(sync=True)
    hide_carbs = traitlets.Bool(False).tag(sync=True)
    hide_non_standard = traitlets.Bool(False).tag(sync=True)
    hide_coarse = traitlets.Bool(False).tag(sync=True)

    _select = traitlets.Dict().tag(sync=True)

    # def __init__(self, *args, **kwargs):
    #     print(self._css)
    #     _css = (pathlib.Path(__file__).parent / "widget.css").read_text()
    #     super().__init__(*args,  _css=_css, **kwargs)

    def color(self, data, non_selected_color=None):
        """
        Alias for PDBE Molstar's `select` method.

        See https://github.com/molstar/pdbe-molstar/wiki/3.-Helper-Methods for parameter
        details
        """

        self._select = {"data": data, "nonSelectedColor": non_selected_color}
