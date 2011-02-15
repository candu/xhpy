class :foo(object):
  attribute
    string foo
  def __init__(self):
    pass
class :bar(object):
  attribute
    :foo foo1,
    :foo foo2,
    string bar
  def __init__(self):
    pass
print "pass"
