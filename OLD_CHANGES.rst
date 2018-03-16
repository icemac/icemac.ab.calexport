===========================
 Change log older versions
===========================

Change log of releases more than 2 minor versions behind the current version.

1.4 (2017-02-04)
================

- Update test infrastructure to `icemac.addressbook >= 3.0` and
  `icemac.ab.calendar >= 2.0`.

- Fix rendering glitch of whole day events in the forecast list.


1.3.1 (2017-01-08)
==================

- Fix forecast list:

  - Render datetime localized to browser language.

  - Prevent double quoting of the test.


1.3 (2017-01-07)
================

- Prevent an error which might occur if HTML header or HTML footer in master
  data are empty.

- Bring test coverage to 100 %.

- Adapt code to `icemac.ab.calendar >= 1.11`.

- Adapt role configuration to `icemac.addressbook >= 2.9`.


1.2 (2016-08-28)
================

- Add a forecast list below the calendar. It contains the special events of
  the next year.


1.1 (2016-06-25)
================

- Fix error on export if no categories where selected in master data.

- Add ability to render a special CSS class for certain events.

- Add ability to render an event as a hyperlink.

- Use `py.test` fixtures in the tests + convert tests to use the class-less
  approach.

- Make compatible with `icemac.ab.calendar` 1.8 thus requiring at least this
  version.


1.0.0 (2015-05-24)
==================

- Initial release.
