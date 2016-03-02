from icemac.ab.calendar.interfaces import IEvent
from icemac.ab.calexport.testing import get_masterdata
import icemac.ab.calexport
import icemac.ab.calexport.testing
import icemac.addressbook.conftest
import icemac.addressbook.testing
import pytest


pytest_plugins = (
    'icemac.addressbook.conftest',
    'icemac.ab.calendar.conftest'
)


# Fixtures to set-up infrastructure which are usable in tests:


@pytest.fixture('function')
def browser(browserWsgiAppS):
    """Fixture for testing with zope.testbrowser."""
    assert icemac.addressbook.conftest.CURRENT_CONNECTION is not None, \
        "The `browser` fixture needs a database fixture like `address_book`."
    return icemac.ab.calexport.testing.Browser(wsgi_app=browserWsgiAppS)


@pytest.fixture('session')
def MasterDataFieldFactory(FieldFactory):
    """Create a field and add it as `special_field` to export master data."""
    def create_masterdata_field(
            address_book, attr_name, iface=IEvent, field_type=u'Bool',
            field_title=u'Special?'):
        """Parameters:

        attr_name ... name of the attribute to put the field on e. g.
                      "special_field"
        iface ... interface of the entity for which the field should be created
        field_type ... type of the field, see `FieldTypeSource`.
        field_title ... title for the field
        """
        field = FieldFactory(address_book, iface, field_type, field_title)
        if iface == IEvent:
            # Only fields on IEvent can be set on master data, not the ones on
            # IRecurringEvent!
            setattr(get_masterdata(address_book), attr_name, field)
        return field
    return create_masterdata_field


# Infrastructure fixtures


@pytest.yield_fixture(scope='session')
def zcmlS(zcmlS):
    """Load calendar export ZCML on session scope."""
    layer = icemac.addressbook.testing.SecondaryZCMLLayer(
        'CalendarExport', __name__, icemac.ab.calexport, [zcmlS])
    layer.setUp()
    yield layer
    layer.tearDown()
