"""
XHPy is XHP for Python, a layer over the base language to permit the use of
XML literals. It also allows you to write your own tags, using
XHTML 1.0 Strict notation to specify allowed attributes and child types; all
validation is performed server-side at compile time, so that it is
_impossible_ to output invalid XHTML.

Using XHPy in your applications is simple: easy_install xhpy, and then just
add

import xhpy

at the top of your main application file.

XHPy works as follows:
- Our __init__.py loads an import hook to intercept calls to the importer.
- When a module without a generated .pyc is imported, we parse it as XHPy.
- XHPy statements are translated to normal Python statements.
- Python generates a normal .pyc, and future module users are none the wiser.

If you're still curious, go read parser/XHPyParser.py; you'll find it's way
more readable than XHP's yacc/lex parser :p
"""
import __builtin__
from xhpy.hook.XHPyImportHook import xhpy_import_hook
__builtin__.__import__ = xhpy_import_hook
