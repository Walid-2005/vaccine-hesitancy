test_runner.py (Source Code and Docstrings)
===========================================

This module defines a custom Django test runner that bypasses test database creation
and teardown. It is useful when working with pre-seeded or read-only databases.

.. literalinclude:: ../../test_runner.py
   :language: python
   :linenos:
