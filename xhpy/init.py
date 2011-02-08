import compiler
import imp
import marshal
import os.path
import sys
from xhpy.parser import parse

class XHPyImporter(object):

  __xhpy_module_map = {}
  __xhpy_path_cache = {}
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
    if name in self.__xhpy_path_cache:
      return self.__xhpy_path_cache[name]
    tt = name.split('.')
    path = imp.find_module(tt[0])
    for t in tt[1:]:
      path = imp.find_module(t, [path[1]])
    ispkg = path[0] is None
    filename = path[1]
    if ispkg:
      filename += '/__init__.py'
    else:
      path[0].close()
    self.__xhpy_path_cache[name] = (ispkg, filename)
    return self.__xhpy_path_cache[name]

  def _get_code(self, name):
    ispkg, xhpy_name = self._get_path(name)
    pyc_name = xhpy_name + 'c'
    if os.path.isfile(pyc_name) and\
       os.path.getmtime(pyc_name) >= os.path.getmtime(xhpy_name):
      with open(pyc_name, 'rb') as pyc_fp:
        code = marshal.load(pyc_fp)
    else:
      with open(xhpy_name, 'r') as xhpy_fp:
        xhpy_code = xhpy_fp.read()
      py_code = parse(xhpy_code)
      code = compiler.compile(py_code, pyc_name, 'exec')
      with open(pyc_name, 'wb') as pyc_fp:
        marshal.dump(code, pyc_fp)
    mod = sys.modules[name]
    mod.__file__ = pyc_name
    mod.__loader__ = self
    if ispkg:
      mod.__path__ = []
    exec code in mod.__dict__
    return mod

  def load_module(self, name):
    sys.modules[name] = imp.new_module(name)
    return self._get_code(name)

def register_xhpy_module(name):
  XHPyImporter.register_xhpy_module(name)

sys.meta_path.append(XHPyImporter())
register_xhpy_module('xhpy')
