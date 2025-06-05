"""
This is an example from the Kingdon Teahouse (https://github.com/tBuLi/teahouse); adapted for ipymolstar.

Original example is from the ["May The Forque Be With You"](https://enki.ws/ganja.js/examples/pga_dyn.html) implementation supplement to [PGAdyn](https://bivector.net/PGADYN.html).

"""

from ipymolstar.molviewspec import DEFAULT_MVS_LOAD_OPTIONS, MolViewSpec
from molviewspec import create_builder, States, GlobalMetadata
from kingdon import Algebra, MultiVector

from functools import reduce
from operator import add


alg = Algebra(3, 0, 1)
globals().update(alg.blades)
bds = alg.blades
# %%


def rsum(values):
    return reduce(add, values)


def dist_pp(P1, P2) -> float:  # point to point
    return (P1.normalized() & P2.normalized()).norm().e


def sort_nn_dist(points: list[MultiVector]) -> list[MultiVector]:
    """Sort points by nearest neighbor."""
    p_list = points.copy()
    current = p_list.pop(0)
    output = [current]
    while p_list:
        next = min(p_list, key=lambda p: dist_pp(current, p))
        output.append(next)
        p_list.remove(next)
        current = next
    return output


def xyz(point: MultiVector) -> tuple:
    """Convert a MultiVector to a tuple."""
    return tuple(point.undual().values()[1:])


class Scene:
    def __init__(self):
        self.builder = create_builder()

    def append(self, mv: MultiVector | list[MultiVector], **kwargs):
        """Append a MultiVector to the scene."""
        # self.builder.append(mv, **kwargs)
        if isinstance(mv, list):
            # all points
            if all(m.grades == (3,) for m in mv):
                if len(mv) == 2:
                    # line
                    points = [tuple(m.undual().values()[1:]) for m in mv]
                    self.line(points[0], points[1], **kwargs)
                if len(mv) == 3:
                    points = [tuple(m.undual().values()[1:]) for m in mv]
                    self.triangle(points, **kwargs)
                if len(mv) == 4:
                    self.quadrilateral(mv, **kwargs)

        elif isinstance(mv, MultiVector):
            # single point
            if mv.grades == (3,):
                coords = tuple(mv.undual().values()[1:])
                self.point(*coords, **kwargs)

    def quadrilateral(self, points: list[MultiVector], color="blue", **kwargs):
        p_sort = sort_nn_dist(points)
        vertices = [c for mv in p_sort for c in xyz(mv)]
        indices = [0, 1, 2, 0, 2, 3, 2, 1, 0, 3, 2, 0]
        self.primitives().mesh(
            vertices=vertices,
            indices=indices,
            triangle_groups=[0],  # All triangles belong to the same group
            color=color,
            **kwargs,
        )

    def primitives(self, **kwargs):
        return self.builder.primitives(**kwargs)

    def axis_arrows(self, opacity=1.0):
        return (
            self.primitives(opacity=opacity)
            .arrow(
                start=(0, 0, 0),
                end=(1, 0, 0),
                color="red",
                tooltip="X",
                show_end_cap=True,
            )
            .arrow(
                start=(0, 0, 0),
                end=(0, 1, 0),
                color="green",
                tooltip="Y",
                show_end_cap=True,
            )
            .arrow(
                start=(0, 0, 0),
                end=(0, 0, 1),
                color="blue",
                tooltip="Z",
                show_end_cap=True,
            )
        )

    def point(self, x, y, z, size=0.1, color="red", **kwargs):
        """Create a point in 3D space."""
        return self.primitives().sphere(
            center=(x, y, z), radius=size, color=color, **kwargs
        )

    def line(self, start: tuple, end: tuple, size=0.02, color="black"):
        return self.primitives().tube(
            start=start,
            end=end,
            color=color,
            radius=size,
        )

    def triangle(self, points: list[tuple], color="blue"):
        """Create a triangle in 3D space."""
        return self.primitives().mesh(
            vertices=[coord for point in points for coord in point],
            indices=[0, 1, 2, 2, 1, 0],
            triangle_groups=[0],
            color=color,
            show_triangles=True,
            show_wireframe=False,
        )

    @property
    def msvj_data(self):
        return self.builder.get_state()


# %%


def RK4(f, y, h):
    k1 = f(*y)
    k2 = f(*[yi + 0.5 * h * k1i for yi, k1i in zip(y, k1)])
    k3 = f(*[yi + 0.5 * h * k2i for yi, k2i in zip(y, k2)])
    k4 = f(*[yi + h * k3i for yi, k3i in zip(y, k3)])
    return [
        yi + (h / 3) * (k2i + k3i + (k1i + k4i) * 0.5)
        for yi, k1i, k2i, k3i, k4i in zip(y, k1, k2, k3, k4)
    ]


# %%

d = 3
size = [0.2, 1, 0.2]
vertexes = [
    alg.vector([1, *[s * (((i >> j) % 2) - 0.5) for j, s in enumerate(size)]]).dual()
    for i in range(2**d)
]

attach_1 = vertexes[5] + alg.blades.e2.dual()
attach_2 = vertexes[1] + alg.blades.e2.dual() + 0.5 * alg.blades.e1.dual()

initial_state = [1 - 0.5 * bds.e02, 38.35 * bds.e13 + 35.27 * bds.e12 - 5 * bds.e01]


faces = [
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (0, 1, 4, 5),
    (2, 3, 6, 7),
    (0, 2, 4, 6),
    (1, 3, 5, 7),
]

face_colors = ["CC00FF", "0400ff", "fbff00", "ffa200", "44ff00", "00aaff"]


mass = 1
I = (
    1
    / 12
    * mass
    * (
        (size[1] ** 2 + size[2] ** 2) * bds.e01
        + (size[2] ** 2 + size[0] ** 2) * bds.e02
        + (size[0] ** 2 + size[1] ** 2) * bds.e03
        + 12 * bds.e12
        + 12 * bds.e13
        + 12 * bds.e23
    )
)

A = lambda B: B.dual().map(lambda k, v: v * getattr(I, alg.bin2canon[k]))
Ai = lambda B: B.map(lambda k, v: v / getattr(I, alg.bin2canon[k])).undual()


@alg.register(symbolic=True)
def forques(M, B):
    Gravity = (~M >> -9.81 * bds.e02).dual()
    Damping = -0.25 * B.grade(2).dual()
    Hooke = -8 * (~M >> attach_1) & vertexes[5]
    Hooke2 = -8 * (~M >> attach_2) & vertexes[1]
    return (Gravity + Hooke + Hooke2 + Damping).grade(
        2
    )  # Ensure a pure bivector because in kingdon<=1.1.0, >> doesn't. Maybe this will change in the future.


# Change in M and B
dState = lambda M, B: [-0.5 * M * B, Ai(forques(M, B) - A(B).cp(B))]

# %%
metadata = GlobalMetadata(
    title="beam_hook_law",
    description="a block dangling from two strings",
    description_format=None,
)
snapshots = []

state = initial_state

for i in range(500):
    scene = Scene()
    upd_vertexes = [state[0] >> point for point in vertexes]

    for c, face in zip(face_colors, faces):
        f_vertices = [upd_vertexes[i] for i in face]
        scene.quadrilateral(f_vertices, color=f"#{c.lower()}")

    scene.point(
        *xyz(attach_1.normalized()), size=0.1, color="green", tooltip="attach_1"
    )
    scene.point(
        *xyz(attach_2.normalized()), size=0.1, color="green", tooltip="attach_2"
    )

    scene.append([attach_1, upd_vertexes[0]], color="black", size=0.02)
    scene.append([attach_2, upd_vertexes[1]], color="black", size=0.02)

    snapshot = scene.builder.get_snapshot(
        title=str(i), linger_duration_ms=2, transition_duration_ms=2
    )
    snapshots.append(snapshot)

    # update the state
    state = RK4(dState, state, 0.01)

states = States(
    snapshots=snapshots,
    metadata=metadata,
).dumps()


# %%
mvs_load_options = {"keepSnapshotCamera": True} | DEFAULT_MVS_LOAD_OPTIONS
view = MolViewSpec(msvj_data=states, mvs_load_options=mvs_load_options)
view


# %%
