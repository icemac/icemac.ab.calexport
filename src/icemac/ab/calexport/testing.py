import gocept.testing.assertion
import icemac.ab.calendar.testing
import icemac.ab.calexport
import icemac.addressbook.testing


ZCML_LAYER = icemac.addressbook.testing.SecondaryZCMLLayer(
    'CalExport', __name__, icemac.ab.calexport,
    bases=[icemac.ab.calendar.testing.ZCML_LAYER])
ZODB_LAYER = icemac.addressbook.testing.ZODBLayer(
    'CalExport', ZCML_LAYER)
TEST_BROWSER_LAYER = icemac.addressbook.testing.TestBrowserLayer(
    'CalExport', ZODB_LAYER)
SELENIUM_LAYER = icemac.addressbook.testing.SeleniumLayer(
    'CalExport', ZODB_LAYER)


# class UnitTestCase(icemac.ab.calendar.testing.UnitTestCase):
#     """Test case for unittests."""


class ZCMLTestCase(icemac.ab.calendar.testing.ZCMLTestCase):
    """Test case for test which only need the ZCML registrations."""

    layer = ZCML_LAYER


# class ZODBTestCase(icemac.ab.calendar.testing.ZODBTestCase):
#     """Test case for test which need the ZODB."""

#     layer = ZODB_LAYER


class BrowserTestCase(icemac.ab.calendar.testing.BrowserTestCase,
                      gocept.testing.assertion.Exceptions,
                      gocept.testing.assertion.String):
    """Test case for browser tests."""

    layer = TEST_BROWSER_LAYER


# class SeleniumTestCase(icemac.ab.calendar.testing.SeleniumTestCase):
#     """Test case for selenium tests."""

#     layer = SELENIUM_LAYER
