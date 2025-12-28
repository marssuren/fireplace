import pkg_resources

__author__ = "Jerome Leclanche"
__email__ = "jerome@leclan.ch"

try:
    __version__ = pkg_resources.require("fireplace")[0].version
except Exception:
    __version__ = "dev"
