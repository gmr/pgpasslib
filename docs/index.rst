pgpasslib
=========
pgpasslib is a library for retrieving passwords from a PostgreSQL password
file, either from a location specified in the ``PGPASSFILE`` environment
variable or in the ``.pgpass`` file in the current user's home directory.

|Version| |Downloads|

Installation
------------
pgpasslib may be installed via the Python package index with the tool of
your choice. I prefer pip:

.. code:: bash

    pip install pgpasslib

Requirements
------------
There are no requirements outside of the Python standard library.

API Documentation
-----------------

.. automodule:: pgpasslib
   :members:


Version History
---------------
See :doc:`history`

Issues
------
Please report any issues to the Github project at `https://github.com/gmr/pgpasslib/issues <https://github.com/gmr/pgpasslib/issues>`_

Source
------
pgpasslib source is available on Github at `https://github.com/gmr/pgpasslib <https://github.com/gmr/pgpasslib>`_

License
-------
pgpasslib is released under the `3-Clause BSD license <https://github.com/gmr/pgpasslib/blob/master/LICENSE>`_.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |Version| image:: https://img.shields.io/pypi/v/pgpasslib.svg?
   :target: https://pypi.python.org/pypi/pgpasslib

.. |Downloads| image:: https://img.shields.io/pypi/dm/pgpasslib.svg?
   :target: https://pypi.python.org/pypi/pgpasslib
