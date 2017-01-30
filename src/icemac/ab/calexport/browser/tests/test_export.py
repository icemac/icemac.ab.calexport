from icemac.ab.calexport.testing import get_masterdata
import pytest


# Fixtures


@pytest.fixture('function')
def sample_category(address_book, CategoryFactory):
    """A sample event category to be used in tests."""
    return CategoryFactory(address_book, u'calendar-export-test')


@pytest.fixture('function')
def export_address_book(
        address_book, sample_category, EventFactory, MasterDataFieldFactory,
        CategoryFactory, DateTime):
    """Address book with some export data in it.

    It defines the `sample_category` to be used for export of the events.
    """
    special_field = MasterDataFieldFactory(address_book, 'special_field')
    EventFactory(address_book, category=sample_category,
                 datetime=DateTime.now)
    EventFactory(address_book, category=sample_category,
                 alternative_title=u'non-special event in next month',
                 datetime=DateTime.add(DateTime.now, 31))
    EventFactory(address_book, category=sample_category,
                 alternative_title=u'special event in next month',
                 datetime=DateTime.add(DateTime.now, 32),
                 **{special_field.__name__: True})
    EventFactory(address_book,
                 category=CategoryFactory(address_book, u'other'),
                 alternative_title=u'special event next month other category',
                 datetime=DateTime.add(DateTime.now, 32),
                 **{special_field.__name__: True})
    get_masterdata(address_book).categories = set([sample_category])
    return address_book


# Tests


def test_export__CalendarActions__update__1(address_book, browser):
    """It renders the export button a calendar exporter user."""
    browser.login('cal-exporter')
    browser.open(browser.CALENDAR_MONTH_OVERVIEW_URL)
    assert (['form.buttons.apply', 'form.buttons.export'] ==
            browser.submit_control_names)


def test_export__CalendarActions__update__2(address_book, browser):
    """It does not rendered the export button for a calendar editor user.

    Because he is not allowed to export.
    """
    browser.login('cal-editor')
    browser.open(browser.CALENDAR_MONTH_OVERVIEW_URL)
    assert browser.CALENDAR_MONTH_OVERVIEW_URL == browser.url  # no log-in form
    assert ['form.buttons.apply'] == browser.submit_control_names


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
    """It returns header, calendar, forecast and footer."""
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
            [x.strip() for x in browser.etree.xpath('//td/dl/dd/text()')])
    assert browser.contents.endswith('</html-foot>')
    assert (['special event in next month'] ==
            [x.strip() for x in browser.etree.xpath('//div/dl/dd/text()')])
    # The forecast only contains a headline the one months having an event:
    assert 1 == len(browser.etree.xpath('//div/h2'))
    assert 'non-special event in next month' not in browser.contents
    assert browser.contents.endswith('</html-foot>')


def test_export__CalendarExportView__2_5(
        export_address_book, sample_category, browser):
    """It does not break if head or foot is `None`.."""
    md = get_masterdata(export_address_book)
    md.categories = set([sample_category])
    md.html_head = None
    md.html_foot = None
    browser.login('cal-exporter')
    browser.handleErrors = False
    browser.open(browser.CALEXPORT_MONTH_EXPORT_URL)
    assert (['calendar-export-test'] ==
            [x.strip() for x in browser.etree.xpath('//td/dl/dd/text()')])


def test_export__CalendarExportView__3(
        export_address_book, CategoryFactory, EventFactory, DateTime, browser):
    """It returns only events having the selected categories.

    It renders the date times nicely.
    """
    category = CategoryFactory(export_address_book, u'selected-category-name')
    md = get_masterdata(export_address_book)
    md.categories = set([category])
    special_field_name = md.special_field.__name__
    EventFactory(export_address_book, category=category, datetime=DateTime.now)
    non_whole_day = EventFactory(
        export_address_book, category=category,
        alternative_title=u'sel-cat-next-month',
        datetime=DateTime.add(DateTime.now, 32),
        **{special_field_name: True})
    whole_day = EventFactory(
        export_address_book, category=category,
        alternative_title=u'sel-cat-next-month-whole-day',
        datetime=DateTime.add(DateTime.now, 32),
        whole_day_event=True,
        **{special_field_name: True})
    browser.login('cal-exporter')
    browser.open(browser.CALEXPORT_MONTH_EXPORT_URL)
    assert (['selected-category-name'] ==
            [x.strip() for x in browser.etree.xpath('//td/dl/dd/text()')])
    assert (['sel-cat-next-month-whole-day', 'sel-cat-next-month'] ==
            [x.strip() for x in browser.etree.xpath('//div/dl/dd/text()')])
    assert ([DateTime.format(whole_day.datetime).split()[0] + u' \u200b',
             DateTime.format(non_whole_day.datetime)] ==
            [x.strip() for x in browser.etree.xpath('//div/dl/dt/text()')])
    assert 'special event next month other category' not in browser.contents
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
