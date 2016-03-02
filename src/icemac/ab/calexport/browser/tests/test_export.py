from ..export import CalendarActions
from icemac.ab.calexport.testing import get_masterdata
import pytest


# Fixtures


@pytest.fixture('function')
def sample_category(address_book, CategoryFactory):
    """A sample event category to be used in tests."""
    return CategoryFactory(address_book, u'calendar-export-test')


@pytest.fixture('function')
def export_address_book(
        address_book, sample_category, EventFactory, DateTime):
    """Address boo with some export data in it.

    It defines the `sample_category` to be used for export of the events.
    """
    EventFactory(address_book, category=sample_category,
                 datetime=DateTime.now)
    get_masterdata(address_book).categories = set([sample_category])
    return address_book


# Tests


def test_export__CalendarActions__update__1(address_book, browser):
    """It renders the export button a calendar exporter user."""
    browser.login('cal-exporter')
    browser.open(browser.CALENDAR_OVERVIEW_URL)
    assert browser.getControl(CalendarActions.export_button_title)


def test_export__CalendarActions__update__2(address_book, browser):
    """It does not rendered the export button for a calendar editor user.

    Because he is not allowed to export.
    """
    browser.login('cal-editor')
    browser.open(browser.CALENDAR_OVERVIEW_URL)
    with pytest.raises(LookupError):
        browser.getControl(CalendarActions.export_button_title)


def test_export__CalendarExportView__1(export_address_book, browser):
    """It returns no events if no categories are set in master data."""
    get_masterdata(export_address_book).categories = set()
    browser.login('cal-exporter')
    browser.open(browser.CALENDAR_OVERVIEW_URL)
    browser.getControl('Export current month').click()
    assert browser.CALEXPORT_MONTH_EXPORT_URL == browser.url
    assert '<dd>' not in browser.contents


def test_export__CalendarExportView__2(
        export_address_book, sample_category, browser):
    """It returns header, calendar and footer."""
    md = get_masterdata(export_address_book)
    md.categories = set([sample_category])
    md.html_head = u'<html-head>'
    md.html_foot = u'</html-foot>'
    browser.login('cal-exporter')
    browser.open(browser.CALEXPORT_MONTH_EXPORT_URL)
    assert ('attachment; filename=export.html' ==
            browser.headers['content-disposition'])
    assert browser.contents.startswith('<html-head>')
    assert (['calendar-export-test'] ==
            [x.strip() for x in browser.etree.xpath('//dd/text()')])
    assert browser.contents.endswith('</html-foot>')


def test_export__CalendarExportView__3(
        export_address_book, CategoryFactory, EventFactory, DateTime, browser):
    """It returns only events having the selected categories."""
    category = CategoryFactory(export_address_book, u'selected-category-name')
    get_masterdata(export_address_book).categories = set([category])
    EventFactory(export_address_book, category=category, datetime=DateTime.now)
    browser.login('cal-exporter')
    browser.open(browser.CALEXPORT_MONTH_EXPORT_URL)
    assert (['selected-category-name'] ==
            [x.strip() for x in browser.etree.xpath('//dd/text()')])
    assert 'calendar-export-test' not in browser.contents


def test_export__CalendarExportView__4(
        address_book, sample_category, EventFactory, MasterDataFieldFactory,
        DateTime, browser):
    """It sets the CSS class ``special`` on events where the special field ...

    ... is set.
    """
    get_masterdata(address_book).categories = set([sample_category])
    EventFactory(address_book, **{
        'category': sample_category,
        'datetime': DateTime.now,
        MasterDataFieldFactory(address_book, 'special_field').__name__: True})
    browser.login('cal-exporter')
    browser.open(browser.CALEXPORT_MONTH_EXPORT_URL)
    assert ['special'] == [x.attrib.get('class')
                           for x in browser.etree.xpath('//dd')]


def test_export__CalendarExportView__5(export_address_book, browser):
    """It respects the file name set in master data."""
    md = get_masterdata(export_address_book)
    md.filename = u'cal.htm'
    browser.login('cal-exporter')
    browser.open(browser.CALEXPORT_MONTH_EXPORT_URL)
    assert ('attachment; filename=cal.htm' ==
            browser.headers['content-disposition'])
