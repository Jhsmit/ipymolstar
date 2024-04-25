# ipymolstar

![image](https://github.com/Jhsmit/ipymolstar/assets/7881506/589a94d5-2647-4977-90aa-c886c10cacb9)

Try it in jupyter lab on [JupyterLite](https://github.com/Jhsmit/ipymolstar-demo) or play with the solara app example on [ploomber cloud](https://damp-hat-3240.ploomberapp.io/)


## Installation


```sh
pip install ipymolstar
```


## Use

```python
from ipymolstar import PDBeMolstar
view = PDBeMolstar(molecule_id='1qyn', theme='light', hide_water=True)
view
```

Loading local data, hiding the buttons:

```python
from pathlib import Path 
fpth = Path().resolve() / 'assets' / '6vsb.bcif'
custom_data = {
    'data': fpth.read_bytes(),
    'format': 'cif',
    'binary': True,
    }
view = PDBeMolstar(
    custom_data=custom_data, 
    hide_controls_icon=True, 
    hide_expand_icon=True, 
    hide_settings_icon=True, 
    hide_selection_icon=True, 
    hide_animation_icon=True,
    hide_water=True,
    hide_carbs=True,
)
view
```

See the example notebook for more advanced usage. 

## Cite

`ipymolstar` uses `anywidget` to create a widget based on the [PDBe integration](https://github.com/molstar/pdbe-molstar) of [Mol*](https://molstar.org/).

When using `ipymolstar`, please cite:

David Sehnal, Sebastian Bittrich, Mandar Deshpande, Radka Svobodová, Karel Berka, Václav Bazgier, Sameer Velankar, Stephen K Burley, Jaroslav Koča, Alexander S Rose: Mol* Viewer: modern web app for 3D visualization and analysis of large biomolecular structures, Nucleic Acids Research, 2021; [10.1093/nar/gkab31](https://doi.org/10.1093/nar/gkab314).

See also the [RCSB citation policies](https://www.rcsb.org/pages/policies) for additional citation information.

## Development

### Creating a new release

- update `__version__` in `__init__.py`
- create a new release on GitHub, choose as tag 'v' + `__version__`; ie 'v0.0.3'
- GitHub actions should automatically deploy to PyPi

### Hot reloading

To enable anywidget hot reloading, you need to set th env var `ANYWIDGET_HMR` to 1. 

Windows:
```bash
set ANYWIDGET_HMR=1
jupyter lab
```
