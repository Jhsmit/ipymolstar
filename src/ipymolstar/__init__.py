from ipymolstar.pdbemolstar import PDBeMolstar

try:
    import molviewspec  # noqa: F401
except ImportError:

    class MolViewSpec:
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "The ipymolstar MolViewSpec requires the molviewspec \n"
                "Python package which may be installed using pip with\n"
                "    pip install molviewspec\n"
                "Afterwards, you will need to restart your Python kernel."
            )

else:
    from ipymolstar.molviewspec import MolViewSpec  # type: ignore

__version__ = "0.1.0"
__all__ = ["MolViewSpec", "PDBeMolstar", "__version__"]
