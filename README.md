# ipymolstar

![image](https://github.com/Jhsmit/ipymolstar/assets/7881506/589a94d5-2647-4977-90aa-c886c10cacb9)

Try it in jupyter lab on [JupyterLite](https://github.com/Jhsmit/ipymolstar-demo)

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

See the example notebook for more advanced usage. 

## Cite

`ipymolstar` uses `anywidget` to create a widget based on the [PDBe integration](https://github.com/molstar/pdbe-molstar) of [Mol*](https://molstar.org/).

When using `ipymolstar`, please cite:

David Sehnal, Sebastian Bittrich, Mandar Deshpande, Radka Svobodová, Karel Berka, Václav Bazgier, Sameer Velankar, Stephen K Burley, Jaroslav Koča, Alexander S Rose: Mol* Viewer: modern web app for 3D visualization and analysis of large biomolecular structures, Nucleic Acids Research, 2021; [10.1093/nar/gkab31](https://doi.org/10.1093/nar/gkab314).


### Development


Windows:

```bash
set ANYWIDGET_HMR=1
jupyter lab
```
