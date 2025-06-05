# ipymolstar

![image](https://github.com/Jhsmit/ipymolstar/assets/7881506/589a94d5-2647-4977-90aa-c886c10cacb9)


## Live Demos

Give `ipymolstar` a spin without even installing python!


 - Try it in jupyter lab via [JupyterLite](https://github.com/Jhsmit/ipymolstar-demo) 🌍🚀
 - Explore the solara ☀️ [demo application](https://github.com/Jhsmit/ploomber-solara-ipymolstar) on [Ploomber-cloud](https://hidden-resonance-5816.ploomberapp.io) ⛅
 - Grab a cup and play with the [solara](https://app.py.cafe/jhsmit/ipymolstar-solara), [pyshiny](https://py.cafe/jhsmit/ipymolstar-shiny) or [panel](https://app.py.cafe/jhsmit/ipymolstar-panel) live demo's on PyCafé ☕
  - Upload your Alphafold3 .zip result and view plddt or chain colors in the `solarafold` result viewer on [huggingface](https://huggingface.co/spaces/Jhsmit/solarafold) 🤗
 - Control the camera 📷 with [MolViewSpec](https://pypi.org/project/molviewspec/) from python 🐍 in a solara ☀️ dashboard on [PyCafé](https://py.cafe/jhsmit/molviewspec-protein-visualization) ☕
 - Use [MolViewSpec](https://pypi.org/project/molviewspec/) to define primitives 🟦🟢 and animations 🎞️, check out the Double Hooke [3DPGA dynamics](https://enki.ws/ganja.js/examples/pga_dyn.html) example on [PyCafé](https://py.cafe/jhsmit/ipymolstar-kingdon-double-hooke) ☕, adapted from the [kingdon](https://github.com/tBuLi/kingdon) teahouse 🍵;

You can find other examples in the examples directory.

## Preview

You can run a quick preview of `ipymolstar` in a notebook with [juv](https://github.com/manzt/juv):
    
```sh
juv run example.ipynb
```

## Installation

```sh
pip install ipymolstar
```
> [!WARNING]  
> Make sure you install ipymolstar in an environment that contains your installation of Jupyter. If you have installed Jupyter in a different environment from your project (requiring you to use a named, non-default kernel), you will have to install ipymolstar (or only anywidget) in your Jupyter environment as well.


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
Solara example code can be found [here](https://github.com/Jhsmit/ploomber-solara-ipymolstar)

## Citing

`ipymolstar` uses [anywidget](https://github.com/manzt/anywidget) to create a widgets based on [Mol*](https://molstar.org/)

To cite Mol*:
> David Sehnal, Sebastian Bittrich, Mandar Deshpande, Radka Svobodová, Karel Berka, Václav Bazgier, Sameer Velankar, Stephen K Burley, Jaroslav Koča, Alexander S Rose: Mol* Viewer: modern web app for 3D visualization and analysis of large biomolecular structures, Nucleic Acids Research, 2021; [10.1093/nar/gkab31](https://doi.org/10.1093/nar/gkab314).


### PDBeMolstar
The PDBeMolstar widget is based on the [PDBe integration](https://github.com/molstar/pdbe-molstar) of Mol*.


### MolViewSpec

The MolViewSpec widget is based on [MolViewSpec](https://github.com/molstar/mol-view-spec). To cite MolViewSpec:

> Sebastian Bittrich, Adam Midlik, Mihaly Varadi, Sameer Velankar, Stephen K. Burley, Jasmine Y. Young, David Sehnal, Brinda Vallat: Describing and Sharing Molecular Visualizations Using the MolViewSpec Toolkit, Current Protocols, 2024; [10.1002/cpz1.1099](https://doi.org/10.1002/cpz1.1099)

See also the [RCSB citation policies](https://www.rcsb.org/pages/policies) for additional citation information.

## Development


The molviewspec widget front-end code bundles it's JavaScript dependencies. After setting up Python,
make sure to install these dependencies locally:

```sh
npm install
```

While developing, you can run the following in a separate terminal to automatically
rebuild JavaScript as you make changes:

```sh
npm run dev
```


### Creating a new release

- update `__version__` in `__init__.py`
- create a new release on GitHub, choose as tag 'v' + `__version__`; ie 'v0.0.3'
- GitHub actions should automatically deploy to PyPi

### Hot reloading

To enable anywidget hot reloading, you need to set the env var `ANYWIDGET_HMR` to 1. 

Windows:
```bash
set ANYWIDGET_HMR=1
jupyter lab
```
