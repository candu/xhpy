class :foo(object):
  bar = None
  etc = 1
:foo.bar = 2
result = {'etc': :foo.etc, 'bar': :foo.bar}
