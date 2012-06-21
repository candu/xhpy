#!/usr/bin/env python

import os.path
from subprocess import Popen, PIPE
import unittest

class XHPyEndToEndTests(unittest.TestCase):
  def test_bar(self):
    py_path = '{0}/bar.py'.format(os.path.dirname(__file__))
    p = Popen(['python', py_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    self.assertEqual(0, p.returncode)
    self.assertEqual(
      '<div class="baz"><ul><li>0</li><li>1</li><li>2</li></ul></div>\n',
      stdout)

if __name__ == '__main__':
  unittest.main()
