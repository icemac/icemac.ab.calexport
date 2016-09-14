from icemac.ab.calendar.interfaces import IEvent
from icemac.ab.calexport.testing import get_masterdata
from icemac.addressbook.interfaces import IEntity
from mechanize import LinkNotFoundError, HTTPError
import pytest


def test_export__Masterdata__1(
        address_book, CategoryFactory, MasterDataFieldFactory, browser):
    """It saves the entered data."""
    CategoryFactory(address_book, u'foo')
    CategoryFactory(address_book, u'bar')
    MasterDataFieldFactory(
        address_book, 'special_field', field_title=u'Special?')
    MasterDataFieldFactory(
        address_book, 'custom_field', field_title=u'Custom?')
    browser.login('cal-export-editor')
    browser.open(browser.CALENDAR_MASTERDATA_URL)
    browser.getLink('Configure export').click()
    assert browser.CALEXPORT_MASTER_DATA_URL == browser.url
    assert browser.getControl('Name for the generated').value == 'export.html'
    browser.getControl('HTML to be inserted above').value = '<html>cal'
    browser.getControl('foo').selected = True
    browser.getControl('Special?').selected = True
    browser.getControl('Name for the generated').value = 'events.html'
    browser.getControl('Apply').click()
    assert 'Data successfully updated.' == browser.message
    browser.open(browser.CALEXPORT_MASTER_DATA_URL)
    assert '<html>cal' == browser.getControl('HTML to be inserted above').value
    assert browser.getControl('foo').selected
    assert not browser.getControl('bar').selected
    assert browser.getControl('Special?').selected
    assert not browser.getControl('Custom?').selected
    assert browser.getControl('Name for the generated').value == 'events.html'


def test_export__Masterdata__2(address_book, browser):
    """There is no link rendered to it for users with the exporter role."""
    browser.login('cal-exporter')
    browser.open(browser.CALENDAR_MASTERDATA_URL)
    with pytest.raises(LinkNotFoundError):
        browser.getLink('Configure export')


def test_export__Masterdata__3(address_book, browser):
    """It cannot be accessed for users with the exporter role."""
    browser.login('cal-exporter')
    with pytest.raises(HTTPError) as err:
        browser.open(browser.CALEXPORT_MASTER_DATA_URL)
    assert 'HTTP Error 403: Forbidden' == str(err.value)


@pytest.mark.parametrize(
    'attr_name,field_type,field_title', [
        ['special_field', 'Bool', 'Special?'],
        ['url_field', 'URI', 'URL'],
    ])
def test_export__ExportMasterData__special_field__1(
        address_book, MasterDataFieldFactory,
        attr_name, field_type, field_title):
    """It stores and returns a field reference."""
    md = get_masterdata(address_book)
    # None by default
    assert None is getattr(md, attr_name)
    field = MasterDataFieldFactory(
        address_book, attr_name, field_type=unicode(field_type),
        field_title=unicode(field_title))
    assert field == getattr(md, attr_name)
    # The attribute is a property which stores a field reference
    private_attr_name = '_{}'.format(attr_name)
    assert ('IcemacAbCalendarEventEvent###Field-1' ==
            getattr(md, private_attr_name))
    # Reset to None is possible, too
    setattr(md, attr_name, None)
    assert None is getattr(md, attr_name)
    assert None is getattr(md, private_attr_name)


@pytest.mark.parametrize(
    'attr_name,field_type,field_title', [
        ['special_field', 'Bool', 'Special?'],
        ['url_field', 'URI', 'URL'],
    ])
def test_export__ExportMasterData__special_field__2(
        address_book, MasterDataFieldFactory,
        attr_name, field_type, field_title):
    """It does not break on a deleted field."""
    field = MasterDataFieldFactory(
        address_book, attr_name, field_type=unicode(field_type),
        field_title=unicode(field_title))
    IEntity(IEvent).removeField(field)
    assert None is getattr(get_masterdata(address_book), attr_name)
