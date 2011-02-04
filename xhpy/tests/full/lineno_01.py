class :thing(object):
  attribute
    string a,
    string b
  def method(self):
    pass
def foo():
  pass
import inspect
print inspect.getsourcelines(foo)
