import compiler
import imp
import marshal
import sys
from xhpy.parser import parse

class XHPyImporter(object):

  __xhpy_module_map = {}
  __xhpy_leaf = '__leaf'
  
  @classmethod
  def register_xhpy_module(cls, name):
    """
    Registers the given module and all its submodules as containing XHPy,
    so that they are passed through the XHPy preprocessor when imported.
    """
    cur = cls.__xhpy_module_map
    for t in name.split('.'):
      cur = cur.setdefault(t, {})
    cur[cls.__xhpy_leaf] = True

  @classmethod
  def is_xhpy_module(cls, name):
    cur = cls.__xhpy_module_map
    for t in name.split('.'):
      if t not in cur:
        return cls.__xhpy_leaf in cur
      cur = cur[t]
    return cls.__xhpy_leaf in cur

  def find_module(self, name, path=None):
    if not self.is_xhpy_module(name):
      return
    if name in sys.modules:
      return
    try:
      path = self._get_path(name)
      return self
    except ImportError:
      return

  def _get_path(self, name):
    tt = name.split('.')
    path = imp.find_module(tt[0])
    for t in tt[1:]:
      path = imp.find_module(t, [path[1]])
    return path[:2]

  def _get_code(self, name):
    xhpy_fp, xhpy_name = self._get_path(name)
    ispkg = xhpy_fp is None
    if ispkg:
      xhpy_name += '/__init__.py'
      xhpy_fp = open(xhpy_name)
    xhpy_code = xhpy_fp.read()
    xhpy_fp.close()
    py_code = parse(xhpy_code)
    return ispkg, xhpy_name, py_code

  def load_module(self, name):
    mod = imp.new_module(name)
    sys.modules[name] = mod
    ispkg, filename, code = self._get_code(name)
    filename += 'c'
    c = compiler.compile(code, filename, 'exec')
    f = open(filename, 'wb')
    marshal.dump(c, f)
    f.close()
    mod = sys.modules.setdefault(name, imp.new_module(name))
    mod.__file__ = filename
    mod.__loader__ = self
    if ispkg:
      mod.__path__ = []
    exec code in mod.__dict__
    return mod

def register_xhpy_module(name):
  XHPyImporter.register_xhpy_module(name)

sys.meta_path.append(XHPyImporter())
register_xhpy_module('xhpy')
