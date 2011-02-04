"""
XHPy parser. We lean on tokenizer to split XHPy input into tokens, then use a
combination of recursive descent and Pratt operator precedence to perform
parsing. For more details, see:

http://effbot.org/zone/simple-top-down-parsing.htm
http://effbot.org/zone/simple-iterator-parser.htm
http://javascript.crockford.com/tdop/tdop.html

The parser then spits out a stream of modified tokens, which is fed to
tokenize.untokenize to produce Python output.
"""

from xhpy.constants import *
from xhpy.utils import tag2class

from cStringIO import StringIO
import tokenize

# TODO: support comment tokens inside xhpy_text (e.g. &#187;)

# parser state
token = None
next = None

# table mapping operators to symbol_base subclasses
symbol_table = {}

# list of keywords, used by xhpy_attribute_name() to ignore operator-ness
keywords = set()

# inside XHPy classes, attribute/category/children become special keywords
in_xhpy_class = []

# for attribute/category/children declarations and XML snippets, we ignore
# newlines.
ignore_whitespace = [False]

# in list comprehensions if clauses, else takes some special handling: note
# [x for x in L if x if f(x) else y] is incorrect syntax;
# [x for x in L if (x if f(x) else y)] is not!
disallow_if_else = [False]

def single_quotify(s):
  return "'%s'" % s.replace('\'', '\\\'')

def advance(id=None):
  global token
  if id and token.id != id:
    raise SyntaxError("Expected %r" % id)
  token = next()

def single_expression(rbp=0):
  global token
  u = token
  yield token.type, token.value
  token = next()
  for t in u.nud():
    yield t
  while rbp < token.lbp:
    u = token
    yield token.type, token.value
    token = next()
    for t in u.led():
      yield t

def expression():
  for t in single_expression():
    yield t
  while token.id == ',':
    yield token.type, token.value
    advance(',')
    for t in single_expression():
      yield t

def expression_ending_in(id):
  for t in single_expression():
    yield t
  while token.id == ',':
    yield token.type, token.value
    advance(',')
    if token.id == id:
      break
    for t in single_expression():
      yield t

def statement():
  if token.std:
    yield token.type, token.value
    u = token
    advance()
    for t in u.std():
      yield t
  else:
    for t in expression():
      yield t
    while token.id == ';':
      yield token.type, token.value
      advance(';')
      for t in expression():
        yield t
    yield token.type, token.value
    advance('(newline)')

def xhpy_enum():
  yield tokenize.OP, '['
  advance('{')
  for t in expression():
    yield t
  while True:
    if token.id != ',':
      break
    yield token.type, token.value
    advance(',')
    for t in expression():
      yield t
  yield tokenize.OP, ']'
  advance('}')

def xhpy_token_normalize():
  if token.id == '(name)' or token.id in keywords:
    yield token.type, token.value
    advance()
  else:
    raise SyntaxError('Expected valid XHPy attribute token')

def xhpy_attribute_name():
  attr_name = []
  for t in xhpy_token_normalize():
    attr_name.append(t[1])
  while True:
    if token.id != '-':
      break
    attr_name.append(token.value)
    advance('-')
    for t in xhpy_token_normalize():
      attr_name.append(t[1])
  yield tokenize.NAME, ''.join(attr_name)

def xhpy_attribute():
  attr_meta_tokens = [(tokenize.NAME, 'None')]
  attr_default_tokens = [(tokenize.NAME, 'None')]
  attr_required_token = (tokenize.NAME, 'False')
  if token.value == 'bool':
    attr_type_token = tokenize.NUMBER, str(TYPE_BOOL)
    attr_default_tokens = [(tokenize.NAME, 'False')]
    advance('(name)')
  elif token.value == 'int':
    attr_type_token = tokenize.NUMBER, str(TYPE_INT)
    attr_default_tokens = [(tokenize.NUMBER, '0')]
    advance('(name)')
  elif token.value == 'float':
    attr_type_token = tokenize.NUMBER, str(TYPE_FLOAT)
    attr_default_tokens = [(tokenize.NUMBER, '0.0')]
    advance('(name)')
  elif token.value == 'list':
    attr_type_token = tokenize.NUMBER, str(TYPE_LIST)
    attr_default_tokens = [(tokenize.OP, '['), (tokenize.OP, ']')]
    advance('(name)')
  elif token.value == 'string':
    attr_type_token = tokenize.NUMBER, str(TYPE_STRING)
    attr_default_tokens = [(tokenize.STRING, single_quotify(''))]
    advance('(name)')
  elif token.value == 'var':
    attr_type_token = tokenize.NUMBER, str(TYPE_VAR)
    advance('(name)')
  elif token.value == 'enum':
    attr_type_token = tokenize.NUMBER, str(TYPE_ENUM)
    advance('(name)')
    attr_meta_tokens = list(xhpy_enum())
  elif token.id == ':':
    attr_type_token = tokenize.NUMBER, str(TYPE_OBJECT)
    advance(':')
    attr_meta_tokens = list(xhpy_tag_name())
  else:
    raise SyntaxError('Expected XHPy attribute type')

  attr_name = ''
  if attr_type_token[1] != str(TYPE_OBJECT):
    _x, attr_name = xhpy_attribute_name().next()

  if token.id == '=':
    advance('=')
    attr_default_tokens = list(expression())
  elif token.id == '@':
    advance('@')
    if token.value != 'required':
      raise SyntaxError('Expected XHPy attribute @required annotation')
    attr_required_token = tokenize.NAME, 'True'
    advance('(name)')

  yield tokenize.STRING, single_quotify(attr_name)
  yield tokenize.OP, ':'
  yield tokenize.OP, '['
  yield attr_type_token
  yield tokenize.OP, ','
  for t in attr_meta_tokens:
    yield t
  yield tokenize.OP, ','
  for t in attr_default_tokens:
    yield t
  yield tokenize.OP, ','
  yield attr_required_token
  yield tokenize.OP, ']'

def xhpy_attribute_decl():
  yield tokenize.NAME, 'def'
  yield tokenize.NAME, '_xhpyAttributeDeclaration'
  yield tokenize.OP, '('
  yield tokenize.NAME, 'self'
  yield tokenize.OP, ')'
  yield tokenize.OP, ':'
  yield tokenize.NAME, 'return'
  yield tokenize.OP, '{'
  for t in xhpy_attribute():
    yield t
  while True:
    if token.id != ',':
      break
    yield token.type, token.value
    advance(',')
    for t in xhpy_attribute():
      yield t
  yield tokenize.OP, '}'

def xhpy_category():
  advance('%')
  tag_type, tag_name = xhpy_tag_name().next()
  yield tokenize.STRING, "'%%%s'" % tag_name

def xhpy_category_decl():
  yield tokenize.NAME, 'def'
  yield tokenize.NAME, '_xhpyCategoryDeclaration'
  yield tokenize.OP, '('
  yield tokenize.NAME, 'self'
  yield tokenize.OP, ')'
  yield tokenize.OP, ':'
  yield tokenize.NAME, 'return'
  yield tokenize.OP, '['
  for t in xhpy_category():
    yield t
  while True:
    if token.id != ',':
      break
    yield token.type, token.value
    advance(',')
    for t in xhpy_category():
      yield t
  yield tokenize.OP, ']'

def xhpy_child_atom():
  if token.value == 'any':
    yield tokenize.OP, '('
    yield tokenize.NUMBER, str(CHILD_ATOM_ANY)
    yield tokenize.OP, ','
    yield tokenize.STRING, '\'any\''
    yield tokenize.OP, ')'
    advance('(name)')
  elif token.value == 'pcdata':
    yield tokenize.OP, '('
    yield tokenize.NUMBER, str(CHILD_ATOM_PCDATA)
    yield tokenize.OP, ','
    yield tokenize.STRING, '\'pcdata\''
    yield tokenize.OP, ')'
    advance('(name)')
  elif token.id == ':':
    advance(':')
    tag_type, tag_name = xhpy_tag_name().next()
    yield tokenize.OP, '('
    yield tokenize.NUMBER, str(CHILD_ATOM_SPECIFIC)
    yield tokenize.OP, ','
    yield tokenize.NAME, tag_name
    yield tokenize.OP, ')'
  elif token.id == '%':
    yield tokenize.OP, '('
    yield tokenize.NUMBER, str(CHILD_ATOM_CATEGORY)
    yield tokenize.OP, ','
    for t in xhpy_category():
      yield t
    yield tokenize.OP, ')'
  elif token.id == '(':
    advance('(')
    for t in xhpy_children_sequence():
      yield t
    advance(')')
  else:
    raise SyntaxError('Expected valid XHPy child')

def xhpy_child_term():
  yield tokenize.OP, '('
  buf = []
  for t in xhpy_child_atom():
    buf.append(t)
  if token.id == '?':
    yield tokenize.NUMBER, str(CHILD_EXPR_ZERO_OR_ONE)
    advance('?')
  elif token.id == '*':
    yield tokenize.NUMBER, str(CHILD_EXPR_ZERO_OR_MORE)
    advance('*')
  elif token.id == '+':
    yield tokenize.NUMBER, str(CHILD_EXPR_ONE_OR_MORE)
    advance('+')
  else:
    yield tokenize.NUMBER, str(CHILD_EXPR_ONE)
  yield tokenize.OP, ','
  for t in buf:
    yield t
  yield tokenize.OP, ')'

def xhpy_child():
  yield tokenize.OP, '('
  yield tokenize.NUMBER, str(CHILD_EXPR_OR)
  yield tokenize.OP, ','
  yield tokenize.OP, '['
  for t in xhpy_child_term():
    yield t
  while True:
    if token.id != '|':
      break
    yield tokenize.OP, ','
    advance('|')
    for t in xhpy_child_term():
      yield t
  yield tokenize.OP, ']'
  yield tokenize.OP, ')'

def xhpy_children_sequence():
  yield tokenize.OP, '('
  yield tokenize.NUMBER, str(CHILD_EXPR_CONCAT)
  yield tokenize.OP, ','
  yield tokenize.OP, '['
  for t in xhpy_child():
    yield t
  while True:
    if token.id != ',':
      break
    yield token.type, token.value
    advance(',')
    for t in xhpy_child():
      yield t
  yield tokenize.OP, ']'
  yield tokenize.OP, ')'

def xhpy_children_decl():
  yield tokenize.NAME, 'def'
  yield tokenize.NAME, '_xhpyChildrenDeclaration'
  yield tokenize.OP, '('
  yield tokenize.NAME, 'self'
  yield tokenize.OP, ')'
  yield tokenize.OP, ':'
  yield tokenize.NAME, 'return'
  if token.value == 'any':
    yield tokenize.OP, '('
    yield tokenize.NUMBER, str(CHILD_DECL_ANY)
    yield tokenize.OP, ','
    yield tokenize.STRING, '\'any\''
    yield tokenize.OP, ')'
    advance('(name)')
  elif token.value == 'empty':
    yield tokenize.OP, '('
    yield tokenize.NUMBER, str(CHILD_DECL_EMPTY)
    yield tokenize.OP, ','
    yield tokenize.STRING, '\'any\''
    yield tokenize.OP, ')'
    advance('(name)')
  else:
    for t in xhpy_children_sequence():
      yield t

def xhpy_block():
  global ignore_whitespace
  yield token.type, token.value
  advance('(newline)')
  yield token.type, token.value
  advance('(indent)')
  while True:
    if token.id == '(dedent)':
      yield token.type, token.value
      advance('(dedent)')
      break
    # don't want to register these in symbol table, since they're not
    # pure Python keywords
    if token.value == 'attribute':
      ignore_whitespace.append(True)
      advance('(name)')
      for t in xhpy_attribute_decl():
        yield t
      yield tokenize.NEWLINE, '\n'
      ignore_whitespace.pop()
    elif token.value == 'category':
      ignore_whitespace.append(True)
      advance('(name)')
      for t in xhpy_category_decl():
        yield t
      yield tokenize.NEWLINE, '\n'
      ignore_whitespace.pop()
    elif token.value == 'children':
      ignore_whitespace.append(True)
      advance('(name)')
      for t in xhpy_children_decl():
        yield t
      yield tokenize.NEWLINE, '\n'
      ignore_whitespace.pop()
    else:
      for t in statement():
        yield t

def block():
  if token.id != '(newline)':
    if token.id in keywords:
      for t in statement():
        yield t
    else:
      for t in expression():
        yield t
      yield token.type, token.value
      advance('(newline)')
    return
  yield token.type, token.value
  advance('(newline)')
  yield token.type, token.value
  advance('(indent)')
  while True:
    if token.id == '(dedent)':
      yield token.type, token.value
      advance('(dedent)')
      break
    for t in statement():
      yield t

class symbol_base(object):
  id = None
  value = None

  def nud(self):
    raise SyntaxError("Syntax error (%r)." % self.id)
  
  def led(self):
    raise SyntaxError("Unknown operator (%r)." % self.id)

  std = None

def method(s):
  assert issubclass(s, symbol_base)
  def bind(fn):
    setattr(s, fn.__name__, fn)
  return bind

def symbol(id, bp=0):
  try:
    s = symbol_table[id]
  except KeyError:
    class s(symbol_base):
      pass
    s.__name__ = 'symbol-' + id
    s.id = id
    s.lbp = bp
    symbol_table[id] = s
    if id.isalpha():
      keywords.add(id)
  else:
    s.lbp = max(bp, s.lbp)
  return s

def infix(id, bp):
  def led(self):
    for t in single_expression(bp):
      yield t
  symbol(id, bp).led = led

def prefix(id, bp):
  def nud(self):
    for t in single_expression(bp):
      yield t
  symbol(id).nud = nud

def infix_r(id, bp):
  def led(self):
    for t in single_expression(bp-1):
      yield t
  symbol(id, bp).led = led

def constant(id):
  @method(symbol(id))
  def nud(self):
    self.id = '(literal)'
    self.value = id
    return []

infix_r("=", 10)
infix_r("+=", 10); infix_r("-=", 10)
infix_r("*=", 10); infix_r("**=", 10)
infix_r("/=", 10); infix_r("%=", 10); infix_r("//=", 10)
infix_r("&=", 10); infix_r("|=", 10); infix_r("^=", 10)
infix_r(">>=", 10); infix_r("<<=", 10)

symbol("if", 20) # ternary form
symbol("lambda", 20)

infix_r("or", 30); infix_r("and", 40); prefix("not", 50)

infix("in", 60); infix("not", 60) # in, not in
infix("is", 60) # is, is not
infix("<", 60); infix("<=", 60)
infix(">", 60); infix(">=", 60)
infix("<>", 60); infix("!=", 60); infix("==", 60)

infix("|", 70); infix("^", 80); infix("&", 90)

infix("<<", 100); infix(">>", 100)

infix("+", 110); infix("-", 110)

infix("*", 120); infix("/", 120); infix("//", 120)
infix("%", 120)

prefix("-", 130); prefix("+", 130); prefix("~", 130)

infix_r("**", 140)

symbol(".", 150); symbol("[", 150); symbol("(", 150)

symbol('(literal)').nud = lambda self: []
symbol('(name)').nud = lambda self: []
symbol('(indent)').nud = lambda self: []
symbol('(dedent)').nud = lambda self: []
symbol('(newline)').nud = lambda self: []
symbol('(end)')

symbol(')')
symbol(']')
symbol('}')
symbol(',')
symbol(':')
symbol(';')
symbol('?')

symbol('print')
symbol('del')
symbol('pass')
symbol('break')
symbol('continue')
symbol('return')
symbol('raise')
symbol('yield')
symbol('from')
symbol('import')
symbol('global')
symbol('exec')
symbol('assert')

symbol('if')
symbol('while')
symbol('for')
symbol('try')
symbol('with')
symbol('def')
symbol('class')
symbol('@')

symbol('elif')
symbol('else')
symbol('except')
symbol('finally')
symbol('as')

constant('None')
constant('True')
constant('False')

# support function list dereference with unary * operation
@method(symbol('*'))
def nud(self):
  for t in single_expression():
    yield t

# support xhpy class names with unary : operation
@method(symbol(':'))
def nud(self):
  yield XHPY_SENTINEL, None
  xhpy_class_name = []
  for t in xhpy_attribute_name():
    xhpy_class_name.append(t[1])
  while True:
    if token.id != ':':
      break
    xhpy_class_name.append(token.value)
    advance(':')
    for t in xhpy_attribute_name():
      xhpy_class_name.append(t[1])
  yield tokenize.NAME, tag2class(''.join(xhpy_class_name))

# support xhpy tags with unary < operation
@method(symbol('<'))
def nud(self, recursive=False):
  # HACK: sentinel value. when parse() gets the list of tokens, it finds these,
  # dropping them along with the preceding '<' token.
  if not recursive:
    yield XHPY_SENTINEL, None
  ignore_whitespace.append(True)
  tag_type, tag_open_name = xhpy_tag_name().next()
  yield tag_type, tag_open_name
  yield tokenize.OP, '(' 
  for t in xhpy_tag_attrs():
    yield t
  if token.id == '/':
    # singleton tag found, close and exit
    yield tokenize.OP, ')'
    ignore_whitespace.pop()
    advance('/')
    advance('>')
    return
  yield tokenize.OP, ','
  yield tokenize.OP, '['
  advance('>')
  while True:
    if token.id == '<':
      advance('<')
      if token.id == '/':
        # close tag found, attempt to match
        advance('/')
        tag_type, tag_close_name = xhpy_tag_name().next()
        if tag_open_name != tag_close_name:
          raise SyntaxError("Expected closing tag </%s>, got </%s>" % (tag_open_name, tag_close_name))
        ignore_whitespace.pop()
        advance('>')
        break
      else:
        # nested open tag found
        for t in symbol('<')().nud(recursive=True):
          yield t
        yield tokenize.OP, ','
    elif token.id == '{':
      # pcdata expression found
      for t in xhpy_expression():
        yield t
      yield tokenize.OP, ','
    else:
      # pcdata text found
      for t in xhpy_text():
        yield t
      yield tokenize.OP, ','
  yield tokenize.OP, ']'
  yield tokenize.OP, ')'
  
def xhpy_tag_name():
  # drop 
  tag_name = list(symbol(':')().nud())[1:]
  yield tokenize.NAME, ''.join([t[1] for t in tag_name])

def xhpy_tag_attrs():
  yield tokenize.OP, '{'
  while True:
    if token.id != '(name)' and token.id not in keywords:
      break
    attr_type, attr_name = xhpy_attribute_name().next()
    yield tokenize.STRING, '\'%s\'' % attr_name
    yield tokenize.OP, ':'
    advance('=')
    if token.id == '{':
      for t in xhpy_expression():
        yield t
    elif token.id == '(literal)':
      yield token.type, token.value
      advance('(literal)')
    else:
      raise SyntaxError('Expected XHPy attribute value')
    yield tokenize.OP, ','
  yield tokenize.OP, '}'

def xhpy_expression():
  advance('{')
  for t in expression():
    yield t
  advance('}')

def get_relpos(p2, p1):
  row = p2[0]-p1[0]+1
  col = p2[1]
  if p2[0] == p1[0]:
    col -= p1[1]
  return (row, col)

def xhpy_text():
  text = []
  for t in grab_until(lambda: token.id in ['{', '<']):
    text.append(t[1])
  yield tokenize.STRING, "%r" % ''.join(text).replace('\'', '\\\'')

@method(symbol('('))
def led(self):
  global ignore_whitespace
  ignore_whitespace.append(True)
  if token.id != ')':
    for t in expression():
      yield t
  if token.id == 'for':
    # generator comprehension
    for t in comprehension_clause():
      yield t
  ignore_whitespace.pop()
  yield token.type, token.value
  advance(')')

@method(symbol('('))
def nud(self):
  global ignore_whitespace
  ignore_whitespace.append(True)
  if token.id != ')':
    for t in expression_ending_in(')'):
      yield t
  if token.id == 'for':
    # generator comprehension
    for t in comprehension_clause():
      yield t
  ignore_whitespace.pop()
  yield token.type, token.value
  advance(')')

@method(symbol('['))
def led(self):
  global ignore_whitespace
  ignore_whitespace.append(True)
  # if [ is followed by (newline), skip it here as it won't be
  # ignored by ignore_whitespace yet
  if token.id == '(newline)':
    advance('(newline)')
  if token.id == '.':
    # ellipsis
    yield token.type, token.value
    advance('.')
    yield token.type, token.value
    advance('.')
    yield token.type, token.value
    advance('.')
  else:
    # slicing or indexing
    if token.id == ':':
      yield token.type, token.value
      advance(':')
      if token.id == ':':
        yield token.type, token.value
        advance(':')
        if token.id != ']':
          # L[::z]
          for t in expression():
            yield t
        # L[::]
      elif token.id != ']':
        for t in expression():
          yield t
        if token.id == ':':
          yield token.type, token.value
          advance(':')
          if token.id != ']':
            # L[:y:z]
            for t in expression():
              yield t
          # L[:y:]
        # L[:y]
      # L[:]
    else: 
      for t in expression():
        yield t
      if token.id == ':':
        yield token.type, token.value
        advance(':')
        if token.id == ':':
          yield token.type, token.value
          advance(':')
          if token.id != ']':
            # L[x::z]
            for t in expression():
              yield t
          # L[x::]
        elif token.id != ']':
          for t in expression():
            yield t
          if token.id == ':':
            yield token.type, token.value
            advance(':')
            if token.id != ']':
              # L[x:y:z]
              for t in expression():
                yield t
            # L[x:y:]
          # L[x:y]
        # L[x:]
      # L[x]
  ignore_whitespace.pop()
  yield token.type, token.value
  advance(']')

def grab_until(p):
  while not p():
    yield token.type, token.value
    advance()

def comprehension_clause():
  disallow_if_else.append(True)
  yield token.type, token.value
  advance('for')
  for t in expression():
    yield t
  while token.id == 'for' or token.id == 'if':
    yield token.type, token.value
    advance(token.id)
    for t in expression():
      yield t
  disallow_if_else.pop()

@method(symbol('['))
def nud(self):
  global ignore_whitespace
  ignore_whitespace.append(True)
  # if [ is followed by (newline), skip it here as it won't be
  # ignored by ignore_whitespace yet
  if token.id == '(newline)':
    advance('(newline)')
  if token.id != ']':
    for t in expression_ending_in(']'):
      yield t
  if token.id == 'for':
    # list comprehension
    for t in comprehension_clause():
      yield t
  ignore_whitespace.pop()
  yield token.type, token.value
  advance(']')

@method(symbol('{'))
def nud(self):
  global ignore_whitespace
  ignore_whitespace.append(True)
  while token.id != '}':
    for t in single_expression():
      yield t
    yield token.type, token.value
    advance(':')
    for t in single_expression():
      yield t
    if token.id != ',':
      break
    yield token.type, token.value
    advance(',')
  yield token.type, token.value
  ignore_whitespace.pop()
  advance('}')

@method(symbol('if'))
def led(self):
  for t in expression():
    yield t
  if disallow_if_else[-1]:
    return
  yield token.type, token.value
  advance('else')
  for t in expression():
    yield t

@method(symbol('.'))
def led(self):
  if token.id != '(name)':
    raise SyntaxError('Expected an attribute name')
  yield token.type, token.value
  advance()

@method(symbol('lambda'))
def nud(self):
  if token.id != ':':
    for t in function_argument():
      yield t
    while token.id == ',':
      yield token.type, token.value
      advance(',')
      for t in function_argument():
        yield t
  yield token.type, token.value
  advance(':')
  for t in expression():
    yield t

@method(symbol('not'))
def led(self):
  if token.id != 'in':
    raise SyntaxError('Invalid syntax')
  yield token.type, token.value
  advance()
  self.id = 'not in'
  for t in single_expression(60):
    yield t

@method(symbol('is'))
def led(self):
  if token.id == 'not':
    yield token.type, token.value
    advance()
    self.id = 'is not'
  for t in single_expression(60):
    yield t

@method(symbol('if'))
def std(self):
  for t in expression():
    yield t
  yield token.type, token.value
  advance(':')
  for t in block():
    yield t
  while True:
    if token.id != 'elif':
      break
    yield token.type, token.value
    advance('elif')
    for t in expression():
      yield t
    yield token.type, token.value
    advance(':')
    for t in block():
      yield t
  if token.id == 'else':
    yield token.type, token.value
    advance('else')
    yield token.type, token.value
    advance(':')
    for t in block():
      yield t

@method(symbol('while'))
def std(self):
  for t in expression():
    yield t
  yield token.type, token.value
  advance(':')
  for t in block():
    yield t
  if token.id == 'else':
    yield token.type, token.value
    advance('else')
    yield token.type, token.value
    advance(':')
    for t in block():
      yield t

@method(symbol('for'))
def std(self):
  for t in expression():
    yield t
  yield token.type, token.value
  advance(':')
  for t in block():
    yield t
  if token.id == 'else':
    yield token.type, token.value
    advance('else')
    yield token.type, token.value
    advance(':')
    for t in block():
      yield t

@method(symbol('try'))
def std(self):
  yield token.type, token.value
  advance(':')
  for t in block():
    yield t
  while True:
    if token.id != 'except':
      break
    yield token.type, token.value
    advance('except')
    for t in expression():
      yield t
    yield token.type, token.value
    advance(':')
    for t in block():
      yield t
  if token.id == 'finally':
    yield token.type, token.value
    advance('finally')
    yield token.type, token.value
    advance(':')
    for t in block():
      yield t
  if token.id == 'else':
    yield token.type, token.value
    advance('else')
    yield token.type, token.value
    advance(':')
    for t in block():
      yield t

@method(symbol('with'))
def std(self):
  for t in expression():
    yield t
  yield token.type, token.value
  advance('as')
  for t in expression():
    yield t
  yield token.type, token.value
  advance(':')
  for t in block():
    yield t

def function_argument():
  if token.id == '*':
    yield token.type, token.value
    advance('*')
    yield token.type, token.value
    advance('(name)')
  elif token.id == '**':
    yield token.type, token.value
    advance('**')
    yield token.type, token.value
    advance('(name)')
  elif token.id == '(name)':
    yield token.type, token.value
    advance('(name)')
    if token.id == '=':
      yield token.type, token.value
      advance('=')
      for t in single_expression():
        yield t
  else:
    raise SyntaxError('Expected an argument name')

@method(symbol('def'))
def std(self):
  global ignore_whitespace
  if token.id != '(name)':
    raise SyntaxError('Expected a function name')
  yield token.type, token.value
  advance('(name)')
  ignore_whitespace.append(True)
  yield token.type, token.value
  advance('(')
  while True:
    if token.id == ')':
      break
    for t in function_argument():
      yield t
    if token.id != ',':
      break
    yield token.type, token.value
    advance(',')
  ignore_whitespace.pop()
  yield token.type, token.value
  advance(')')
  yield token.type, token.value
  advance(':')
  for t in block():
    yield t

@method(symbol('class'))
def std(self):
  global in_xhpy_class
  if token.id == '(name)':
    yield token.type, token.value
    advance('(name)')
    in_xhpy_class.append(False)
  elif token.id == ':':
    advance(':')
    tag_type, tag_name = xhpy_tag_name().next()
    yield tokenize.NAME, tag_name
    in_xhpy_class.append(True)
  if token.id == '(':
    yield token.type, token.value
    advance('(')
    for t in expression_ending_in(')'):
      yield t
    yield token.type, token.value
    advance(')')
  yield token.type, token.value
  advance(':')
  if in_xhpy_class[-1]:
    for t in xhpy_block():
      yield t
  else:
    for t in block():
      yield t
  in_xhpy_class.pop()

def class_name_fragment():
  if token.id == ':':
    advance(':')
    tag_type, tag_name = xhpy_tag_name().next()
    yield tokenize.NAME, tag_name
  elif token.id == '(name)':
    yield token.type, token.value
    advance('(name)')

def class_name():
  for t in class_name_fragment():
    yield t
  while token.id == '.':
    yield token.type, token.value
    advance('.')
    for t in class_name_fragment():
      yield t

@method(symbol('@'))
def std(self):
  if token.id != '(name)':
    raise SyntaxError('Expected a decorator call')
  for t in expression():
    yield t
  yield token.type, token.value
  advance('(newline)')
  while True:
    if token.id != '@':
      break
    yield token.type, token.value
    advance('@')
    for t in expression():
      yield t
    yield token.type, token.value
    advance('(newline)')
  if token.id == 'def':
    u = token
    yield token.type, token.value
    advance('def')
    for t in u.std():
      yield t
  elif token.id == 'class':
    u = token
    yield token.type, token.value
    advance('class')
    for t in u.std():
      yield t
  else:
    raise SyntaxError('Expected a decorated function or class')

@method(symbol('print'))
def std(self):
  if token.id == '>>':
    yield token.type, token.value
    advance('>>')
    for t in single_expression():
      yield t
    yield token.type, token.value
    advance(',')
  while True:
    if token.id == '(newline)':
      break
    for t in single_expression():
      yield t
    if token.id != ',':
      break
    yield token.type, token.value
    advance(',')
  yield token.type, token.value
  advance('(newline)')

@method(symbol('del'))
def std(self):
  for t in expression():
    yield t
  yield token.type, token.value
  advance('(newline)')

@method(symbol('pass'))
def std(self):
  yield token.type, token.value
  advance('(newline)')

@method(symbol('break'))
def std(self):
  yield token.type, token.value
  advance('(newline)')

@method(symbol('continue'))
def std(self):
  yield token.type, token.value
  advance('(newline)')

@method(symbol('return'))
def std(self):
  if token.id != '(newline)':
    for t in expression():
      yield t
  yield token.type, token.value
  advance('(newline)')

@method(symbol('raise'))
def std(self):
  if token.id != '(newline)':
    for t in expression():
      yield t
  if token.id == ',':
    yield token.type, token.value
    advance(',')
    for t in expression():
      yield t
  if token.id == ',':
    yield token.type, token.value
    advance(',')
    for t in expression():
      yield t
  yield token.type, token.value
  advance('(newline)')

@method(symbol('yield'))
def std(self):
  if token.id != '(newline)':
    for t in expression():
      yield t
  yield token.type, token.value
  advance('(newline)')

@method(symbol('from'))
def std(self):
  for t in import_dotted_name():
    yield t
  yield token.type, token.value
  advance('import')
  for t in import_target():
    yield t
  while True:
    if token.id != ',':
      break
    yield token.type, token.value
    advance(',')
    for t in import_target():
      yield t
  yield token.type, token.value
  advance('(newline)')

@method(symbol('import'))
def std(self):
  for t in import_dotted_name():
    yield t
  if token.id == 'as':
    yield token.type, token.value
    advance('as')
    yield token.type, token.value
    advance('(name)')
  while True:
    if token.id != ',':
      break
    yield token.type, token.value
    advance(',')
    for t in import_dotted_name():
      yield t
    if token.id == 'as':
      yield token.type, token.value
      advance('as')
      yield token.type, token.value
      advance('(name)')
  yield token.type, token.value
  advance('(newline)')

def import_target():
  if token.id == '*':
    # import all
    yield token.type, token.value
    advance('*')
  elif token.id == ':':
    # import XHPy name
    advance(':')
    for t in xhpy_tag_name():
      yield t
  elif token.id == '(name)':
    # normal name
    yield token.type, token.value
    advance('(name)')
    if token.id == 'as':
      yield token.type, token.value
      advance('as')
      yield token.type, token.value
      advance('(name)')

def import_dotted_name():
  if token.id != '(name)':
    raise SyntaxError('Expected import dotted name')
  yield token.type, token.value
  advance('(name)')
  while True:
    if token.id != '.':
      break
    yield token.type, token.value
    advance('.')
    yield token.type, token.value
    advance('(name)')

@method(symbol('global'))
def std(self):
  for t in expression():
    yield t
  yield token.type, token.value
  advance('(newline)')

@method(symbol('exec'))
def std(self):
  for t in expression():
    yield t
  yield token.type, token.value
  advance('(newline)')

@method(symbol('assert'))
def std(self):
  for t in expression():
    yield t
  yield token.type, token.value
  advance('(newline)')

def argument_list():
  while True:
    if token.id != '(name)':
      raise SyntaxError('Expected an argument name')
    yield token.type, token.value
    advance()
    if token.id != ',':
      break
    yield token.type, token.value
    advance(',')

def tokenize_python(program):
  type_map = {
    tokenize.NUMBER: '(literal)',
    tokenize.STRING: '(literal)',
    tokenize.INDENT: '(indent)',
    tokenize.DEDENT: '(dedent)',
    tokenize.NL: '(newline)',
    tokenize.NEWLINE: '(newline)',
    tokenize.OP: '(operator)',
    tokenize.ERRORTOKEN: '(operator)',    # probably ?
    tokenize.NAME: '(name)',
    tokenize.ENDMARKER: '(end)'
  }
  for t in tokenize.generate_tokens(StringIO(program).next):
    t_type, t_value, t_start, t_end, t_line = t
    try:
      if t_type == tokenize.COMMENT:
        continue
      yield type_map[t_type], t_value, t_start, t_end, t_type
      if t_type == tokenize.ENDMARKER:
        break
    except KeyError:
      raise SyntaxError("Unexpected token %r" % (t,))

def tokenize_collapse_multiple_strings(program):
  string_token = None
  # string (newline) string => string string, BUT string (newline) (name) is
  # unchanged - so we need to buffer (newline) until we know how to handle it
  string_token_buffer = []
  for t in tokenize_collapse_multiple_newlines(program):
    if t.type == tokenize.STRING:
      if string_token is None:
        symbol = symbol_table['(literal)']
        string_token = symbol()
        string_token.value = ''
        string_token.start = t.start
        string_token.type = t.type
      string_token.value += t.value
      string_token.end = t.end
      string_token_buffer = []
      continue
    elif string_token is not None:
      if t.id in ['(newline)', '(indent)', '(dedent)']:
        string_token_buffer.append(t)
        continue
      else:
        yield string_token
        for u in string_token_buffer:
          yield u
        string_token = None
        string_token_buffer = []
    yield t

def tokenize_collapse_multiple_newlines(program):
  newline_token = None
  for t in tokenize_ignore_whitespace(program):
    # collapse multiple newlines
    if t.id == '(newline)':
      if newline_token is None:
        symbol = symbol_table['(newline)']
        newline_token = symbol()
        newline_token.value = t.value
        newline_token.start = t.start
        newline_token.type = t.type
      newline_token.end = t.end
      continue
    elif newline_token is not None:
      yield newline_token
      newline_token = None
      # fall through to allow output of next token
    yield t

def tokenize_ignore_whitespace(program):
  for t in tokenize_xhpy(program):
    if ignore_whitespace[-1] and t.id in ['(newline)', '(indent)', '(dedent)']:
      continue
    yield t

def tokenize_xhpy(program):
  for id, value, start, end, type in tokenize_python(program):
    if id == '(name)':
      # note tokenize reads 'if', 'else', etc. as names
      symbol = symbol_table.get(value)
      if symbol:
        s = symbol()
      else:
        symbol = symbol_table[id]
        s = symbol()
    elif id == '(operator)':
      symbol = symbol_table.get(value)
      if not symbol:
        raise SyntaxError("Unknown operator (%r)" % id)
      s = symbol()
    else:
      symbol = symbol_table[id]
      s = symbol()
    s.value = value
    s.start = start
    s.end = end
    s.type = type
    yield s

def rewrite(program, debug=False):
  global token, next
  if debug:
    next_debug_helper = tokenize_collapse_multiple_strings(program).next
    def next_debug():
      token = next_debug_helper()
      print token.id, token.value, token.start, token.end
      return token
    next = next_debug
  else:
    next = tokenize_collapse_multiple_strings(program).next
  token = next()
  # ignore leading whitespace, if any
  if token.id == '(newline)':
    advance('(newline)')
  while token.id != '(end)':
    for t in statement():
      yield t

def parse(program, debug=False):
  tokens = []
  for t in rewrite(program, debug):
    if t[0] == XHPY_SENTINEL:
      tokens.pop()
    else:
      tokens.append(t)
  return tokenize.untokenize(tokens)

if __name__ == '__main__':
  import sys
  debug = len(sys.argv) > 1 and sys.argv[1] == '-d'
  print parse(sys.stdin.read(), debug)
