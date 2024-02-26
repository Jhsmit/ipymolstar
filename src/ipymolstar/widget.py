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
    assembly_id = traitlets.Unicode().tag(sync=True)
    default_preset = traitlets.Enum(
        ["default", "unitcell", "all-models", "supercell"],
        default_value="default",
    ).tag(sync=True)
    ligand_view = traitlets.Dict(default_value=None, allow_none=True).tag(sync=True)
    alphafold_view = traitlets.Bool(default_value=False).tag(sync=True)
    superposition = traitlets.Bool(default_value=False).tag(sync=True)
    superposition_params = traitlets.Dict(default_value=None, allow_none=True).tag(
        sync=True
    )
    visual_style = traitlets.Enum(
        [
            "cartoon",
            "ball-and-stick",
            "carbohydrate",
            "ellipsoid",
            "gaussian-surface",
            "molecular-surface",
            "point",
            "putty",
            "spacefill",
        ],
        default_value=None,
        allow_none=True,
    ).tag(sync=True)
    hide_polymer = traitlets.Bool(False).tag(sync=True)
    hide_water = traitlets.Bool(False).tag(sync=True)
    hide_heteroatoms = traitlets.Bool(False).tag(sync=True)
    hide_carbs = traitlets.Bool(False).tag(sync=True)
    hide_non_standard = traitlets.Bool(False).tag(sync=True)
    hide_coarse = traitlets.Bool(False).tag(sync=True)
    load_maps = traitlets.Bool(False).tag(sync=True)
    map_settings = traitlets.Dict(default_value=None, allow_none=True).tag(sync=True)
    bg_color = traitlets.Unicode().tag(sync=True)
    highlight_color = traitlets.Unicode("#FF6699").tag(sync=True)
    select_color = traitlets.Unicode("#33FF19").tag(sync=True)
    lighting = traitlets.Enum(
        ["flat", "matte", "glossy", "metallic", "plastic"],
        default_value=None,
        allow_none=True,
    ).tag(sync=True)
    validation_annotation = traitlets.Bool(False).tag(sync=True)
    domain_annotation = traitlets.Bool(False).tag(sync=True)
    symmetry_annotation = traitlets.Bool(False).tag(sync=True)
    pdbe_url = traitlets.Unicode("https://www.ebi.ac.uk/pdbe/").tag(sync=True)
    encoding = traitlets.Enum(["bcif", "cif"], default_value="bcif").tag(sync=True)
    low_precision_coords = traitlets.Bool(False).tag(sync=True)
    select_interaction = traitlets.Bool(True).tag(sync=True)
    granularity = traitlets.Enum(
        [
            "element",
            "residue",
            "chain",
            "entity",
            "model",
            "operator",
            "structure",
            "elementInstances",
            "residueInstances",
            "chainInstances",
        ],
        default_value="residue",
    ).tag(sync=True)
    subscribe_events = traitlets.Bool(False).tag(sync=True)
    hide_controls = traitlets.Bool(False).tag(sync=True)
    hide_controls_icon = traitlets.Bool(False).tag(sync=True)
    hide_expand_icon = traitlets.Bool(False).tag(sync=True)
    hide_settings_icon = traitlets.Bool(False).tag(sync=True)
    hide_selection_icon = traitlets.Bool(False).tag(sync=True)
    hide_animation_icon = traitlets.Bool(False).tag(sync=True)
    sequence_panel = traitlets.Bool(False).tag(sync=True)
    pdbe_link = traitlets.Bool(True).tag(sync=True)
    loading_overlay = traitlets.Bool(False).tag(sync=True)
    expanded = traitlets.Bool(False).tag(sync=True)
    landscape = traitlets.Bool(False).tag(sync=True)
    reactive = traitlets.Bool(False).tag(sync=True)

    spin = traitlets.Bool(False).tag(sync=True)
    _focus = traitlets.Dict().tag(sync=True)
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
