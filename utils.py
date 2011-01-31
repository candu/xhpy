"""
Various utility functions, provided as replacements for their PHP
counterparts from the original XHP code.
"""

def element2class(element):
  return 'xhpy_' + element.replace(':', '__').replace('-'.'_')

def class2element(klass):
  if klass.startswith('xhpy_'):
    klass = klass[5:]
  return klass.replace('__', ':').replace('_', '-')

def htmlspecialchars(s, ent_quotes=False):
  s = s.replace('&', '&amp;')\
       .replace('"', '&quot;')\
       .replace('<', '&lt;')\
       .replace('>', '&gt;')
  if ent_quotes:
    s = s.replace('\'', '&#039;')
  return s

def get_probably_unique_id():
  import hashlib
  import random
  return hashlib.md5(str(random.randrange(2**31-1))).hexdigest()[:10]
