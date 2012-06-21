#!/usr/bin/env python

import os.path
from subprocess import check_call, Popen, PIPE
import unittest

class XHPyPrecompiledTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    setup_path = '{0}/setup_tests'.format(os.path.dirname(__file__))
    check_call(setup_path)

  @classmethod
  def tearDownClass(cls):
    print
    print 'Removing generated files:'
    cleanup_path = '{0}/cleanup_tests'.format(os.path.dirname(__file__))
    check_call(cleanup_path)


# We dynamically generate tests based on the files in this directory.
for filename in os.listdir(os.path.dirname(__file__)):
  if not filename.endswith('.py') or filename in ['__init__.py', 'tests.py']:
    continue
  def _test(filename):
    def _test_helper(self):
      py_path = '{0}/{1}'.format(os.path.dirname(__file__), filename)
      p = Popen(['python', py_path])
      p.communicate()
      if filename.startswith('fail_'):
        self.assertNotEqual(0, p.returncode)
      else:
        self.assertEqual(0, p.returncode)
    return _test_helper
  testname = filename[:-3]
  setattr(XHPyPrecompiledTests, 'test_{0}'.format(testname), _test(filename))

if __name__ == '__main__':
  unittest.main()
