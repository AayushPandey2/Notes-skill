"""Compatibility import; canonical implementation lives in composition."""
import sys
from importlib import import_module
sys.modules[__name__] = import_module(".composition", __package__)
