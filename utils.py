"""
Various utility functions for generating DOM element IDs, translating
between XHPy tag/element names and valid Python class names, and escaping
HTML.
"""

def tag2class(tag):
  return 'xhpy_' + tag.replace(':', '__').replace('-', '_')

def element2class(element):
  # strip leading ':' for consistency with tags
  start = element.startswith(':xhpy') and 6 or 1
  return 'xhpy_' + element[start:].replace(':', '__').replace('-', '_')

def class2element(klass):
  return klass[5:].replace('__', ':').replace('_', '-')

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
