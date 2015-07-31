import icemac.ab.calendar.interfaces
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


class TestMixIn(object):
    """Helper funcions."""

    def create_special_field(
            self, md, iface=icemac.ab.calendar.interfaces.IEvent,
            set_on_masterdata=True):
        """Create a field and add it at special_field to master data.

        md .. ExportMasterData instance
        iface ... interface of the entity for which the field should be created
        set_on_masterdata ... Set the field as special_field on master data
        """
        from icemac.addressbook.testing import create_field
        from icemac.addressbook.interfaces import IEntity
        field_name = create_field(
            self.layer['addressbook'], iface, u'Bool', u'Special?')
        field = IEntity(iface).getRawField(field_name)
        if set_on_masterdata:
            md.special_field = field
        return field


class ZCMLTestCase(icemac.ab.calendar.testing.ZCMLTestCase):
    """Test case for test which only need the ZCML registrations."""

    layer = ZCML_LAYER


class ZODBTestCase(icemac.ab.calendar.testing.ZODBTestCase,
                   TestMixIn):
    """Test case for test which need the ZODB."""

    layer = ZODB_LAYER


class BrowserTestCase(icemac.ab.calendar.testing.BrowserTestCase,
                      gocept.testing.assertion.Exceptions,
                      gocept.testing.assertion.String,
                      TestMixIn):
    """Test case for browser tests."""

    layer = TEST_BROWSER_LAYER
