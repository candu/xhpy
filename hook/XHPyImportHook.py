import imp
import sys
from xhpy.parser.XHPyParser import parse

# TODO: implement as PEP 302-style hook

def xhpy_load_transformed_module(name, fp, pathname, description):
  mod = imp.new_module(name)
  sys.modules[name] = mod
  # TODO: fill these in
  """
  mod.__file__ = ''
  mod.__path__ = []
  """
  try:
    xhpy_code = fp.read()
    py_code = parse(xhpy_code)
  
    exec py_code in mod.__dict__
    return mod
  except SyntaxError:
    del(sys.modules[name])
    raise ImportError("Syntax error in module %s!" % name)
  except:
    raise

def xhpy_load_module(name, fp, pathname, description):
  if fp is not None:
    return xhpy_load_transformed_module(name, fp, pathname, description)
  return imp.load_module(name, fp, pathname, description)

# Replacement for __import__()
def xhpy_import_hook(name, globals=None, locals=None, fromlist=None):
  parent = determine_parent(globals)
  q, tail = find_head_package(parent, name)
  m = load_tail(q, tail)
  if not fromlist:
    return q
  if hasattr(m, "__path__"):
    ensure_fromlist(m, fromlist)
  return m

def determine_parent(globals):
  if not globals or not globals.has_key("__name__"):
    return None
  pname = globals['__name__']
  if globals.has_key("__path__"):
    parent = sys.modules[pname]
    assert globals is parent.__dict__
    return parent
  if '.' in pname:
    i = pname.rfind('.')
    pname = pname[:i]
    parent = sys.modules[pname]
    assert parent.__name__ == pname
    return parent
  return None

def find_head_package(parent, name):
  try:
    head, tail = name.split('.', 1)
  except ValueError:
    head, tail = name, ''
  if parent:
    qname = "%s.%s" % (parent.__name__, head)
  else:
    qname = head
  q = import_module(head, qname, parent)
  if q: return q, tail
  if parent:
    qname = head
    parent = None
    q = import_module(head, qname, parent)
    if q: return q, tail
  raise ImportError("No module named " + qname)

def load_tail(q, tail):
  m = q
  while tail:
    try:
      head, tail = tail.split('.', 1)
    except ValueError:
      head, tail = tail, ''
    mname = "%s.%s" % (m.__name__, head)
    m = import_module(head, mname, m)
    if not m:
      raise ImportError("No module named " + mname)
  return m

def ensure_fromlist(m, fromlist, recursive=0):
  for sub in fromlist:
    if sub == "*":
      if not recursive:
        try:
          all = m.__all__
        except AttributeError:
          pass
        else:
          ensure_fromlist(m, all, 1)
      continue
    if sub != "*" and not hasattr(m, sub):
      subname = "%s.%s" % (m.__name__, sub)
      submod = import_module(sub, subname, m)
      if not submod:
        raise ImportError("No module named " + subname)

def import_module(partname, fqname, parent):
  try:
    return sys.modules[fqname]
  except KeyError:
    pass
  try:
    fp, pathname, stuff = imp.find_module(partname,
                        parent and parent.__path__)
  except ImportError:
    return None
  try:
    m = xhpy_load_module(fqname, fp, pathname, stuff)
  finally:
    if fp: fp.close()
  if parent:
    setattr(parent, partname, m)
  return m
