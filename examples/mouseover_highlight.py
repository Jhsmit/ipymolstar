"""
Example solara app with two-way hover/highlight between ipymolstar and altair
"""

# %%
from pathlib import Path

import altair as alt
import numpy as np
import pandas as pd
import solara
from cmap import Colormap
from ipymolstar.widget import PDBeMolstar

# color limits in kJ/mol
VMIN = 10
VMAX = 40
NO_COVERAGE = "#8c8c8c"
HIGHLIGHT_COLOR = "#e933f8"
cmap = Colormap("tol:rainbow_PuRd_r", bad=NO_COVERAGE)
domain = np.linspace(VMIN, VMAX, 256, endpoint=True)
scale = alt.Scale(domain=list(domain), range=cmap.to_altair())

# %%


def norm(x, vmin=VMIN, vmax=VMAX):
    return (x - vmin) / (vmax - vmin)


# %%
script_path = Path(__file__).parent
kwargs = {"comment": "#", "header": [0]}
data = pd.read_csv(script_path / "pyhdx_secb_deltaG.csv", **kwargs).rename(
    columns={"r_number": "residue"}
)
data = data.drop(data.index[-1])[["residue", "deltaG"]]
data["deltaG"] *= 1e-3


# %%
cmap = Colormap("tol:rainbow_PuRd_r", bad=NO_COVERAGE)

rgba_array = cmap(norm(data["deltaG"]), bytes=True)
base_v = np.vectorize(np.base_repr)
ints = rgba_array.astype(np.uint8).view(dtype=np.uint32).byteswap()
padded = np.char.rjust(base_v(ints // 2**8, 16), 6, "0")
hex_colors = np.char.add("#", padded).squeeze()

# %%
color_data = {
    "data": [
        {"residue_number": resi, "color": hcolor.lower()}
        for resi, hcolor in zip(data["residue"], hex_colors)
    ],
    "nonSelectedColor": NO_COVERAGE,
}

# %%

tooltips = {
    "data": [
        {
            "residue_number": resi,
            "tooltip": f"ΔG: {value:.2f} kJ/mol"
            if not np.isnan(value)
            else "No coverage",
        }
        for resi, value in zip(data["residue"], data["deltaG"])
    ]
}


# Create a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection_point(
    name="point",
    nearest=True,
    on="pointerover",
    fields=["residue"],
    empty=False,
    clear="mouseout",
)

pad = (VMAX - VMIN) * 0.05

# The basic scatter
scatter = (
    alt.Chart(data)
    .mark_circle(interpolate="basis", size=200)
    .encode(
        x=alt.X("residue:Q", title="Residue Number"),
        y=alt.Y(
            "deltaG:Q",
            title="ΔG (kJ/mol)",
            scale=alt.Scale(domain=(VMAX + pad, VMIN - pad)),
        ),
        color=alt.Color("deltaG:Q", scale=scale, title="ΔG (kJ/mol)"),
    )
)

# %%

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = (
    alt.Chart(data)
    .mark_point()
    .encode(
        x="residue:Q",
        opacity=alt.value(0),
    )
    .add_params(nearest)
)

# Draw a rule at the location of the selection
rule = (
    alt.Chart(data)
    .mark_rule(color="gray", size=2)
    .encode(
        x="residue:Q",
    )
    .transform_filter(nearest)
)

vline = (
    alt.Chart(pd.DataFrame({"x": [0]}))
    .mark_rule(color=HIGHLIGHT_COLOR, size=2)
    .encode(x="x:Q")
)


# Put the five layers into a chart and bind the data
chart = (
    alt.layer(scatter, vline, selectors, rule).properties(
        width="container",
        height=480,  # autosize height?
    )
    # .configure(autosize="fit")
)

spec = chart.to_dict()
data_name = spec["layer"][1]["data"]["name"]


@solara.component
def SelectChart(on_selections, line_value):
    spec["datasets"][data_name] = [{"x": line_value}]
    view = alt.JupyterChart.element(
        chart=chart, spec=spec, embed_options={"actions": False}
    )

    def bind():
        real = solara.get_widget(view)
        real.selections.observe(on_selections, "point")

    solara.use_effect(bind, [])


@solara.component
def Page():
    # residue number to highlight in altair chart
    line_number = solara.use_reactive(None)

    # residue number to highlight in protein view
    highlight_number = solara.use_reactive(None)
    with solara.AppBar():
        solara.AppBarTitle("altair/ipymolstar bidirectional highlight")
    solara.Style(
        """
        .vega-embed {
        overflow: visible;
        width: 100% !important;
        height: 800px !important;
        }"""
    )

    def on_mouseover(value):
        r = value.get("residueNumber", None)
        line_number.set(r)

    def on_mouseout(value):
        on_mouseover({})

    def on_selections(event):
        try:
            r = event["new"].value[0]["residue"]
            highlight_number.set(r)
        except (IndexError, KeyError):
            highlight_number.set(None)

    with solara.ColumnsResponsive([4, 8]):
        with solara.Card(style={"height": "550px"}):
            PDBeMolstar.element(
                molecule_id="1qyn",
                color_data=color_data,
                hide_water=True,
                tooltips=tooltips,
                height="500px",
                highlight={"data": [{"residue_number": int(highlight_number.value)}]}
                if highlight_number.value
                else None,
                highlight_color=HIGHLIGHT_COLOR,
                on_mouseover_event=on_mouseover,
                on_mouseout_event=on_mouseout,
            )
        with solara.Card(style={"height": "550px"}):
            SelectChart(on_selections, line_number.value)


# %%
