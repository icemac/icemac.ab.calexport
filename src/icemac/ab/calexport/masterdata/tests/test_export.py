from icemac.ab.calendar.interfaces import IEvent
from icemac.ab.calexport.testing import get_masterdata
from icemac.addressbook.interfaces import IEntity
from mechanize import LinkNotFoundError, HTTPError
import pytest


def test_export__Masterdata__1(address_book, CategoryFactory, browser):
    """It saves the entered data."""
    CategoryFactory(address_book, u'foo')
    CategoryFactory(address_book, u'bar')
    browser.login('cal-export-editor')
    browser.open(browser.CALENDAR_MASTERDATA_URL)
    browser.getLink('Configure export').click()
    assert browser.CALEXPORT_MASTER_DATA_URL == browser.url
    browser.getControl('HTML to be inserted above').value = '<html>cal'
    browser.getControl('foo').selected = True
    browser.getControl('Apply').click()
    assert 'Data successfully updated.' == browser.message
    browser.open(browser.CALEXPORT_MASTER_DATA_URL)
    assert '<html>cal' == browser.getControl('HTML to be inserted above').value
    assert browser.getControl('foo').selected
    assert not browser.getControl('bar').selected


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


# class ExportMasterDataTests(icemac.ab.calexport.testing.ZODBTestCase):
#     """Testing ..export.ExportMasterData."""

#     def makeOne(self):
#
#         return ExportMasterData()


def test_export__ExportMasterData__special_field__1(
        address_book, SpecialFieldFactory):
    """It stores and returns a field reference."""
    md = get_masterdata(address_book)
    # None by default
    assert None is md.special_field
    field = SpecialFieldFactory(address_book)
    assert field == md.special_field
    # `special_field` is a property which stores a field reference
    assert 'IcemacAbCalendarEventEvent###Field-1' == md._special_field
    # Reset to None is possible, too
    md.special_field = None
    assert None is md.special_field
    assert None is md._special_field


def test_export__ExportMasterData__special_field__2(
        address_book, SpecialFieldFactory):
    """It does not break on a deleted field."""
    field = SpecialFieldFactory(address_book)
    IEntity(IEvent).removeField(field)
    assert None is get_masterdata(address_book).special_field
