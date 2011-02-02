from xhpy.utils import class2element

class XHPyException(Exception):
  @classmethod
  def getElementName(cls, that):
    name = that.__class__.__name__
    if name[:5] != 'xhpy_':
      return name
    return class2element(name)

class XHPyClassException(XHPyException):
  def __init__(self, that, msg):
    super(XHPyException, self).__init__("""\
Exception in class `%s`

%s
""" % (XHPyException.getElementName(that), msg))

class XHPyCoreRenderException(XHPyException):
  def __init__(self, that, rend):
    super(XHPyException, self).__init__("""\
:x:element.render() must reduce an object to an :x:primitive, but `%s` reduced into `%s`
""" % (class2element(that.__class__.__name__), type(rend)))

class XHPyRenderArrayException(XHPyException):
  pass

class XHPyAttributeNotSupportedException(XHPyException):
  def __init__(self, that, attr):
    super(XHPyException, self).__init__("""\
Attribute `%s` is not supported in class `%s`.

Please check for typos in your attribute.
If you are creating a new attribute on this element please add your attribute to the `supportedAttributes` method.
""" % (attr, XHPyException.getElementName(that)))

class XHPyAttributeRequiredException(XHPyException):
  def __init__(self, that, attr):
    super(XHPyException, self).__init__("""\
Required attribute `%s` was not specified in element `%s`.
""" % (attr, XHPyException.getElementName(that)))

class XHPyInvalidAttributeException(XHPyException):
  def __init__(self, that, type, attr, val):
    if isinstance(val, object):
      val_type = val.__class__
    else:
      val_type = type(val)
    super(XHPyException, self).__init__("""\
Invalid attribute `%s` of type `%s` supplied to element `%s`
Expected `%s`
""" % (attr, val_type, XHPyException.getElementName(that), type))

class XHPyInvalidChildrenException(XHPyException):
  def __init__(self, that, index):
    super(XHPyException, self).__init__("""\
Element `%s` was rendered with invalid children.

Verified %s children before failing.

Children expected:
%s

Children received:
%s
""" % (\
    XHPyException.getElementName(that),\
    index,\
    that.renderChildrenDeclaration(),\
    that._children))
