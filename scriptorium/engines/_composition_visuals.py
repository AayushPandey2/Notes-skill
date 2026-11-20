"""Compatibility import; canonical implementation lives in composition.visuals."""
import sys
from importlib import import_module
sys.modules[__name__] = import_module(".composition.visuals", __package__)
