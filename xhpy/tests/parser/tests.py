#!/usr/bin/env python

import os.path
from subprocess import Popen, PIPE
import unittest

class XHPyParserTests(unittest.TestCase):
  pass

# We dynamically generate tests based on the files in this directory.
for filename in os.listdir(os.path.dirname(__file__)):
  if not filename.endswith('.py') or filename in ['__init__.py', 'tests.py']:
    continue
  def _test(filename):
    def _test_helper(self):
      parser_path = '{0}/../../parser.py'.format(os.path.dirname(__file__))
      p = Popen(['python', parser_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
      py_path = '{0}/{1}'.format(os.path.dirname(__file__), filename)
      with open(py_path) as f:
        stdout, stderr = p.communicate(input=f.read())
      if filename.startswith('fail_'):
        self.assertNotEqual(0, p.returncode)
      else:
        self.assertEqual(0, p.returncode)
    return _test_helper
  testname = filename[:-3]
  setattr(XHPyParserTests, 'test_{0}'.format(testname), _test(filename))

if __name__ == '__main__':
  unittest.main()
