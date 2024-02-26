import pathlib

import anywidget
import traitlets


THEMES = {
    "light": {
        "bg_color": "#F7F7F7",
        "css": (pathlib.Path(__file__).parent / "pdbe-light.css").read_text(),
    },
    "dark": {
        "bg_color": "#111111",
        "css": (pathlib.Path(__file__).parent / "pdbe-dark.css").read_text(),
    },
}


class PDBeMolstar(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "widget.js"
    _css = pathlib.Path(__file__).parent / "pdbe-light.css"
    value = traitlets.Int(0).tag(sync=True)

    molecule_id = traitlets.Unicode().tag(sync=True)
    custom_data = traitlets.Dict(default_value=None, allow_none=True).tag(sync=True)

    bg_color = traitlets.Unicode().tag(sync=True)

    spin = traitlets.Bool(False).tag(sync=True)

    hide_polymer = traitlets.Bool(False).tag(sync=True)
    hide_water = traitlets.Bool(False).tag(sync=True)
    hide_heteroatoms = traitlets.Bool(False).tag(sync=True)
    hide_carbs = traitlets.Bool(False).tag(sync=True)
    hide_non_standard = traitlets.Bool(False).tag(sync=True)
    hide_coarse = traitlets.Bool(False).tag(sync=True)

    _select = traitlets.Dict().tag(sync=True)

    def __init__(self, theme="light", **kwargs):
        _css = THEMES[theme]["css"]
        bg_color = kwargs.pop("bg_color", THEMES[theme]["bg_color"])
        super().__init__(_css=_css, bg_color=bg_color, **kwargs)

    def color(self, data, non_selected_color=None):
        """
        Alias for PDBE Molstar's `select` method.

        See https://github.com/molstar/pdbe-molstar/wiki/3.-Helper-Methods for parameter
        details
        """

        self._select = {"data": data, "nonSelectedColor": non_selected_color}
