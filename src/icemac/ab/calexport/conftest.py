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
def SpecialFieldFactory(FieldFactory):
    """Create a field and add it as `special_field` to export master data."""
    def create_special_field(
            address_book, iface=IEvent, set_on_masterdata=True):
        """Parameters:

        iface ... interface of the entity for which the field should be created
        set_on_masterdata ... Set the field as `special_field` on master data
        """
        field = FieldFactory(address_book, iface, u'Bool', u'Special?')
        if set_on_masterdata:
            get_masterdata(address_book).special_field = field
        return field
    return create_special_field


# Infrastructure fixtures


@pytest.yield_fixture(scope='session')
def zcmlS(zcmlS):
    """Load calendar export ZCML on session scope."""
    layer = icemac.addressbook.testing.SecondaryZCMLLayer(
        'CalendarExport', __name__, icemac.ab.calexport, [zcmlS])
    layer.setUp()
    yield layer
    layer.tearDown()
