"""setup.py file for the package `pyutils`.

The PyPi project name is py-common-utils and the package name is `pyutils`.

"""

import os
from setuptools import find_packages, setup


# Directory of this file
dirpath = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(dirpath, "README.md")) as f:
    README = f.read()

setup(name='py-common-utils',
      version='1.0',
      description='Library of common Python utilities',
      long_description=README,
      long_description_content_type='text/markdown',
      classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries'
      ],
      keywords='python library utilities',
      url='https://github.com/raul23/utilities',
      author='Raul C.',
      author_email='rchfe23@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      zip_safe=False)