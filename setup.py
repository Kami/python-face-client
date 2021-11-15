# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import re
from setuptools import setup

version_re = re.compile(
    r'__version__ = (\(.*?\))')

cwd = os.path.dirname(os.path.abspath(__file__))
fp = open(os.path.join(cwd, 'face_client', '__init__.py'))

version = None
for line in fp:
    match = version_re.search(line)
    if match:
        version = eval(match.group(1))
        break
else:
    raise Exception('Cannot find version in __init__.py')
fp.close()

setup(name='face_client',
      version='.' . join(map(str, version)),
      description='SkyBiometry Face Detection and Recognition API Python client library',
      author='Tomaž Muraus',
      author_email='tomaz@tomaz.me',
      license='BSD',
      url='http://github.com/Liuftvafas/python-face-client',
      download_url='http://github.com/Liuftvafas/python-face-client/',
      packages=['face_client'],
      provides=['face_client'], 
      install_requires=[
          'requests',
		  'future'
        ],	  
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
