import panel as pn
import param
from ipymolstar.panel import PDBeMolstar

theme = "light" if pn.config.theme == "default" else "dark"


protein_store = ["1QYN", "2PE4"]
molecule_store = {
    "Glucose": dict(
        url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/conformers/000016A100000001/SDF?response_type=save&response_basename=Conformer3D_COMPOUND_CID_5793",
        format="sdf",
        binary=False,
    ),
    "ATP": dict(
        url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/5957/record/SDF?record_type=3d&response_type=save&response_basename=Conformer3D_COMPOUND_CID_5957",
        format="sdf",
        binary=False,
    ),
    "Caffeine": dict(
        url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/2519/record/SDF?record_type=3d&response_type=save&response_basename=Conformer3D_COMPOUND_CID_2519",
        format="sdf",
        binary=False,
    ),
    "Strychnine": dict(
        url=" https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/441071/record/SDF?record_type=3d&response_type=save&response_basename=Conformer3D_COMPOUND_CID_441071 ",
        format="sdf",
        binary=False,
    ),
}


class Controller(param.Parameterized):
    structure_type = param.Selector(
        default="Protein",
        allow_None=False,
        objects=["Protein", "Molecule"],
        doc="Choose to display protein or a small molecule",
    )

    protein_id = param.Selector(
        default=protein_store[0],
        objects=protein_store,
        doc="Protein to display",
    )

    molecule_id = param.Selector(
        default="Glucose",
        objects=list(molecule_store.keys()),
        doc="Molecule to display",
    )

    def __init__(self, molstar_view: PDBeMolstar, **params):
        self.molstar_view = molstar_view
        super().__init__(**params)

    @param.depends("structure_type")
    def secondary_selector(self):
        if self.structure_type == "Protein":
            return pn.widgets.Select.from_param(self.param.protein_id, name="Protein")
        elif self.structure_type == "Molecule":
            return pn.widgets.Select.from_param(self.param.molecule_id, name="Molecule")
        else:
            return pn.pane.Str("Please make a selection")

    @param.depends("structure_type", "protein_id", "molecule_id", watch=True)
    def update_molecule_data(self):
        if self.structure_type == "Protein":
            molecule_id = self.protein_id.lower()
            custom_data = None
        else:
            molecule_id = ""
            custom_data = molecule_store[self.molecule_id]

        self.molstar_view.param.update(molecule_id=molecule_id, custom_data=custom_data)


molstar = PDBeMolstar(
    molecule_id="1qyn", theme=theme, sizing_mode="stretch_width"
)  # , width="1150px")


parameters = pn.Param(
    molstar,
    parameters=[
        "spin",
        "visual_style",
        "hide_water",
        "hide_polymer",
        "hide_heteroatoms",
        "hide_carbs",
        "hide_non_standard",
        "hide_coarse",
        "bg_color",
    ],
    widgets={
        "bg_color": {"type": pn.widgets.ColorPicker, "sizing_mode": "stretch_width"}
    },
    show_name=False,
)

ctrl = Controller(molstar)


settings = pn.Column(
    pn.pane.Markdown("## Controls"),
    pn.widgets.Select.from_param(ctrl.param.structure_type, name="Structure type"),
    ctrl.secondary_selector,
    *parameters,
)
view = pn.Column(molstar, sizing_mode="stretch_width")

template = pn.template.FastListTemplate(
    title="MaterialTemplate",
    sidebar=[settings],
    main_max_width="1200px",
)

template.main.append(view)

if pn.state.served:
    template.servable()
