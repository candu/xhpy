'''this is a one-line docstring'''
x = 42
x = 3, 4
False or not True and False or True
this_is_a_variable_name = (1+2*(3-4)//6), False or not True and False or True
a = b
a = test + <div class="test">{{1:2, 3:4}}<a href={link_url}>test {link_title + "test"} test</a>{test < 42}</div>
if a == b:
  '''
  Checks the bars against the bazes.
  '''
  print a   # NOTE: don't remove this, it's essential
  # this inner loop does nothing
  if c == d:
    pass
  c = a

a = <div><a></a></div>

a = test + <div class="test">{{1:2, 3:4}}<a href={link_url}>test {link_title + "test"} test</a>{test < 42}</div>

L = [0,1,2,3]
ul = <ul />
for item in L:
  ul.appendChild(<li>{item}</li>)

class :ui:foo(:ui:base):
  # here are some special XHPy declarations
  category %ui:bar
  attribute string baz, enum {1, 2, 3} goat, bool is-awesome @required, int i = 42
  children :ui:beef, (:ui:thing-one | :ui:thing-two)*

  # here is some Python code
  def render(self):
    a =\
    <div>
      <a href="google.com">test</a>
    </div>
    ul = <ul />
    for item in self.getAttribute('items'):
      ul.appendChild(<li>{item}</li>) 
    return\
    <div>
      {ul}
    </div>
