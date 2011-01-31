"""
Various utility functions, provided as replacements for their PHP
counterparts from the original XHP code.
"""

def tag2class(tag):
  return 'xhpy_' + tag.replace(':', '__').replace('-', '_')
