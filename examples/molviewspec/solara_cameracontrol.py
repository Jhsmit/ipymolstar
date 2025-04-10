from io import StringIO
import requests
import solara
from molviewspec import create_builder
from ipymolstar.molviewspec import MolViewSpec
import math
import copy
from molviewspec import GlobalMetadata

from Bio.PDB import PDBParser
import numpy as np
import solara.lab


# https://github.com/molstar/mol-view-spec/blob/def8ad6cdc351dbe01e29bf717e58e004bd10408/molviewspec/app/api/examples.py#L1819
def target_spherical_to_tpu(
    target: tuple[float, float, float],
    phi: float = 0,
    theta: float = 0,
    radius: float = 100,
):
    x, y, z = target
    phi, theta = math.radians(phi), math.radians(theta)
    direction = (
        -math.sin(phi) * math.cos(theta),
        -math.sin(theta),
        -math.cos(phi) * math.cos(theta),
    )
    position = (
        x - direction[0] * radius,
        y - direction[1] * radius,
        z - direction[2] * radius,
    )
    up = (0, 1, 0)
    return target, position, up


def fetch_pdb(pdb_id) -> StringIO:
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url)
    if response.status_code == 200:
        sio = StringIO(response.text)
        sio.seek(0)
        return sio
    else:
        raise requests.HTTPError(f"Failed to download PDB file {pdb_id}")


def load_structure(pdb_id: str):
    parser = PDBParser()
    structure = parser.get_structure(pdb_id, fetch_pdb(pdb_id))

    return structure


# %%
def calculate_com(structure) -> tuple[float, float, float]:
    # Collect C-alpha atom coordinates
    ca_coords = []

    for model in structure:
        for chain in model:
            for residue in chain:
                if "CA" in residue:  # Check for C-alpha atom
                    ca_coords.append(residue["CA"].coord)

    # Compute average (center of mass)
    ca_coords = np.array(ca_coords)
    return tuple(float(f) for f in np.mean(ca_coords, axis=0))


metadata = GlobalMetadata(
    title=None,
    description=None,
    description_format=None,
)


@solara.component
def Page():
    pdb_id = solara.use_reactive("1qyn")
    radius = solara.use_reactive(100.0)
    phi = solara.use_reactive(0.0)
    theta = solara.use_reactive(0.0)

    with solara.AppBar():
        solara.AppBarTitle("MolViewSpec + Solara: Camera control from python")

    def load_structure_and_com():
        builder = create_builder()
        (
            builder.download(url=f"https://files.rcsb.org/download/{pdb_id.value}.pdb")
            .parse(format="pdb")
            .model_structure()
            .component()
            .representation()
            .color(color="blue")
        )

        structure = load_structure(pdb_id.value)
        com = calculate_com(structure)

        return builder, com

    load_task = solara.lab.use_task(load_structure_and_com, dependencies=[pdb_id.value])

    def rot_phi(value):
        new_value = (phi.value + value) % 360
        phi.set(new_value)

    def rot_theta(value):
        new_value = (theta.value + value) % 360
        theta.set(new_value)

    with solara.ColumnsResponsive([4, 8]):
        with solara.Card("Controls"):
            solara.InputText(label="PDB ID", value=pdb_id)
            solara.SliderFloat(label="Radius", value=radius, min=50, max=200, step=0.5)
            solara.SliderFloat(label="Phi", value=phi, min=0, max=360, step=1)
            solara.SliderFloat(label="Theta", value=theta, min=0, max=360, step=1)
            with solara.Row(justify="space-between"):
                solara.Button(label="-90° y", on_click=lambda: rot_phi(-90))
                solara.Button(label="+90° y", on_click=lambda: rot_phi(90))
                solara.Button(label="-90° x", on_click=lambda: rot_theta(-90))
                solara.Button(label="+90° x", on_click=lambda: rot_theta(90))

        with solara.Card("Protein view"):
            if load_task.latest is None:
                solara.Markdown("Loading...")
            else:
                builder, com = (
                    load_task.value if load_task.finished else load_task.latest
                )

                target, position, up = target_spherical_to_tpu(
                    target=com,
                    phi=phi.value,
                    theta=theta.value,
                    radius=radius.value,
                )
                local_builder = copy.deepcopy(builder)
                local_builder.camera(target=target, position=position, up=up)
                msvj_data = local_builder.get_state()
                with solara.Div(style="opacity: 0.3" if load_task.pending else None):
                    view = MolViewSpec.element(msvj_data=msvj_data)
