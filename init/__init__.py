import __builtin__
from xhpy.hook.XHPyImportHook import xhpy_import_hook
__builtin__.__import__ = xhpy_import_hook
