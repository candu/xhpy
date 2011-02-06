from xhpy.constants import *
from  xhpy.utils import htmlspecialchars, element2class

from exception import *

# TODO: <img /> singletons fail validation, but should pass

ENABLE_VALIDATION = True

class XHPyStrictValidator(object):
  def __init__(self):
    # used to track state during child spec validation
    self.ii = None

  def _safe(self, cast, val):
    try:
      return cast(val)
    except (ValueError, TypeError):
      raise XHPyInvalidAttributeException(element, decl[attr][1], attr, val)

  def validateAttributeValue(self, element, attr, val):
    if val is None:
      return None

    that = element
    decl = that._xhpyAttributeDeclaration()
    while attr not in decl:
      if not isinstance(that, :x:base):
        raise XHPyAttributeNotSupportedException(element, attr)
      that = super(type(that), that)
      decl = that._xhpyAttributeDeclaration()
    attr_type = decl[attr][0]
    if attr_type == TYPE_STRING:
      return self._safe(str, val)
    if attr_type == TYPE_BOOL:
      return self._safe(bool, val)
    if attr_type == TYPE_INT:
      return self._safe(int, val)
    if attr_type == TYPE_FLOAT:
      return self._safe(float, val)
    if attr_type == TYPE_LIST:
      return self._safe(list, val)
    if attr_type == TYPE_OBJECT:
      if not isinstance(val, decl[attr][1]):
        raise XHPyInvalidAttributeException(element, decl[attr][1], attr, val)
      return val
    if attr_type == TYPE_VAR:
      return val
    if attr_type == TYPE_ENUM:
      for enum in decl[attr][1]:
        if enum == val:
          return val
      enums = 'enum("' + '","'.join(decl[attr][1]) + '")'
      raise XHPyInvalidAttributeException(element, enums, attr, val)

  def validateChildren(self, element):
    decl = element._xhpyChildrenDeclaration()
    if decl == CHILD_DECL_ANY:
      # any children allowed
      return
    if decl == CHILD_DECL_EMPTY:
      # no children allowed
      if element._children:
        raise XHPyInvalidChildrenException(element, 0)
      return
    self.ii = 0
    if not self.validateChildrenExpression(element, decl) or\
      self.ii < len(element._children):
      raise XHPyInvalidChildrenException(element, self.ii)

  def validateChildrenExpression(self, element, decl):
    n = len(element._children)
    if decl[0] == CHILD_ATOM_ANY:
      # any element -- any
      if self.ii < n:
        self.ii += 1
        return True
      return False
    if decl[0] == CHILD_ATOM_PCDATA:
      # pcdata -- any non-element data
      if self.ii < n and not isinstance(element._children[self.ii], :x:base):
        self.ii += 1
        return True
      return False
    if decl[0] == CHILD_ATOM_SPECIFIC:
      # specific element -- :fb-thing
      if self.ii < n and isinstance(element._children[self.ii], decl[1]):
        self.ii += 1
        return True
      return False
    if decl[0] == CHILD_ATOM_CATEGORY:
      # element category -- %block
      if self.ii < n and\
          isinstance(element._children[self.ii], :x:base) and\
          element._children[self.ii].categoryOf(decl[1]):
        self.ii += 1
        return True
      return False
    if decl[0] == CHILD_EXPR_ONE:
      # exactly once -- :thing
      return self.validateChildrenExpression(element, decl[1])
    if decl[0] == CHILD_EXPR_ZERO_OR_MORE:
      # zero or more times -- :thing*
      while self.validateChildrenExpression(element, decl[1]):
        pass
      return True
    if decl[0] == CHILD_EXPR_ZERO_OR_ONE:
      # zero or one times -- :thing?
      if self.validateChildrenExpression(element, decl[1]):
        pass
      return True
    if decl[0] == CHILD_EXPR_ONE_OR_MORE:
      # one or more times -- :thing+
      if not self.validateChildrenExpression(element, decl[1]):
        return False
      while self.validateChildrenExpression(element, decl[1]):
        pass
      return True
    if decl[0] == CHILD_EXPR_CONCAT:
      # specific order -- :thing, :other-thing, ...
      oindex = self.ii
      for d in decl[1]:
        if not self.validateChildrenExpression(element, d):
          self.ii = oindex
          return False
      return True
    if decl[0] == CHILD_EXPR_OR:
      # either-or -- :thing | :other-thing | ...
      for d in decl[1]:
        if self.validateChildrenExpression(element, d):
          return True
      return False

class :x:base(object):
  """
  A validator for XHPy attribute and child declarations.
  """
  _validator = XHPyStrictValidator()

  """
  Defined in elements by the `attribute` keyword. The declaration is simple.
  There is a keyed array, with each key being an attribute. Each value is
  an array with 4 elements. The first is the attribute type. The second is
  meta-data about the attribute. The third is a default value (null for
  none). And the fourth is whether or not this value is required.
  Attribute types are suggested by the TYPE_* constants.
  """
  def _xhpyAttributeDeclaration(self):
    return {}

  """
  Defined in elements by the `category` keyword. This is just a list of all
  categories an element belongs to. Each category is a key with value 1.
  """
  def _xhpyCategoryDeclaration(self):
    return []

  """
  Defined in elements by the `children` keyword. This returns a pattern of
  allowed children. The return value is potentially very complicated. The
  two simplest are 0 and 1 which mean no children and any children,
  respectively. Otherwise you're dealing with an array which is just the
  biggest mess you've ever seen.
  """
  def _xhpyChildrenDeclaration(self):
    return CHILD_DECL_ANY

  def renderChildrenDeclaration(self):
    """
    Render the children declaration in readable format. Used in exception
    output.
    """
    decl = self._xhpyChildrenDeclaration()
    if decl == CHILD_DECL_ANY:
      return 'any'
    if decl == CHILD_DECL_EMPTY:
      return 'empty'
    def _helper(decl):
      if decl[0] == CHILD_ATOM_ANY:
        return 'any'
      if decl[0] == CHILD_ATOM_PCDATA:
        return 'pcdata'
      if decl[0] == CHILD_ATOM_CATEGORY:
        return decl[1]
      if decl[0] == CHILD_ATOM_SPECIFIC:
        return decl[1].__name__
      if decl[0] == CHILD_EXPR_ONE:
        return _helper(decl[1])
      if decl[0] == CHILD_EXPR_ZERO_OR_ONE:
        return "%s?" % _helper(decl[1])
      if decl[0] == CHILD_EXPR_ZERO_OR_MORE:
        return "%s*" % _helper(decl[1])
      if decl[0] == CHILD_EXPR_ONE_OR_MORE:
        return "%s+" % _helper(decl[1])
      if decl[0] == CHILD_EXPR_CONCAT:
        return ','.join([_helper(d) for d in decl[1]])
      if decl[0] == CHILD_EXPR_OR:
        return '|'.join([_helper(d) for d in decl[1]])
    return _helper(decl)
  
  def __init__(self):
    raise NotImplementedError('not implemented!')

  def __str__(self):
    raise NotImplementedError('not implemented!')

  def appendChild(self, child):
    raise NotImplementedError('not implemented!')

  def getAttribute(self, attr):
    raise NotImplementedError('not implemented!')

  def setAttribute(self, attr, val):
    raise NotImplementedError('not implemented!')

  def categoryOf(self, cat):
    raise NotImplementedError('not implemented!')

  @classmethod
  def renderChild(cls, child):
    if isinstance(child, :x:base):
      return str(child)
    if isinstance(child, list):
      raise XHPyRenderListException('Can not render list!')
    return htmlspecialchars(str(child))

class :x:composable-element(:x:base):
  def _init(self):
    pass

  def __init__(self, attributes={}, children=[], source=None):
    self.source = source
    if attributes and ENABLE_VALIDATION:
      for key in attributes:
        attributes[key] =\
          self._validator.validateAttributeValue(self, key, attributes[key])
    self._attributes = attributes
    self._children = []
    for child in children:
      self.appendChild(child)

  def appendChild(self, child):
    """
    Adds a child to the end of this node. If you give an array to this method
    then it will behave like a DocumentFragment.
    """
    if isinstance(child, list):
      for c in child:
        self.appendChild(c)
    elif isinstance(child, :x:frag):
      self._children += child._children
    elif child is not None:
      self._children.append(child)
    return self

  def getChildren(self, tag_name=None):
    """
    Fetches all direct children of this element that match a particular tag
    name (or all children if no tag is given)
    """
    if not tag_name:
      return self._children
    tag_name = element2class(tag_name)
    tag_class = globals()[tag_name]
    return [child for child in self._children if isinstance(child, tag_class)]

  def getAttribute(self, attr):
    """
    Fetches an attribute from this elements attribute store. If attr is not
    defined in the store, and default is null an exception will be thrown.
    """
    if attr in self._attributes:
      return self._attributes[attr]
    decl = self._xhpyAttributeDeclaration()
    if attr not in decl:
      raise XHPyAttributeNotSupportedException(self, attr)
    elif decl[attr][3]:
      raise XHPyAttributeRequiredException(self, attr)
    else:
      return decl[attr][2]

  def getAttributes(self):
    return self._attributes

  def setAttribute(self, attr, val):
    """
    Sets an attribute in this element's attribute store.
    """
    if ENABLE_VALIDATION:
      val = self._validator.validateAttributeValue(self, attr, val)
    self._attributes[attr] = val
    return self

  def _flushElementChildren(self):
    ln = len(self._children)
    for ii in xrange(ln):
      child = self._children[ii]
      if isinstance(child, :x:element):
        while isinstance(child, :x:element):
          if ENABLE_VALIDATION:
            self._validator.validateChildren(child)
          child = child.render()
        if not isinstance(child, :x:primitive):
          raise XHPyCoreRenderException(self._children[ii], child)
        if isinstance(child, :x:frag):
          self._children = self._children[:ii] + child._children +\
            self._children[ii+1:]
          ln = len(self._children)
          ii -= 1
        else:
          self._children[ii] = child

  def categoryOf(self, c):
    return c in self._xhpyCategoryDeclaration()

class :x:primitive(:x:composable-element):
  """
  :x:primitive lays down the foundation for very low-level elements. You
  should directly :x:primitive only if you are creating a core element that
  needs to directly implement stringify(). All other elements should subclass
  from :x:element.
  """

  def stringify(self):
    pass
  
  def __str__(self):
    self._flushElementChildren()
    if ENABLE_VALIDATION:
      self._validator.validateChildren(self)
    return self.stringify()

class :x:element(:x:composable-element):
  """
  :x:element defines an interface that all user-land elements should subclass
  from. The main difference between :x:element and :x:primitive is that
  subclasses of :x:element should implement `render()` instead of `stringify`.
  This is important because most elements should not be dealing with strings
  of markup.
  """

  def __str__(self):
    that = self
    if ENABLE_VALIDATION:
      self._validator.validateChildren(that)
      that = that.render()
      while isinstance(that, :x:element):
        self._validator.validateChildren(that)
        that = that.render()
      if not isinstance(that, :x:composable-element):
        raise XHPyCoreRenderException(self, that)
    else:
      that = that.render()
      while isinstance(that, :x:element):
        that = that.render()
    return str(that)

class :x:frag(:x:primitive):
  """
  An <x:frag /> is a transparent wrapper around any number of elements. When
  you render it just the children will be rendered. When you append it to an
  element the <x:frag /> will disappear and each child will be sequentially
  appended to the element.
  """
  def stringify(self):
    buf = ''
    for child in self.getChildren():
      buf += :x:base.renderChild(child)
    return buf
