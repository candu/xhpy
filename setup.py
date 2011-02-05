import os.path
from distutils.core import setup

ROOT = os.path.abspath(os.path.dirname(__file__))

setup(
  name = 'xhpy',
  packages = [
    'xhpy',
    'xhpy.init',
    'xhpy.parser',
    'xhpy.pylib'
  ],
  version = '0.6',
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
