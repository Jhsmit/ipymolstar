import pathlib
from typing import Any, List, Optional, TypedDict

import anywidget
import traitlets

THEMES = {
    "light": {
        "bg_color": "#F7F7F7",
        "css": (
            pathlib.Path(__file__).parent / "static" / "pdbe-light.css"
        ).read_text(),
    },
    "dark": {
        "bg_color": "#111111",
        "css": (pathlib.Path(__file__).parent / "static" / "pdbe-dark.css").read_text(),
    },
}


class Color(TypedDict):
    r: int
    g: int
    b: int


# codeieum translation of QueryParam from
# https://github.com/molstar/pdbe-molstar/blob/master/src/app/helpers.ts#L180
class QueryParam(TypedDict, total=False):
    auth_seq_id: Optional[int]
    entity_id: Optional[str]
    auth_asym_id: Optional[str]
    struct_asym_id: Optional[str]
    residue_number: Optional[int]
    start_residue_number: Optional[int]
    end_residue_number: Optional[int]
    auth_residue_number: Optional[int]
    auth_ins_code_id: Optional[str]
    start_auth_residue_number: Optional[int]
    start_auth_ins_code_id: Optional[str]
    end_auth_residue_number: Optional[int]
    end_auth_ins_code_id: Optional[str]
    atoms: Optional[List[str]]
    label_comp_id: Optional[str]
    color: Optional[Color]
    sideChain: Optional[bool]
    representation: Optional[str]
    representationColor: Optional[Color]
    focus: Optional[bool]
    tooltip: Optional[str]
    start: Optional[Any]
    end: Optional[Any]
    atom_id: Optional[List[int]]
    uniprot_accession: Optional[str]
    uniprot_residue_number: Optional[int]
    start_uniprot_residue_number: Optional[int]
    end_uniprot_residue_number: Optional[int]


class ResetParam(TypedDict, total=False):
    camera: Optional[bool]
    theme: Optional[bool]
    highlightColor: Optional[bool]
    selectColor: Optional[bool]


class PDBeMolstar(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "pdbemolstar.js"
    _css = pathlib.Path(__file__).parent / "static" / "pdbe-light.css"

    width = traitlets.Unicode("100%").tag(sync=True)
    height = traitlets.Unicode("500px").tag(sync=True)

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
    hide_controls = traitlets.Bool(True).tag(sync=True)
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
    _focus = traitlets.List(default_value=None, allow_none=True).tag(sync=True)
    highlight = traitlets.Dict(default_value=None, allow_none=True).tag(sync=True)
    _clear_highlight = traitlets.Bool(default_value=False).tag(sync=True)
    color_data = traitlets.Dict(default_value=None, allow_none=True).tag(sync=True)
    _clear_selection = traitlets.Bool(default_value=False).tag(sync=True)
    tooltips = traitlets.Dict(default_value=None, allow_none=True).tag(sync=True)
    _clear_tooltips = traitlets.Bool(default_value=False).tag(sync=True)
    _set_color = traitlets.Dict(default_value=None, allow_none=True).tag(sync=True)
    _reset = traitlets.Dict(allow_none=True, default_value=None).tag(sync=True)
    _update = traitlets.Dict(allow_none=True, default_value=None).tag(sync=True)

    _args = traitlets.Dict().tag(sync=True)

    mouseover_event = traitlets.Dict().tag(sync=True)
    mouseout_event = traitlets.Bool().tag(sync=True)
    click_event = traitlets.Dict().tag(sync=True)
    click_focus = traitlets.Bool(True).tag(sync=True)

    def __init__(self, theme="light", **kwargs):
        _css = THEMES[theme]["css"]
        bg_color = kwargs.pop("bg_color", THEMES[theme]["bg_color"])
        super().__init__(_css=_css, bg_color=bg_color, **kwargs)

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
