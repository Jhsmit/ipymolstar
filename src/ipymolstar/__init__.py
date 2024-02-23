import importlib.metadata

try:
    __version__ = importlib.metadata.version("ipymolstar")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

from ipymolstar.widget import PDBeMolstar

__all__ = ["PDBeMolstar"]
