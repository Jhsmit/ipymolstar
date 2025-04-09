import anywidget
import pathlib
import traitlets

# https://github.com/molstar/molstar/blob/80415a2771fcddbca3cc13ddba4be10c92a1454b/src/apps/viewer/app.ts#L88
DEFAULT_VIEWER_OPTIONS = {
    "layoutIsExpanded": False,
    "layoutShowControls": False,
}

# https://github.com/molstar/molstar/blob/80415a2771fcddbca3cc13ddba4be10c92a1454b/src/extensions/mvs/load.ts#L37
DEFAULT_MVS_LOAD_OPTIONS = {
    "replaceExisting": True,
    "sanityChecks": True,
}


class MolViewSpec(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "molviewspec.js"
    _css = pathlib.Path(__file__).parent / "static" / "molviewspec.css"

    width = traitlets.Unicode("100%").tag(sync=True)
    height = traitlets.Unicode("500px").tag(sync=True)
    msvj_data = traitlets.Unicode("").tag(sync=True)

    viewer_options = traitlets.Dict(DEFAULT_VIEWER_OPTIONS).tag(sync=True)
    mvs_load_options = traitlets.Dict(DEFAULT_MVS_LOAD_OPTIONS).tag(sync=True)
