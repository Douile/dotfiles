# -*- coding:utf-8 -*-

import sys
import importlib
import traceback

from libqtile.log_utils import logger
from libqtile.widget.import_error import make_error

def import_class(module_path, class_name, fallback=None):
    """Import a class safely
    Try to import the class module, and if it fails because of an ImporError
    it logs on WARNING, and logs the traceback on DEBUG level
    """
    try:
        module = importlib.import_module(module_path, __package__)
        return getattr(module, class_name)
    except ImportError as error:
        logger.warning("Unmet dependencies for '%s.%s': %s", module_path,
                       class_name, error)
        if fallback:
            logger.debug("%s", traceback.format_exc())
            return fallback(module_path, class_name, error)
        raise

def safe_import_(module_names, class_name, globals_, fallback=None):
    """Import a class into given globals, lazily and safely
    The globals are filled with a proxy function so that the module is imported
    only if the class is being instanciated.
    An exception is made when the documentation is being built with Sphinx, in
    which case the class is eagerly imported, for inspection.
    """
    module_path = '.'.join(module_names)
    if type(class_name) is list:
        for name in class_name:
            safe_import(module_names, name, globals_)
        return

    def class_proxy(*args, **kwargs):
        cls = import_class(module_path, class_name, fallback)
        return cls(*args, **kwargs)

    if "sphinx" in sys.modules:
        globals_[class_name] = import_class(module_path, class_name, fallback)
    else:
        globals_[class_name] = class_proxy

def safe_import(module_name, class_name):
    safe_import_(
        ("", module_name), class_name, globals(), fallback=make_error
    )

safe_import("cpu", "CPU")
safe_import("hwmon", "ThermalHwmon")
safe_import("net", "CustomNet")
