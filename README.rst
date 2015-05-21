This package provides a calendar export feature for `icemac.ab.calendar`_.

.. _`icemac.ab.calendar` : http://pypi.python.org/pypi/icemac.ab.calendar

Copyright (c) 2015 Michael Howitz

All Rights Reserved.

This software is subject to the provisions of the Zope Public License,
Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
FOR A PARTICULAR PURPOSE.

.. contents::

=========
 Hacking
=========

Source code
===========

Get the source code::

   $ hg clone https://bitbucket.org/icemac/icemac.ab.calexport

or fork me on: https://bitbucket.org/icemac/icemac.ab.calexport

Running the tests
=================

To run the tests yourself call::

  $ python2.7 bootstrap.py
  $ bin/buildout -n
  $ bin/py.test
