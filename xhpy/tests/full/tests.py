#!/usr/bin/env python

from xhpy.init import register_xhpy_module

import unittest

# HACK: for Python < 2.7, monkey-patch unittest to include a stub
# implementation of unittest.skip().
try:
    unittest.skip
except AttributeError:
    def _unittest_skip(msg):
        def wrap(func):
            def wrapped_func(*args):
                pass
            return wrapped_func
        return wrap
    unittest.skip = _unittest_skip

class XHPyFullTests(unittest.TestCase):
  def test_array_constant(self):
    register_xhpy_module('array_constant')
    import array_constant
    self.assertEqual('pass', array_constant.result)

  def test_attr_blank(self):
    register_xhpy_module('attr_blank')
    import attr_blank
    self.assertEqual('pass', attr_blank.result)

  def test_attr_entity(self):
    register_xhpy_module('attr_entity')
    import attr_entity
    self.assertEqual('pass', attr_entity.result)

  def test_attr_float(self):
    register_xhpy_module('attr_float')
    import attr_float
    self.assertEqual('pass', attr_float.result)

  def test_attributes(self):
    register_xhpy_module('attributes')
    import attributes
    self.assertEqual('pass', attributes.result)

  def test_attributes(self):
    register_xhpy_module('attributes')
    import attributes
    self.assertEqual('pass', attributes.result)

  def test_class_constants(self):
    register_xhpy_module('class_constants')
    import class_constants
    self.assertEqual({'etc': 1, 'bar': 2}, class_constants.result)

  def test_docstrings_01(self):
    register_xhpy_module('docstrings_01')
    import docstrings_01
    self.assertEqual('b', docstrings_01.result)

  def test_docstrings_02(self):
    register_xhpy_module('docstrings_02')
    import docstrings_02
    self.assertEqual('b', docstrings_02.result)

  def test_docstrings_03(self):
    register_xhpy_module('docstrings_03')
    import docstrings_03
    self.assertEqual('c', docstrings_03.result)

  def test_docstrings_05(self):
    register_xhpy_module('docstrings_05')
    import docstrings_05
    self.assertEqual('b', docstrings_05.result)

  def test_klass(self):
    register_xhpy_module('klass')
    import klass
    self.assertEqual('pass', klass.result)

  @unittest.skip('TODO: match input source lines on output')
  def test_lineno_01(self):
    register_xhpy_module('lineno_01')
    import lineno_01
    self.assertEqual(7, lineno_01.result[1])

  @unittest.skip('TODO: add support for comment tokens within tags')
  def test_lineno_02(self):
    register_xhpy_module('lineno_02')
    import lineno_02
    self.assertEqual(7, lineno_02.result[1])

  def test_logical_op(self):
    register_xhpy_module('logical_op')
    import logical_op
    self.assertEqual(True, logical_op.result)

  def test_pep0263_01(self):
    register_xhpy_module('pep0263_01')
    import pep0263_01
    self.assertEqual(u'<p>Andr\xe9</p>', unicode(pep0263_01.result))

  def test_pep0263_02(self):
    register_xhpy_module('pep0263_02')
    import pep0263_02
    self.assertEqual(u'<p>Andr\xe9</p>', unicode(pep0263_02.result))

  def test_pep0263_03(self):
    register_xhpy_module('pep0263_03')
    import pep0263_03
    self.assertEqual(u'<p>Andr\xe9</p>', unicode(pep0263_03.result))

  def test_stack_balance_fail(self):
    register_xhpy_module('stack_balance_fail')
    import stack_balance_fail
    self.assertEqual('pass', stack_balance_fail.result)

  def test_whitespace_01(self):
    register_xhpy_module('whitespace_01')
    import whitespace_01
    self.assertEqual(u'<a><a></a>+</a>', unicode(whitespace_01.result))

  def test_whitespace_02(self):
    register_xhpy_module('whitespace_02')
    import whitespace_02
    self.assertEqual(u'<a>a<a></a></a>', unicode(whitespace_02.result))

  def test_whitespace_03(self):
    register_xhpy_module('whitespace_03')
    import whitespace_03
    self.assertEqual(u'<a>a</a>', unicode(whitespace_03.result))

  def test_whitespace_04(self):
    register_xhpy_module('whitespace_04')
    import whitespace_04
    self.assertEqual(u'<a><a></a>a</a>', unicode(whitespace_04.result))

  def test_whitespace_05(self):
    register_xhpy_module('whitespace_05')
    import whitespace_05
    self.assertEqual(u'<a>foo</a>', unicode(whitespace_05.result))

  def test_whitespace_06(self):
    register_xhpy_module('whitespace_06')
    import whitespace_06
    self.assertEqual(u'<a>abc</a>', unicode(whitespace_06.result))

  def test_whitespace_07(self):
    register_xhpy_module('whitespace_07')
    import whitespace_07
    self.assertEqual(u'<a>abc</a>', unicode(whitespace_07.result))

  def test_xhpy_function_param(self):
    register_xhpy_module('xhpy_function_param')
    import xhpy_function_param
    self.assertEqual('pass', xhpy_function_param.result)

if __name__ == '__main__':
  unittest.main()
