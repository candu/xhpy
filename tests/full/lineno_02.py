def foo():
 return <x>&#187;</x>
def bar():
  pass
import inspect
print inspect.getsourcelines(bar)[1]
