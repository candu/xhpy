from foo import bar, baz, :ui:thing

class :ui:foo(:ui:base):
  # here are some special XHPy declarations
  category %ui:bar, %ui:frob
  attribute
    # this is how these attribute declarations usually look
    string baz,
    # how many goats?
    enum {1, 2, 3} goat,
    # some required and default annotations
    bool is-awesome @required, int i = 42
  children :ui:beef, (:ui:thing-one | :ui:thing-two)*, (:dt+, :dd+)*, %block, pcdata, any
  
  # here is some Python code
  def render(self):
    :x:base.renderChild()
    a =\
    <div>
      <a href="google.com">test</a>
    </div>
    ul = <ul />
    for item in self.getAttribute('items'):
      ul.appendChild(<li>{item}</li>) 
    b = <ui:thing>stuff</ui:thing>
    return\
    <div>
      {ul}
    </div>
