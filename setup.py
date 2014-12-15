import setuptools

classifiers = ['Development Status :: 5 - Production/Stable',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: BSD License',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 2',
               'Programming Language :: Python :: 2.6',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Programming Language :: Python :: 3.2',
               'Programming Language :: Python :: 3.3',
               'Programming Language :: Python :: 3.4',
               'Programming Language :: Python :: Implementation :: CPython',
               'Programming Language :: Python :: Implementation :: PyPy',
               'Topic :: Database',
               'Topic :: Software Development :: Libraries']

setuptools.setup(name='pgpasslib',
                 version='1.0.1',
                 description='Library for getting passwords from PostgreSQL '
                             'password files',
                 long_description=open('README.rst').read(),
                 author='Gavin M. Roy',
                 author_email='gavinmroy@gmail.com',
                 keywords='postgresql schema',
                 url='http://pgpasslib.readthedocs.org',
                 py_modules=['pgpasslib'],
                 package_data={'': ['LICENSE', 'README.rst']},
                 include_package_data=True,
                 license=open('LICENSE').read(),
                 classifiers=classifiers)
