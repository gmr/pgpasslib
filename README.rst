pgpasslib
=========
pgpasslib is a library for retrieving passwords from a PostgreSQL password
file, either from a location specified in the ``PGPASSFILE`` environment
variable or in the ``.pgpass`` file in the current user's home directory.

|Version| |Downloads| |Status| |Coverage| |CodeClimate|

Installation
------------
pgpasslib may be installed via the Python package index with the tool of
your choice. I prefer pip:

.. code:: bash

    pip install pgpasslib

Documentation
-------------

https://pgpasslib.readthedocs.org

Requirements
------------
There are no requirements outside of the Python standard library.

Example
-------
The following example will attempt to get the password for PostgreSQL running
on ``localhost:5432`` to the ``postgres`` database as the ``postgres`` user.

.. code:: python

    import pgpasslib

    password = pgpasslib.getpass('localhost', 5432, 'postgres', 'postgres')
    if not password:
        raise ValueError('Did not find a password in the .pgpass file')

Version History
---------------
Available at https://pgpasslib.readthedocs.org

.. |Version| image:: https://img.shields.io/pypi/v/pgpasslib.svg?
   :target: https://pypi.python.org/pypi/pgpasslib

.. |Status| image:: https://img.shields.io/travis/gmr/pgpasslib.svg?
   :target: https://travis-ci.org/gmr/pgpasslib

.. |Coverage| image:: https://img.shields.io/codecov/c/github/gmr/pgpasslib.svg?
   :target: https://codecov.io/github/gmr/pgpasslib?branch=master

.. |Downloads| image:: https://img.shields.io/pypi/dm/pgpasslib.svg?
   :target: https://pypi.python.org/pypi/pgpasslib

.. |CodeClimate| image:: https://codeclimate.com/github/gmr/pgpasslib/badges/gpa.svg
   :target: https://codeclimate.com/github/gmr/pgpasslib
   :alt: Code Climate
