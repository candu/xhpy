from xhpy.pylib import *
class :ui:foo(:x:element):
  attribute list bar
  category %flow
  def render(self):
    a = <ul />
    for b in self.getAttribute('bar'):
      a.appendChild(<li>{b}</li>)
    return a
print <div class="baz"><ui:foo bar={range(3)} /></div>
