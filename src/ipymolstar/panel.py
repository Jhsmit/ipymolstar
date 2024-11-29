import pathlib
from typing import Optional

from ipymolstar.widget import THEMES, Color, QueryParam, ResetParam

try:
    import panel as pn
except ImportError:
    msg = "To use ipypmolstar as panel AnyWidgetComponent, the panel package needs to be installed"
    raise ImportError(msg)
import param
from panel.custom import AnyWidgetComponent


class PDBeMolstar(AnyWidgetComponent):
    _esm = pathlib.Path(__file__).parent / "widget.js"
    _stylesheets = [str(pathlib.Path(__file__).parent / "pdbe-light.css")]

    width = param.String(default="800px")
    height = param.String(default="500px")

    molecule_id = param.String()
    custom_data = param.Dict(default=None, allow_None=True)
    assembly_id = param.String(default="")
    default_preset = param.Selector(
        default="default", objects=["default", "unitcell", "all-models", "supercell"]
    )
    ligand_view = param.Dict(default=None)
    alphafold_view = param.Boolean(default=False)
    superposition = param.Boolean(default=False)
    superposition_params = param.Dict(default=None)
    visual_style = param.Selector(
        default=None,
        objects=[
            "cartoon",
            "ball-and-stick",
            "carbohydrate",
            "ellipsoid",
            "gaussian-surface" "molecular-surface",
            "point",
            "putty",
            "spacefill",
        ],
    )
    hide_polymer = param.Boolean(default=False)
    hide_water = param.Boolean(default=False)
    hide_heteroatoms = param.Boolean(default=False)
    hide_carbs = param.Boolean(default=False)
    hide_non_standard = param.Boolean(default=False)
    hide_coarse = param.Boolean(default=False)
    load_maps = param.Boolean(default=False)
    map_settings = param.Dict(default=None)
    bg_color = param.String(default="")
    highlight_color = param.String(default="#FF6699")
    select_color = param.String(default="#33FF19")
    lighting = param.Selector(
        default=None, objects=["flat", "matte", "glossy", "metallic", "plastic"]
    )
    validation_annotation = param.Boolean(default=False)
    domain_annotation = param.Boolean(default=False)
    symmetry_annotation = param.Boolean(default=False)
    pdbe_url = param.String(default="https://www.ebi.ac.uk/pdbe/")
    encoding = param.Selector(default="bcif", objects=["bcif", "cif"])
    low_precision_coords = param.Boolean(default=False)
    select_interaction = param.Boolean(default=True)
    granularity = param.Selector(
        default="residue",
        objects=[
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
    )
    subscribe_events = param.Boolean(default=False)
    hide_controls = param.Boolean(default=True)
    hide_controls_icon = param.Boolean(default=False)
    hide_expand_icon = param.Boolean(default=False)
    hide_settings_icon = param.Boolean(default=False)
    hide_selection_icon = param.Boolean(default=False)
    hide_animation_icon = param.Boolean(default=False)
    sequence_panel = param.Boolean(default=False)
    pdbe_link = param.Boolean(default=True)
    loading_overlay = param.Boolean(default=False)
    expanded = param.Boolean(default=False)
    landscape = param.Boolean(default=False)
    reactive = param.Boolean(default=False)

    spin = param.Boolean(default=False)
    _focus = param.List(default=None)
    highlight = param.Dict(default=None)
    _clear_highlight = param.Boolean(default=False)
    color_data = param.Dict(default=None)
    _clear_selection = param.Boolean(default=False)
    tooltips = param.Dict(default=None)
    _clear_tooltips = param.Boolean(default=False)
    _set_color = param.Dict(default=None)
    _reset = param.Dict(default=None)
    _update = param.Dict(default=None)
    _args = param.Dict(default={})

    mouseover_event = param.Dict(default={})
    mouseout_event = param.Boolean(default=False)
    click_event = param.Dict(default={})
    click_focus = param.Boolean(default=True)

    def __init__(self, theme="light", **params):
        _stylesheets = [THEMES[theme]["css"]]
        bg_color = params.pop("bg_color", THEMES[theme]["bg_color"])
        self._stylesheets = _stylesheets  # shouldnt work but it does

        super().__init__(bg_color=bg_color, **params)

    def color(
        self,
        data: list[QueryParam],
        non_selected_color=None,
        keep_colors=False,
        keep_representations=False,
    ) -> None:
        """
        Alias for PDBE Molstar's `select` method.

        See https://github.com/molstar/pdbe-molstar/wiki/3.-Helper-Methods for parameter
        details
        """

        self.color_data = {
            "data": data,
            "nonSelectedColor": non_selected_color,
            "keepColors": keep_colors,
            "keepRepresentations": keep_representations,
        }
        self.color_data = None

    def focus(self, data: list[QueryParam]):
        self._focus = data
        self._focus = None

    def clear_highlight(self):
        self._clear_highlight = not self._clear_highlight

    def clear_tooltips(self):
        self._clear_tooltips = not self._clear_tooltips

    def clear_selection(self, structure_number=None):
        # move payload to the traitlet which triggers the callback
        self._args = {"number": structure_number}
        self._clear_selection = not self._clear_selection

    # todo make two traits: select_color, hightlight_color
    def set_color(
        self, highlight: Optional[Color] = None, select: Optional[Color] = None
    ):
        data = {}
        if highlight is not None:
            data["highlight"] = highlight
        if select is not None:
            data["select"] = select
        if data:
            self._set_color = data
            self._set_color = None

    def reset(self, data: ResetParam):
        self._reset = data
        self._reset = None

    def update(self, data):
        self._update = data
        self._update = None
