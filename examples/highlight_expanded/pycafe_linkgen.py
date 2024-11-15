import base64
import gzip
import json
from dataclasses import asdict
from pathlib import Path
from urllib.parse import quote

import pandas as pd
from viewer import AxisProperties, ColorTransform

pth = Path(__file__).parent
# pth = Path()

requirements = (pth / "requirements_view.txt").read_text()
code = (pth / "viewer.py").read_text()


def make_link(
    title: str,
    data: pd.DataFrame,
    molecule_id: str,
    colors: ColorTransform,
    axis_properties: AxisProperties,
    description: str = "",
):
    files = []
    settings_dict = {
        "title": title,
        "molecule_id": molecule_id,
        **asdict(colors),
        **asdict(axis_properties),
    }

    s = json.dumps(settings_dict)
    files.append({"name": "settings.json", "content": s})

    s = data.to_csv(index=False, lineterminator="\n")
    files.append({"name": "color_data.csv", "content": s})

    if description:
        files.append({"name": "description.md", "content": description})

    json_object = {
        "code": code,
        "requirements": requirements,
        "files": files,
    }
    json_text = json.dumps(json_object)

    compressed_json_text = gzip.compress(json_text.encode("utf8"))
    base64_text = base64.b64encode(compressed_json_text).decode("utf8")
    c = quote(base64_text)
    # use the c= argument, c stands for compressed
    url = f"https://py.cafe/snippet/solara/v1#c={c}"

    return url
