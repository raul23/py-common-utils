from setuptools import setup

setup(name='utilities',
      version='0.1',
      description='Library ...',
      long_description='Library ...',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
      ],
      keywords='python library utilities',
      url='https://github.com/raul23/utilities',
      author='Raul C.',
      author_email='rchfe23@gmail.com',
      license='MIT',
      packages=['utils', 'utils/databases', 'utils/exceptions', 'utils/logging'],
      zip_safe=False)
