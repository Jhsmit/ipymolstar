import solara
from ipymolstar import PDBeMolstar
import random


molecule_id = solara.reactive("1qyn")
count = solara.reactive(0)
spin = solara.reactive(False)

spin_cb = solara.reactive(False)
theme = solara.reactive("light")


def make_molstar():
    print("make molstar")
    c = PDBeMolstar(molecule_id=molecule_id.value, theme=theme.value)
    return c


def rand_rgb() -> dict[str, int]:
    """returns a random rgb color dict"""
    return {
        "r": random.randint(0, 255),
        "g": random.randint(0, 255),
        "b": random.randint(0, 255),
    }


def gen_color_data():
    data = []
    for chain in "ABCD":
        d = {
            "start_residue_number": 0,
            "end_residue_number": 200,
            "struct_asym_id": chain,
            "color": rand_rgb(),
            "focus": False,
        }
        data.append(d)

    return data


@solara.component
def Page():
    c = solara.use_memo(make_molstar, dependencies=[molecule_id.value, theme.value])

    def set_spin(value):
        # doesnt work, triggers rerender instead of setting spin
        print("value", value)
        spin.set(value)

        c.spin = not c.spin

    def set_spin_cb(value):
        # same issue as switch
        print("cb setter", value)
        spin_cb.set(value)
        c.spin = value

    def set_true(*event):
        # works
        c.spin = True

    def set_false(*event):
        # works
        print("event", event)
        c.spin = False

    def do_color():
        # works
        data = gen_color_data()
        c.color(data, non_selected_color={"r": 0, "g": 87, "b": 0})

    def toggle_water():
        # works
        c.hide_water = not c.hide_water

    def toggle_spin():
        c.spin = not c.spin

    with solara.Card(style="width: 500px; height: 750px;"):
        solara.InputText(
            label="molecule id", value=molecule_id.value, on_value=molecule_id.set
        )
        solara.display(c)
        solara.Button(label="increment", on_click=lambda: count.set(count.value + 1))
        solara.Button(label="set true", on_click=set_true)
        solara.Button(label="set false", on_click=set_false)
        solara.Button(label="randcolor", on_click=do_color)
        solara.Button(label="toggle water", on_click=toggle_water)
        solara.Button(label="toggle spin", on_click=toggle_spin)
        solara.Switch(label="spin", value=spin.value, on_value=set_spin)
        solara.Checkbox(label="spin_cb", value=spin_cb.value, on_value=set_spin_cb)
        solara.Select(
            label="set theme",
            value=theme.value,
            on_value=theme.set,
            values=["light", "dark"],
        )
        solara.Text(
            f"molecule_id: {molecule_id.value}, count: {count.value}, spin: {spin.value}, {c.spin}"
        )
        solara.Text(f"hide_water: {c.hide_water}")


# @solara.component
# def Page():
#     # molecule_id, set_molecule_id = solara.use_state("1qyn")

#     with solara.Card(style="width: 500px; height: 750px;"):
#         solara.InputText(
#             label="molecule id", value=molecule_id.value, on_value=molecule_id.set
#         )
#         # c = PDBeMolstar.element(molecule_id=molecule_id.value)
#         c = PDBeMolstar(molecule_id=molecule_id.value)
#         solara.display(c)

#         solara.Text(f"molecule_id: {molecule_id.value}")
