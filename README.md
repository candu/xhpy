XHPy: XHP for Python
====================

XHPy extends Python syntax such that XML document fragments become valid Python expressions.
It is based off [XHP](https://github.com/facebook/xhp), a similar framework for PHP.

Advantages
----------
- *Simplicity*: write UI logic in a simple, expressive syntax without the need for external
  templates or templating languages.

- *Flexibility*: use Python expressions freely within XHPy tags, and vice-versa.

- *Security*: benefit from automatic escaping of text within XHPy tags.

- *Reusability*: build reusable components by subclassing :x:element.

An example
----------
The following XHPy snippet:

    class :ui:foo(:x:element):
      attribute list bar
      category %flow
      def render(self):
        a = <ul />
        for b in self.getAttribute('bar'):
          a.appendChild(<li>{b}</li>)
        return a
    print <div class="baz"><ui:foo bar={range(3)} /></div>

produces:

<div class="baz"><ul><li>1</li><li>2</li><li>3</li></ul></div>

How it works
------------
When you

    import xhpy

XHPy installs an [import hook](http://www.python.org/dev/peps/pep-0302/).
This hook traps all subsequent import statements, running them through a preprocessor
that parses a superset of Python. This preprocessor translates XHPy tags and class
names to valid Python, then executes the translated code in module scope.

This is similar to how XHP works, except:

- with, e.g., [pythonenv](http://pypi.python.org/pypi/virtualenv), you can always use
  XHPy even without access to system-wide Python package installation directories;
- by default, Python compiles bytecode .pyc files from your modules, so the
  preprocessing only needs to be done once when a module is first imported.
