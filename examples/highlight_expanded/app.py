from pathlib import Path

import altair as alt
import ipywidgets
import pandas as pd
import pyperclip
import solara
from cmap import Catalog, Colormap
from pycafe_linkgen import make_link
from viewer import AxisProperties, ColorTransform, ProteinView

DEFAULT_CMAP = "tol:rainbow_PuRd"
VMIN_DEFAULT = 0.0
VMAX_DEFAULT = 1.0
HIGHLIGHT_COLOR = "#e933f8"
MISSING_DATA_COLOR = "#8c8c8c"
CMAP_OPTIONS = list(Catalog().namespaced_keys())

# TODO color pickers formatting


# VMIN_DEFAULT =

# column selection
# test button
# -> seca data
# revert vmin vmax defaults

# DONE


# %%


# script_path = Path(__file__).parent
# kwargs = {"comment": "#", "header": [0]}
# data = pd.read_csv(script_path.parent / "pyhdx_secb_deltaG.csv", **kwargs).rename(
#     columns={"r_number": "residue"}
# )
# data = data.drop(data.index[-1])[["residue", "deltaG"]]
# data["deltaG"] *= 1e-3

# test_data = data.rename(columns={"residue": "residue_number", "deltaG": "value"})

# data.rename(columns={"residue": "residue_number", "deltaG": "value"}).to_csv(
#     "test_data.csv", index=False
# )

import numpy as np

# TESTING TODO REMOVE

N = 200
my_data = pd.DataFrame(
    {
        "resi": np.arange(N),
        "data1": np.sin(np.arange(N) / 10.0),
        "data2": np.random.rand(N),
    }
)

R_DEFAULT = "resi"
V_DEFAULT = "data1"

# %%
empty_frame = pd.DataFrame()
empty_frame = my_data


@solara.component
def Page():
    solara.Style(
        """
        .vega-embed {
        overflow: visible;
        width: 100% !important;
        }"""
    )

    dark_effective = solara.lab.use_dark_effective()
    dark_previous = solara.use_previous(dark_effective)

    if dark_previous != dark_effective:
        if dark_effective:
            alt.themes.enable("dark")
        else:
            alt.themes.enable("default")

    title = solara.use_reactive("My annotated protein view")
    description = solara.use_reactive("")
    pdb_id = solara.use_reactive("1QYN")
    data = solara.use_reactive(empty_frame)
    warning_text = solara.use_reactive("")

    residue_column = solara.use_reactive(R_DEFAULT)
    color_column = solara.use_reactive(V_DEFAULT)

    label = solara.use_reactive("value")
    unit = solara.use_reactive("au")

    highlight_color = solara.use_reactive(HIGHLIGHT_COLOR)
    missing_data_color = solara.use_reactive(MISSING_DATA_COLOR)
    autoscale_y = solara.use_reactive(True)

    cmap_name = solara.use_reactive(DEFAULT_CMAP)
    reverse = solara.use_reactive(False)
    full_cmap_name = cmap_name.value + "_r" if reverse.value else cmap_name.value
    cmap = Colormap(full_cmap_name)

    vmin = solara.use_reactive(VMIN_DEFAULT)
    vmax = solara.use_reactive(VMAX_DEFAULT)
    diverging = solara.use_reactive(False)

    png_bytes = cmap._repr_png_(height=24)

    def on_file(value: solara.components.file_drop.FileInfo):
        df = pd.read_csv(value["file_obj"])
        if len(df.columns) < 2:
            warning_text.set(f"Expected at least 2 columns, got {len(df.columns)}")
            data.set(pd.DataFrame())
            return

        warning_text.set("")
        data.set(df)
        residue_column.set(df.columns[0])
        color_column.set(df.columns[1])

    colors = ColorTransform(
        name=full_cmap_name,
        vmin=vmin.value,
        vmax=vmax.value,
        missing_data_color=missing_data_color.value,
        highlight_color=highlight_color.value,
    )

    axis_props = AxisProperties(
        label=label.value,
        unit=unit.value,
        autoscale_y=autoscale_y.value,
    )

    data_view = data.value.rename(
        columns={residue_column.value: "residue_number", color_column.value: "value"}
    )[["residue_number", "value"]]

    ProteinView(
        title.value,
        molecule_id=pdb_id.value,
        data=data_view,
        colors=colors,
        axis_properties=axis_props,
        dark_effective=dark_effective,
        description=description.value,
    ).key(f"ProteinView-{dark_effective}")  # redraw the app on theme change

    with solara.Sidebar():
        with solara.Card("Settings"):
            solara.InputText(label="Title", value=title)
            solara.InputText(label="PDB ID", value=pdb_id)
            solara.FileDrop(
                label="Drop .csv file with residue/color data", on_file=on_file
            )

            if warning_text.value:
                solara.Warning(warning_text.value)

            if not data.value.empty:
                with solara.Row():
                    solara.Select(
                        label="Residue Column",
                        value=residue_column,
                        values=list(data.value.columns),
                    )
                    solara.Select(
                        label="Color Column",
                        value=color_column,
                        values=list(data.value.columns),
                    )

            with solara.Row():
                solara.InputText(label="Label", value=label)
                solara.InputText(label="Unit", value=unit)

            solara.Text("Colors")
            with solara.Row(gap="10px", justify="space-around"):
                btn = solara.Button("Highlight", color=highlight_color.value)
                with solara.lab.Menu(activator=btn, close_on_content_click=False):
                    solara.v.ColorPicker(
                        v_model=highlight_color.value,
                        on_v_model=highlight_color.set,
                    )
                btn = solara.Button("Missing data", color=missing_data_color.value)
                with solara.lab.Menu(activator=btn, close_on_content_click=False):
                    solara.v.ColorPicker(
                        v_model=missing_data_color.value,
                        on_v_model=missing_data_color.set,
                    )

            with solara.Row():
                # solara.v.ColorPicker()

                solara.Checkbox(label="Autoscale Y", value=autoscale_y)

            with solara.Row():
                solara.v.Autocomplete(
                    v_model=cmap_name.value,
                    on_v_model=cmap_name.set,
                    items=CMAP_OPTIONS,
                )
                solara.Checkbox(label="Reverse", value=reverse)

            with solara.Row():

                def set_vmin(value: float):
                    if diverging.value:
                        vmin.set(value)
                        vmax.set(-value)
                    else:
                        vmin.set(value)

                solara.InputFloat(
                    label="vmin",
                    value=vmin.value,
                    on_value=set_vmin,
                )
                solara.InputFloat(
                    label="vmax",
                    value=vmax,
                    disabled=diverging.value,
                )
                with solara.Tooltip("Sets normalization range symmetric around zero"):
                    solara.Checkbox(label="Diverging", value=diverging)

            solara.Image(png_bytes, width="100%")
            solara.InputTextArea(
                label="Description", value=description, continuous_update=True
            )
            solara.Div(style={"height": "10px"})

            def to_cafe():
                url = make_link(
                    title=title.value,
                    data=data_view,
                    molecule_id=pdb_id.value,
                    colors=colors,
                    axis_properties=axis_props,
                    description=description.value,
                )
                print(url)
                pyperclip.copy(url)

            solara.Button("Copy PyCafé link", block=True, on_click=to_cafe)


# %%
