XHPy: XHP for Python
====================

`XHPy <https://github.com/candu/xhpy>`_ extends Python syntax such that XML document
fragments become valid Python expressions. It is based off
`XHP <https://github.com/facebook/xhp>`_, a similar framework for PHP.

Advantages
----------
- *Simplicity*: write UI logic in a simple, expressive syntax without the need for external
  templates or templating languages.

- *Flexibility*: use Python expressions freely within XHPy tags, and vice-versa.

- *Security*: benefit from automatic escaping of text within XHPy tags.

- *Reusability*: build reusable components by subclassing :x:element.

An example
----------
In bar.py:

::

    import xhpy.init
    import foo

In foo.py:

::

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

We can now run bar.py as a normal Python script:

::

    $ python bar.py
    <div class="baz"><ul><li>0</li><li>1</li><li>2</li></ul></div>

Congratulations! You just wrote your first snippet of XHPy.

Syntax
------

XHPy adds some new syntax to Python. Line by line replay time!

::

    import xhpy.init

This initializes XHPy; from now on, everything you import will be interpreted as XHPy.
To actually use XHPy, however, you will probably want the core library:

::

    from xhpy.pylib import *

Now you have access to all the standard HTML 4.0 elements, the ``:x:element`` base class
(this is what you build custom components on top of!), and some utilities.

::

    class :ui:foo(:x:element):

Making new components is easy: just subclass ``:x:element``. For your component class to be
registered, it must start with ``:`` - this clearly distinguishes your components from
ordinary Python classes.

::

    attribute list bar

This is an attribute declaration, meaning that ``:ui:foo`` allows bar attributes on ``<ui:foo>``
tags. Note the

::

    <ui:foo bar={range(3)} />

later on - like XHP, XHPy uses XML attribute syntax.

::

    category %flow

This is a category declaration - ``:ui:foo`` is part of the ``%flow`` category. Categories are
primarily useful as a way of identifying elements that are similar without using
inheritance; for example, the ``<a>`` tag in pylib.html has

::

    children (pcdata | %flow)*

indicating that its children must either contain text or be of the ``%flow`` category. (So
we can put ``<ui:foo>`` inside ``<a>``!)

::

    def render(self):    

When you print an ``:x:element`` (or call ``str`` on it), the ``render()`` method is invoked; this
is where you put your UI logic.

::

    a = <ul />
    for b in self.getAttribute('bar'):
        a.appendChild(<li>{b}</li>)
    return a

Here, ``<ui:foo>`` is a thin wrapper around ``<ul>`` that allows you to construct an unordered
list out of a Python list. Standard HTML elements like ``<ul>`` and ``<li>`` are automatically
rendered - except that, in XHPy, you can use Python expressions within tags, so that

::

    {b}

is replaced by the value of b. Note the use of ``getAttribute()`` and ``appendChild()``:

::

    self.getAttribute('bar')

fetches the value of attribute ``bar`` (in this case, ``range(3)``), whereas

::

    a.appendChild(<li>{b}</li>)

adds ``<li>{b}</li>`` as a child of ``a = <ul />``.

XHPy is largely based off XHP; for more details on the latter, see the
`XHP wiki <https://github.com/facebook/xhp/wiki/`_. The syntax has been adapted for
Python; in particular:

- there are no semicolons;
- XHPy class names may be used anywhere ordinary Python classes can;
- XHPy tags ignore internal whitespace, but must externally obey indentation and
  line continuation rules.
  
More on the last point:

::

    def foo(href):
      return <a href={href}></a>

    def bar(href):
      return\
      <a href={href}></a>

are valid, whereas

::

    def foo(href):
      return\
        <a href={href}>
        </a>

is not, as it introduces an extra dedent after ``</a>``.

How it works
------------
When you

::

    import xhpy.init

XHPy installs an `import hook <http://www.python.org/dev/peps/pep-0302/>`_.
This hook traps all subsequent import statements, running them through a preprocessor
that parses a superset of Python. This preprocessor translates XHPy tags and class
names to valid Python, then executes the translated code in module scope.

This is similar to how XHP works, except:

- with, e.g., `pythonenv <http://pypi.python.org/pypi/virtualenv>`_, you can always use
  XHPy even without access to system-wide Python package installation directories;
- by default, Python compiles bytecode .pyc files from your modules, so the
  preprocessing only needs to be done once when a module is first imported.
