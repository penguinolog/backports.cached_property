backports.cached_property
=========================

.. image:: https://travis-ci.com/penguinolog/backports.cached_property.svg?branch=master
    :target: https://travis-ci.com/penguinolog/backports.cached_property
.. image:: https://img.shields.io/pypi/v/backports.cached-property.svg
    :target: https://pypi.python.org/pypi/backports.cached-property
.. image:: https://img.shields.io/pypi/pyversions/backports.cached-property.svg
    :target: https://pypi.python.org/pypi/backports.cached-property
.. image:: https://img.shields.io/pypi/status/backports.cached-property.svg
    :target: https://pypi.python.org/pypi/backports.cached-property
.. image:: https://img.shields.io/github/license/penguinolog/backports.cached_property.svg
    :target: https://raw.githubusercontent.com/penguinolog/backports.cached_property/master/LICENSE
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

What
----

Python 3.8 adds great descriptor to functools: cached_property.
Technically all required APIs was available since python 3.6,
but it is what it is.

This package is a backport of this functionality for python 3.6 and 3.7.

How to use
----------

.. code-block:: python

    from backports.cached_property import cached_property

And then python 3.8 documentation will work (because code is minimally changed):

.. class:: cached_property

   Transform a method of a class into a property whose value is computed once
   and then cached as a normal attribute for the life of the instance. Similar
   to `property`, with the addition of caching. Useful for expensive
   computed properties of instances that are otherwise effectively immutable.

   Example::

       class DataSet:
           def __init__(self, sequence_of_numbers):
               self._data = sequence_of_numbers

           @cached_property
           def stdev(self):
               return statistics.stdev(self._data)

           @cached_property
           def variance(self):
               return statistics.variance(self._data)


   .. note::

      This decorator requires that the ``__dict__`` attribute on each instance
      be a mutable mapping. This means it will not work with some types, such as
      metaclasses (since the ``__dict__`` attributes on type instances are
      read-only proxies for the class namespace), and those that specify
      ``__slots__`` without including ``__dict__`` as one of the defined slots
      (as such classes don't provide a ``__dict__`` attribute at all).
