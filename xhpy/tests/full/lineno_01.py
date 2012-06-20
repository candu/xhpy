class :thing(object):
  attribute
    string a,
    string b
  def method(self):
    pass
def foo():
  pass
import inspect
result = inspect.getsourcelines(foo)
