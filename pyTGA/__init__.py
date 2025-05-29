from pyTGA.pyTGA import *

# Version information
try:
    from importlib.metadata import version
    __version__ = version("pyTGA")
except ImportError:
    __version__ = "unknown"
