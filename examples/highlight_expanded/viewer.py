from __future__ import annotations

import json
from dataclasses import dataclass, fields

import altair as alt
import numpy as np
import pandas as pd
import solara
import solara.lab
from cmap import Colormap
from ipymolstar.widget import PDBeMolstar

base_v = np.vectorize(np.base_repr)
PAD_SIZE = 0.05  # when not autoscale Y size of padding used


def norm(x, vmin, vmax):
    return (x - vmin) / (vmax - vmin)


@dataclass
class ColorTransform:
    name: str
    vmin: float
    vmax: float
    missing_data_color: str
    highlight_color: str

    def molstar_colors(self, data: pd.DataFrame) -> dict:
        rgba_array = self.cmap(
            norm(data["value"], vmin=self.vmin, vmax=self.vmax), bytes=True
        )
        ints = rgba_array.astype(np.uint8).view(dtype=np.uint32).byteswap()
        padded = np.char.rjust(base_v(ints // 2**8, 16), 6, "0")
        hex_colors = np.char.add("#", padded).squeeze()

        color_data = {
            "data": [
                {"residue_number": resi, "color": hcolor.lower()}
                for resi, hcolor in zip(data["residue_number"], hex_colors)
            ],
            "nonSelectedColor": self.missing_data_color,
        }

        return color_data

    @property
    def cmap(self) -> Colormap:
        return Colormap(self.name, bad=self.missing_data_color)

    @property
    def altair_scale(self) -> alt.Scale:
        domain = np.linspace(self.vmin, self.vmax, 256, endpoint=True)
        scale = alt.Scale(domain=list(domain), range=self.cmap.to_altair(), clamp=True)
        return scale

    @classmethod
    def from_dict(cls, **kwargs) -> ColorTransform:
        accepted_kwargs = {
            k: v for k, v in kwargs.items() if k in {f.name for f in fields(cls)}
        }
        return cls(**accepted_kwargs)


@dataclass
class AxisProperties:
    label: str
    unit: str
    autoscale_y: bool = True

    @property
    def title(self) -> str:
        return f"{self.label} ({self.unit})"

    @classmethod
    def from_dict(cls, **kwargs) -> AxisProperties:
        accepted_kwargs = {
            k: v for k, v in kwargs.items() if k in {f.name for f in fields(cls)}
        }
        return cls(**accepted_kwargs)


def make_chart(
    data: pd.DataFrame, colors: ColorTransform, axis_properties: AxisProperties
) -> alt.LayerChart:
    ypad = (colors.vmax - colors.vmin) * 0.05
    xmin, xmax = data["residue_number"].min(), data["residue_number"].max()
    xpad = (xmax - xmin) * 0.05
    xscale = alt.Scale(domain=(xmin - xpad, xmax + xpad))
    if axis_properties.autoscale_y:
        y_scale = alt.Scale()
    else:
        y_scale = alt.Scale(domain=(colors.vmin - ypad, colors.vmax + ypad))

    # TODO zoom resets after highlight
    zoom_x = alt.selection_interval(
        bind="scales",
        encodings=["x"],
        zoom="wheel![!event.shiftKey]",
    )

    scatter = (
        alt.Chart(data)
        .mark_circle(interpolate="basis", size=200)
        .encode(
            x=alt.X("residue_number:Q", title="Residue Number", scale=xscale),
            y=alt.Y(
                "value:Q",
                title=axis_properties.title,
                scale=y_scale,
            ),
            color=alt.Color(
                "value:Q", scale=colors.altair_scale, title=axis_properties.title
            ),
        )
        .add_params(zoom_x)
    )

    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection_point(
        name="point",
        nearest=True,
        on="pointerover",
        fields=["residue_number"],
        empty=False,
        clear="mouseout",
    )

    select_residue = (
        alt.Chart(data)
        .mark_point()
        .encode(
            x="residue_number:Q",
            opacity=alt.value(0),
        )
        .add_params(nearest)
    )

    # Draw a rule at the location of the selection
    rule = (
        alt.Chart(data)
        .mark_rule(color=colors.highlight_color, size=2)
        .encode(
            x="residue_number:Q",
        )
        .transform_filter(nearest)
    )

    vline = (
        alt.Chart(pd.DataFrame({"x": [0]}))
        .mark_rule(color=colors.highlight_color, size=2)
        .encode(x="x:Q")
    )

    # Put the five layers into a chart and bind the data
    chart = (
        alt.layer(scatter, vline, select_residue, rule).properties(
            width="container",
            height=480,  # autosize height?
        )
        # .configure(autosize="fit")
    )

    return chart


@solara.component
def ScatterChart(
    data: pd.DataFrame,
    colors: ColorTransform,
    axis_properties: AxisProperties,
    on_selections,
    line_value,
):
    def mem_chart():
        chart = make_chart(data, colors, axis_properties)
        spec = chart.to_dict()
        return chart, spec

    chart, spec = solara.use_memo(
        mem_chart, dependencies=[data, colors, axis_properties]
    )

    data_name = spec["layer"][1]["data"]["name"]
    spec["datasets"][data_name] = [{"x": line_value}]
    view = alt.JupyterChart.element(
        chart=chart, spec=spec, embed_options={"actions": False}
    )

    def bind():
        real = solara.get_widget(view)
        real.selections.observe(on_selections, "point")

    solara.use_effect(bind, [data, colors])


@solara.component
def ProteinView(
    title: str,
    molecule_id: str,
    data: pd.DataFrame,
    colors: ColorTransform,
    axis_properties: AxisProperties,
    dark_effective: bool,
    description: str = "",
):
    about_dialog = solara.use_reactive(False)

    # residue number to highlight in altair chart
    line_number = solara.use_reactive(None)

    # residue number to highlight in protein view
    highlight_number = solara.use_reactive(None)

    color_data = colors.molstar_colors(data)
    tooltips = {
        "data": [
            {
                "residue_number": resi,
                "tooltip": f"{axis_properties.label}: {value:.2g} {axis_properties.unit}"
                if not np.isnan(value)
                else "No data",
            }
            for resi, value in zip(data["residue_number"], data["value"])
        ]
    }

    def on_molstar_mouseover(value):
        r = value.get("residueNumber", None)
        line_number.set(r)

    def on_molstar_mouseout(value):
        on_molstar_mouseover({})

    def on_chart_selection(event):
        try:
            r = event["new"].value[0]["residue_number"]
            highlight_number.set(r)
        except (IndexError, KeyError):
            highlight_number.set(None)

    with solara.AppBar():
        solara.AppBarTitle(title)
        if description:
            with solara.Tooltip("About"):
                solara.Button(
                    icon_name="mdi-information-outline",
                    icon=True,
                    on_click=lambda: about_dialog.set(True),
                )
        solara.lab.ThemeToggle()

    with solara.v.Dialog(
        v_model=about_dialog.value, on_v_model=lambda _ignore: about_dialog.set(False)
    ):
        with solara.Card(f"About", margin=0):
            solara.Markdown(description)

    with solara.ColumnsResponsive([4, 8]):
        with solara.Card(style={"height": "550px"}):
            PDBeMolstar.element(
                theme="dark" if dark_effective else "light",
                molecule_id=molecule_id.lower(),
                color_data=color_data,
                hide_water=True,
                tooltips=tooltips,
                height="525px",
                highlight={"data": [{"residue_number": int(highlight_number.value)}]}
                if highlight_number.value
                else None,
                highlight_color=colors.highlight_color,
                on_mouseover_event=on_molstar_mouseover,
                on_mouseout_event=on_molstar_mouseout,
            )
        with solara.Card(style={"height": "550px"}):
            ScatterChart(
                data,
                colors,
                axis_properties,
                on_chart_selection,
                line_number.value,
            )


@solara.component
def Page():
    dark_effective = solara.lab.use_dark_effective()
    dark_previous = solara.use_previous(dark_effective)

    if dark_previous != dark_effective:
        if dark_effective:
            alt.themes.enable("dark")
        else:
            alt.themes.enable("default")

    solara.Style(
        """
        .vega-embed {
        overflow: visible;
        width: 100% !important;
        }"""
    )

    settings = json.loads(Path("settings.json").read_text())

    colors = ColorTransform.from_dict(**settings)
    axis_properties = AxisProperties.from_dict(**settings)

    data = pd.read_csv("color_data.csv")

    ProteinView(
        settings["title"],
        molecule_id=settings["molecule_id"],
        data=data,
        colors=colors,
        axis_properties=axis_properties,
        dark_effective=dark_effective,
    ).key(f"ProteinView-{dark_effective}")  # redraw the app on theme change
