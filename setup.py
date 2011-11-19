# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import re
from distutils.core import setup

version_re = re.compile(
    r'__version__ = (\(.*?\))')

cwd = os.path.dirname(os.path.abspath(__file__))
fp = open(os.path.join(cwd, 'face', '__init__.py'))

version = None
for line in fp:
    match = version_re.search(line)
    if match:
        version = eval(match.group(1))
        break
else:
    raise Exception('Cannot find version in __init__.py')
fp.close()

setup(name='face',
      version='.' . join(map(str, version)),
      description='face.com face recognition Python API client library',
      author='Tomaž Muraus',
      author_email='tomaz@tomaz.me',
      license='BSD',
      url='https://github.com/chris-piekarski/python-face-client',
      download_url='git://github.com/chris-piekarski/python-face-client.git',
      packages=['face'],
      provides=['face'],

      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Security',
          'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
