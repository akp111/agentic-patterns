from .tools_registry import ToolsRegistry, register_tool
from .tools_base import ToolsBase
import importlib
import pkgutil
import os

__all__ = ["ToolsRegistry", "ToolsBase", "register_tool"]


def import_submodules():
    package_dir = os.path.dirname(__file__)
    for _, module_name, is_pkg in pkgutil.iter_modules([package_dir]):
        if module_name not in ['tools_registry', 'tools_base', '__pycache__']:
            importlib.import_module(f"{__name__}.{module_name}")

import_submodules()