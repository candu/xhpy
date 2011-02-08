import os.path
from distutils.core import setup

# The standard distutils bytecode generation step spits out stacktraces on
# trying to parse xhpy/pylib/core.py and xhpy/pylib/html.py as Python, so
# we disable it here.
import sys
sys.dont_write_bytecode = True

ROOT = os.path.abspath(os.path.dirname(__file__))
setup(
  name = 'xhpy',
  packages = [
    'xhpy',
    'xhpy.pylib'
  ],
  version = '0.7',
  author = 'Evan Stratford',
  author_email = 'evan.stratford@gmail.com',
  license = 'Apache',
  description = 'XHP for Python',
  url = 'http://github.com/candu/xhpy',
  keywords = ['xhp', 'html', 'xml'],
  classifiers = [
    'Programming Language :: Python',
    # TODO: test for Python 3 compatibility
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Code Generators',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Text Processing :: Markup'
  ],
  long_description = open(os.path.join(ROOT, 'README.rst')).read(),
)
