This package provides a calendar HTML export feature for `icemac.ab.calendar`_.

*Caution:* This package might not be as customizable as needed for a general
HTML calendar export.

.. _`icemac.ab.calendar` : https://pypi.org/project/icemac.ab.calendar

Copyright (c) 2015-2019 Michael Howitz

This package is licensed under the MIT License, see LICENSE.txt inside the
package.

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

  $ virtualenv-2.7 .
  $ bin/pip install zc.buildout
  $ bin/buildout -n
  $ bin/py.test
