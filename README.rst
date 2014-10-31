pgpasslib
=========
pgpasslib is a library for retrieving passwords from a PostgreSQL password
file, either from a location specified in the ``PGPASSFILE`` environment
variable or in the ``.pgpass`` file in the current user's home directory.

|Version| |Downloads| |Status| |Coverage| |License|

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

.. |Version| image:: https://badge.fury.io/py/pgpasslib.svg?
   :target: http://badge.fury.io/py/pgpasslib

.. |Status| image:: https://travis-ci.org/gmr/pgpasslib.svg?branch=master
   :target: https://travis-ci.org/gmr/pgpasslib

.. |Coverage| image:: https://coveralls.io/repos/gmr/pgpasslib/badge.png
   :target: https://coveralls.io/r/gmr/pgpasslib
   
.. |Downloads| image:: https://pypip.in/d/pgpasslib/badge.svg?
   :target: https://pypi.python.org/pypi/pgpasslib

.. |License| image:: https://pypip.in/license/pgpasslib/badge.svg?
   :target: https://pgpasslib.readthedocs.org
